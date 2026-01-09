# 实验记录AI工具 - 项目大纲

## 项目概述

### 项目名称
**Lab Diary AI** - 智能实验记录与管理工具

### 项目目标
为科研人员提供一体化的实验记录管理解决方案，结合AI技术提升科研效率，保持原始记录的完整性和准确性。

### 核心功能模块
1. **智能日程管理** - AI驱动的任务规划
2. **实验记录系统** - 完整的记录编辑与管理
3. **历史数据迁移** - 保护原始记录的一键导入
4. **语音交互** - 语音输入与识别
5. **数据可视化** - 科研数据分析与展示
6. **导出与归档** - 多格式导出功能

## 技术架构

### 前端技术栈
- **Streamlit** - Web应用框架
- **ECharts.js** - 数据可视化
- **Anime.js** - 动画效果
- **P5.js** - 音频可视化
- **Splide.js** - 轮播组件
- **Matter.js** - 物理动画
- **Shader-park** - 着色器特效

### 后端技术栈
- **Python** - 主要编程语言
- **SQLite** - 轻量级数据库
- **OpenAI API** - AI功能集成
- **火山引擎ASR** - 语音识别服务

### 数据存储
- **SQLite数据库** - 任务和记录存储
- **本地文件系统** - 附件和备份存储
- **JSON格式** - 配置文件和缓存

## 功能模块详解

### 1. 智能日程管理模块
**文件**: `modules/scheduler.py`

**核心功能**:
- AI智能解析自然语言描述
- 自动生成结构化任务列表
- 任务日期计算和排程
- 批量任务导入确认

**关键函数**:
- `ai_parse_schedule()` - AI解析用户输入
- `show_ai_confirm_dialog()` - 任务预览确认
- `calculate_task_dates()` - 日期计算逻辑

### 2. 实验记录管理模块
**文件**: `modules/records.py`

**核心功能**:
- 富文本编辑器
- 语音输入转文字
- AI润色助手
- 附件上传管理
- 标签系统

**关键函数**:
- `show_record_editor_dialog()` - 记录编辑对话框
- `stream_volc_asr()` - 语音识别
- `ai_polish_text()` - AI文本润色

### 3. 历史数据迁移模块
**文件**: `modules/importer.py`

**核心功能**:
- 多格式文件支持(.md, .doc, .docx, .txt, .csv)
- 原始内容保护模式
- AI元数据提取
- 批量导入预览
- 文件名日期解析

**关键函数**:
- `import_legacy_records()` - 主要导入函数
- `convert_document_bytes_to_markdown()` - 文档转换
- `guess_record_date_from_filename()` - 日期识别

### 4. 语音交互模块
**文件**: `modules/voice.py`

**核心功能**:
- 录音组件美化
- 实时音频可视化
- 语音识别集成
- 语音指令处理

**关键函数**:
- `record_audio_to_pcm()` - 录音处理
- `stream_volc_asr()` - 语音识别
- `audio_visualization()` - 音频可视化

### 5. 数据可视化模块
**文件**: `modules/analytics.py`

**核心功能**:
- 工作量统计图表
- 任务完成率趋势
- 时间分布热力图
- 标签使用频率
- 周报自动生成

**关键函数**:
- `generate_workload_chart()` - 工作量统计
- `create_progress_visualization()` - 进度可视化
- `generate_weekly_report()` - 周报生成

### 6. 日历视图模块
**文件**: `modules/calendar.py`

**核心功能**:
- 月/周/日视图切换
- 任务事件展示
- 快速任务创建
- 悬停预览
- 拖拽调整日期

**关键函数**:
- `render_calendar()` - 日历渲染
- `handle_calendar_events()` - 事件处理
- `quick_add_task()` - 快速添加

### 7. 导出与归档模块
**文件**: `modules/exporter.py`

**核心功能**:
- Markdown格式导出
- Word文档导出
- 批量归档功能
- 自定义模板

**关键函数**:
- `build_record_exports()` - 单记录导出
- `get_archive_exports()` - 批量导出
- `build_record_docx_bytes()` - Word文档生成

## 数据库设计

### 主表结构
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,              -- 任务日期
    task_name TEXT,         -- 任务名称
    category TEXT,          -- 类别(科研/临床/课程/其他)
    is_done INTEGER,        -- 完成状态
    details TEXT,           -- 实验记录详情
    tags TEXT,              -- 标签
    created_at TIMESTAMP,   -- 创建时间
    updated_at TIMESTAMP    -- 更新时间
);
```

### 索引设计
- `idx_date` - 日期索引，优化日历查询
- `idx_category` - 类别索引，优化分类筛选
- `idx_tags` - 标签索引，优化搜索

## 用户界面设计

### 布局结构
```
┌─────────────────────────────────────────────┐
│  侧边栏 (Sidebar)                          │
│  - Logo和标题                              │
│  - 导航菜单                                │
│  - AI助手面板                              │
│  - 快速操作                                │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  主内容区 (Main Content)                   │
│  - 日历视图 / 列表视图                     │
│  - 任务展示                                │
│  - 搜索和筛选                              │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  详情面板 (Detail Panel)                   │
│  - 任务详情                                │
│  - 统计信息                                │
│  - 导出选项                                │
└─────────────────────────────────────────────┘
```

### 页面结构
1. **日历总览页** - 主要工作界面
2. **科研归档页** - 历史记录管理
3. **数据分析页** - 可视化统计
4. **设置页** - 配置管理

## 文件结构

```
lab_diary_ai/
├── app.py                    # 主应用入口
├── requirements.txt          # 依赖包列表
├── config.py                 # 配置文件
├── database/
│   ├── schema.sql           # 数据库架构
│   └── migrations/          # 数据库迁移脚本
├── modules/
│   ├── __init__.py
│   ├── scheduler.py         # 智能排程模块
│   ├── records.py           # 记录管理模块
│   ├── importer.py          # 数据导入模块
│   ├── voice.py             # 语音交互模块
│   ├── analytics.py         # 数据分析模块
│   ├── calendar.py          # 日历视图模块
│   ├── exporter.py          # 导出模块
│   └── utils.py             # 工具函数
├── static/
│   ├── css/
│   │   └── styles.css       # 自定义样式
│   ├── js/
│   │   └── main.js          # 前端脚本
│   └── images/              # 图片资源
├── uploads/                  # 上传文件存储
├── backups/                  # 数据库备份
└── tests/                    # 测试文件
    ├── test_scheduler.py
    ├── test_importer.py
    └── test_voice.py
```

## 性能优化策略

### 前端优化
- 组件懒加载
- 图片压缩和懒加载
- CSS/JS压缩
- 缓存策略

### 后端优化
- 数据库查询优化
- 连接池管理
- 异步处理
- 缓存机制

### 数据库优化
- 索引优化
- 查询优化
- 定期维护
- 备份策略

## 安全考虑

### 数据安全
- 敏感信息加密
- 访问控制
- 数据备份
- 恢复机制

### 应用安全
- 输入验证
- SQL注入防护
- XSS防护
- CSRF防护

## 测试策略

### 单元测试
- 核心函数测试
- AI功能测试
- 数据库操作测试

### 集成测试
- 端到端测试
- 用户场景测试
- 性能测试

### 兼容性测试
- 浏览器兼容性
- 设备适配性
- 分辨率适配

## 部署方案

### 本地部署
- Streamlit本地运行
- 数据库本地存储
- 文件本地存储

### 云端部署
- Docker容器化
- 云服务部署
- 域名绑定
- HTTPS配置

### 监控与维护
- 日志记录
- 性能监控
- 错误追踪
- 定期维护

## 未来扩展计划

### 功能扩展
- 团队协作功能
- 项目管理集成
- 文献管理集成
- 实验数据可视化

### 技术升级
- 数据库升级
- 前端框架升级
- AI模型升级
- 性能优化

### 生态建设
- 插件系统
- API接口
- 第三方集成
- 开源社区