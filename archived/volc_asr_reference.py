"""
Archived: Volcengine (火山引擎) ASR integration reference.

Status
------
This module is NOT imported by the app currently (voice input is disabled for the web app).
It is kept here so you can quickly restore the feature later (e.g. for WeChat mini program).

How to re-enable (high-level)
----------------------------
1) Ensure dependencies are installed:
   - websocket-client
   - audio-recorder-streamlit (if you want Streamlit in-browser recording)
2) Put Volc secrets into Streamlit Secrets or env vars:
   - VOLC_ASR_WS_URL (optional)
   - VOLC_ASR_APP_KEY
   - VOLC_ASR_ACCESS_KEY
   - VOLC_ASR_RESOURCE_ID (optional)
3) Wire `record_audio_to_pcm()` and `stream_volc_asr()` back into the UI.

Notes
-----
This is based on the earlier prototype implementation, adjusted to avoid hardcoding secrets.
"""

from __future__ import annotations

import base64
import gzip
import hashlib
import json
import os
import secrets as py_secrets
import ssl
import struct
import time
import uuid
import wave
from io import BytesIO

try:
    import audioop  # type: ignore  # optional (may be removed in newer Python versions)
except Exception:
    audioop = None

try:
    import websocket  # type: ignore  # websocket-client
except Exception:
    websocket = None

try:
    from audio_recorder_streamlit import audio_recorder  # type: ignore
except Exception:
    audio_recorder = None

try:
    import streamlit as st  # type: ignore
except Exception:
    st = None


def _get_setting(name: str, default: str = "") -> str:
    if st is not None:
        try:
            if hasattr(st, "secrets") and name in st.secrets:
                return str(st.secrets[name])
        except Exception:
            pass
    return os.getenv(name, default)


# --- Volcengine ASR settings (fill via secrets/env, do NOT hardcode) ---
VOLC_ASR_WS_URL = _get_setting("VOLC_ASR_WS_URL", "wss://openspeech.bytedance.com/api/v3/sauc/bigmodel_async")
VOLC_ASR_APP_KEY = _get_setting("VOLC_ASR_APP_KEY", "")
VOLC_ASR_ACCESS_KEY = _get_setting("VOLC_ASR_ACCESS_KEY", "")
VOLC_ASR_RESOURCE_ID = _get_setting("VOLC_ASR_RESOURCE_ID", "volc.bigasr.sauc.duration")

VOLC_AUDIO_SAMPLE_RATE = 16000
VOLC_AUDIO_SAMPLE_WIDTH = 2  # 16bit = 2 bytes
VOLC_AUDIO_CHANNELS = 1
VOLC_AUDIO_FORMAT = "pcm"
VOLC_AUDIO_CHUNK_MS = 200

ERROR_CODE_MAP = {
    45000001: "参数无效",
    45000151: "音频格式错误",
    45000152: "音频过短",
    45000153: "音频过长",
}


def _generate_connect_id() -> str:
    return uuid.uuid4().hex


def _merge_asr_text(current: str, new_text: str) -> str:
    if not new_text:
        return current
    new_text = new_text.strip()
    if not current:
        return new_text
    if new_text == current:
        return current
    if new_text.startswith(current):
        return new_text
    if current.startswith(new_text):
        return current
    max_overlap = min(len(current), len(new_text))
    overlap = 0
    for size in range(max_overlap, 0, -1):
        if current.endswith(new_text[:size]):
            overlap = size
            break
    return (current + new_text[overlap:]).strip()


def record_audio_to_pcm(
    *,
    widget_key: str,
    sample_rate: int = VOLC_AUDIO_SAMPLE_RATE,
) -> bytes | None:
    """
    Streamlit-only helper: record audio in browser and return 16kHz/16bit/mono PCM bytes.

    Returns None if:
    - no recording submitted, or
    - dependencies missing.
    """
    if st is None or audio_recorder is None:
        return None

    audio_bytes = audio_recorder(
        text="",
        recording_color="#ff4b4b",
        neutral_color="#4b8bf4",
        icon_name="microphone-lines",
        icon_size="3x",
        key=widget_key,
        sample_rate=sample_rate,
    )
    if audio_bytes is None:
        return None

    digest_key = f"{widget_key}_last_digest"
    audio_hash = hashlib.sha1(audio_bytes).hexdigest()
    if st.session_state.get(digest_key) == audio_hash:
        return None
    st.session_state[digest_key] = audio_hash

    try:
        with wave.open(BytesIO(audio_bytes), "rb") as wf:
            channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            frame_rate = wf.getframerate()
            frames = wf.readframes(wf.getnframes())
    except wave.Error:
        return None

    if not frames:
        return None
    if frame_rate != VOLC_AUDIO_SAMPLE_RATE:
        return None

    if channels not in (1, 2):
        return None
    if audioop is None:
        return None

    if sample_width != VOLC_AUDIO_SAMPLE_WIDTH:
        frames = audioop.lin2lin(frames, sample_width, VOLC_AUDIO_SAMPLE_WIDTH)
        sample_width = VOLC_AUDIO_SAMPLE_WIDTH

    if channels == 2:
        frames = audioop.tomono(frames, sample_width, 0.5, 0.5)

    return frames


def build_websocket_header(message_type: int, flags: int) -> bytes:
    header = bytearray(4)
    header[0] = 0b00010001
    header[1] = ((message_type & 0x0F) << 4) | (flags & 0x0F)
    header[2] = 0b00010000
    header[3] = 0x00
    return bytes(header)


def send_protocol_packet(ws, message_type: int, flags: int, payload: bytes):
    payload = payload or b""
    header = build_websocket_header(message_type, flags)
    payload_size = struct.pack(">I", len(payload))
    ws.send_binary(header + payload_size + payload)


def _extract_payload_from_server(packet) -> bytes:
    if not packet:
        return b""
    if isinstance(packet, str):
        packet = packet.encode("utf-8")
    if len(packet) < 12:
        return b""

    header_unit = packet[0] & 0x0F
    header_len = (header_unit or 1) * 4
    if len(packet) < header_len + 8:
        return b""

    message_type = (packet[1] >> 4) & 0x0F
    compression = packet[2] & 0x0F
    offset = header_len

    if message_type == 0b1111:
        offset += 4  # error code
        payload_size = struct.unpack(">I", packet[offset : offset + 4])[0]
        offset += 4
    else:
        offset += 4  # sequence number
        payload_size = struct.unpack(">I", packet[offset : offset + 4])[0]
        offset += 4

    if len(packet) < offset + payload_size:
        return b""

    payload = packet[offset : offset + payload_size]
    if compression == 0b0001:
        payload = gzip.decompress(payload)
    return payload


def stream_volc_asr(audio_bytes: bytes) -> tuple[str | None, str | None]:
    """
    Volcengine streaming ASR.
    Returns: (text, error_message)
    """
    if websocket is None:
        return None, "Missing dependency: websocket-client"
    if not audio_bytes:
        return None, "未检测到音频数据"
    if not (VOLC_ASR_APP_KEY and VOLC_ASR_ACCESS_KEY):
        return None, "未配置火山引擎密钥"

    connect_id = _generate_connect_id()
    headers = [
        f"X-Api-App-Key: {VOLC_ASR_APP_KEY}",
        f"X-Api-Access-Key: {VOLC_ASR_ACCESS_KEY}",
        f"X-Api-Resource-Id: {VOLC_ASR_RESOURCE_ID}",
        f"X-Api-Connect-Id: {connect_id}",
    ]

    try:
        ws = websocket.create_connection(
            VOLC_ASR_WS_URL,
            header=headers,
            timeout=30,
        )
    except Exception as exc:
        return None, f"连接语音识别服务失败：{exc}"

    full_request = {
        "audio": {
            "format": VOLC_AUDIO_FORMAT,
            "sample_rate": VOLC_AUDIO_SAMPLE_RATE,
            "channels": VOLC_AUDIO_CHANNELS,
            "bit_width": VOLC_AUDIO_SAMPLE_WIDTH * 8,
            "language": "zh-CN",
        },
        "request": {
            "model_name": "bigmodel",
            "enable_punc": True,
            "enable_ddc": False,
        },
        "user_info": {"uid": "streamlit-user"},
    }

    try:
        send_protocol_packet(ws, 0b0001, 0b0000, json.dumps(full_request).encode("utf-8"))

        chunk_size = int(
            VOLC_AUDIO_SAMPLE_RATE
            * VOLC_AUDIO_CHUNK_MS
            / 1000
            * VOLC_AUDIO_SAMPLE_WIDTH
            * VOLC_AUDIO_CHANNELS
        )
        if chunk_size <= 0:
            chunk_size = 6400

        total_chunks = (len(audio_bytes) + chunk_size - 1) // chunk_size or 1
        for idx in range(total_chunks):
            start = idx * chunk_size
            end = start + chunk_size
            chunk = audio_bytes[start:end]
            if not chunk:
                continue
            is_last = 1 if idx == total_chunks - 1 else 0
            flag = 0b0010 if is_last else 0b0000
            send_protocol_packet(ws, 0b0010, flag, chunk)
            time.sleep(VOLC_AUDIO_CHUNK_MS / 1000.0)

        final_text = ""
        while True:
            packet = ws.recv()
            payload = _extract_payload_from_server(packet)
            if not payload:
                continue

            try:
                data = json.loads(payload.decode("utf-8"))
            except Exception:
                continue

            err_code = data.get("error_code") or data.get("code")
            if err_code and int(err_code) != 0:
                err_code = int(err_code)
                reason = ERROR_CODE_MAP.get(err_code, data.get("message", "未知错误"))
                return None, f"识别失败({err_code})：{reason}"

            result = data.get("result")
            seg_list = []
            if isinstance(result, dict):
                seg_list = [result]
            elif isinstance(result, list):
                seg_list = result

            for seg in seg_list or []:
                text_piece = seg.get("text")
                if not text_piece:
                    continue
                if seg.get("definite", True):
                    final_text = _merge_asr_text(final_text, text_piece)

            if data.get("end_of_result") or data.get("is_final") or data.get("final"):
                break

        if not final_text:
            return None, "未识别到有效语音内容"
        return final_text, None
    finally:
        try:
            ws.close()
        except Exception:
            pass

