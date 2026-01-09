# Lab Diary AI - 智能实验记录管理工具

一个专为科研人员设计的智能实验记录管理工具，结合AI技术提升科研效率，同时保持原始记录的完整性和准确性。

## ✨ 核心特性

### 🤖 AI智能助手
- **自然语言解析**: 用日常语言描述计划，AI自动生成结构化任务
- **智能元数据提取**: AI只提取日期、任务名、标签等元数据，保留原始记录内容
- **语音输入**: 支持语音转文字，解放双手
- **智能润色**: AI辅助润色实验记录，提升学术表达

### 📅 智能日程管理
- **日历视图**: 月/周/日多视图切换，直观展示任务安排
- **任务分类**: 科研/临床/课程/其他分类管理
- **状态追踪**: 任务完成状态和记录填写状态可视化
- **快速操作**: 点击日期快速创建任务，悬停预览详情

### 🪄 历史记录迁移
- **保护原始内容**: 一字不改地导入历史记录，AI只提取元数据
- **多格式支持**: 支持 Markdown、Word、TXT、CSV 等常见格式
- **批量导入**: 支持多文件批量导入，提供预览确认
- **智能识别**: 自动识别文件名中的日期信息

### 📊 数据分析可视化
- **工作量统计**: 每日任务数量趋势图
- **类别分布**: 任务类别饼图分析
- **标签云**: 常用标签统计和可视化
- **周报生成**: AI自动生成科研周报

### 🎤 语音交互
- **语音识别**: 集成火山引擎ASR，高精度中文语音识别
- **实时转写**: 语音实时转文字，支持编辑修正
- **语音指令**: 支持语音添加任务、搜索等操作

### 📤 导出与归档
- **多格式导出**: 支持 Markdown、Word 格式导出
- **批量归档**: 批量导出多个记录为归档文件
- **自定义模板**: 灵活的导出格式配置

## 🚀 快速开始

### 本地运行

#### 0. 运行入口
- 推荐入口：`app.py`（内部调用 `lab_diary_optimized.py` 的 `main()`）
- 也可以直接运行：`streamlit run lab_diary_optimized.py`

#### 1. 安装依赖
```bash
pip install -r requirements.txt
```

#### 2. 配置密钥（可选）
本项目会优先从 `Streamlit secrets` 读取，其次读取环境变量；本地开发推荐使用 `.env`：

```bash
copy .env.example .env
```

然后在 `.env` 里填写（至少需要 `DEEPSEEK_API_KEY` 才能使用 AI 功能）。

#### 3. 运行应用
```bash
streamlit run app.py
```

#### 4. 访问应用
打开浏览器访问: http://localhost:8501

#### 5. 一键启动（Windows）
- PowerShell：运行 `run_local.ps1`
- CMD：运行 `run_local.bat`

### Docker部署

#### 1. 使用Docker Compose
```bash
docker-compose up -d
```

#### 2. 访问应用
打开浏览器访问: http://localhost:8501

### 云端部署

支持多种云平台部署：
- **Streamlit Cloud** (推荐 - 免费)
- **Render.com**
- **Railway.app**
- **Heroku**

> 如果你希望“用户用邮箱登录后才能访问”，可优先用 Streamlit Cloud 的访问控制（在管理页开启 Require sign-in/Private app 并添加允许访问的邮箱）。
> 另：云平台的本地文件通常不保证持久化；若要长期、多用户使用，建议自托管挂载数据卷或接入外部数据库。
>
> 多用户数据隔离：本项目会在检测到登录邮箱后，把每个用户的数据保存到独立目录（`data/users/<hash>/`）；可在 Secrets/环境变量里设置 `LAB_DIARY_REQUIRE_SIGNIN=1` 强制要求登录（本地可用 `LAB_DIARY_USER_EMAIL=you@example.com` 模拟）。

详细部署步骤请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

## 📖 使用指南

### 创建任务

#### 方法1: 日历点击创建
1. 在日历视图中点击任意日期
2. 填写任务名称、类型、标签
3. 点击"添加"完成任务创建

#### 方法2: AI智能创建
1. 在侧边栏的AI助手面板中
2. 用自然语言描述您的计划（如："明天开始做CUMS模型，连续3天"）
3. 点击"生成任务预览"
4. 确认AI生成的任务列表
5. 一键导入到日程中

#### 方法3: 语音创建
1. 点击语音输入按钮
2. 用语音描述您的计划
3. 系统自动识别并转换为文字
4. 确认后生成任务

### 填写实验记录

#### 方法1: 从任务列表进入
1. 在任务列表中找到需要填写记录的任务
2. 点击"记录"按钮
3. 在编辑器中填写实验记录
4. 支持语音输入、AI润色、附件上传
5. 点击"保存记录"

#### 方法2: 从日历进入
1. 在日历中点击有记录标记的任务
2. 在弹出的任务详情中点击"编辑实验记录"
3. 填写并保存记录

### 导入历史记录

1. 进入"科研归档"页面
2. 展开"一键迁移历史记录"面板
3. 选择要导入的文件（支持多选）
4. 设置导入参数：
   - 导入后类别
   - 统一标签
   - 默认日期
   - 是否使用AI提取元数据
5. 点击"开始迁移"
6. 预览导入结果并确认

### 生成周报

1. 在"科研归档"页面
2. 展开"自动生成周报"面板
3. 选择参考日期（默认今天）
4. 点击"生成周报"
5. AI会自动整理近7天的实验记录
6. 可编辑和导出为Markdown格式

### 数据分析

1. 切换到"数据分析"页面
2. 查看总体统计信息
3. 查看工作量趋势图
4. 查看任务类别分布
5. 查看标签使用统计
6. 导出CSV格式的数据报告

## 🛠️ 技术架构

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

## 🔧 配置选项

### AI服务配置
推荐使用环境变量或 Streamlit secrets（避免把密钥写进代码）：

- 环境变量（或 `.env`）：`DEEPSEEK_API_KEY`、`DEEPSEEK_BASE_URL`、`DEEPSEEK_MODEL`、`VOLC_ASR_APP_KEY`、`VOLC_ASR_ACCESS_KEY`
- Streamlit secrets：复制 `.streamlit/secrets.toml.example` 为 `.streamlit/secrets.toml` 并填写

```python
# DeepSeek API配置
DEEPSEEK_API_KEY = "your-api-key"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# 火山引擎ASR配置
VOLC_ASR_APP_KEY = "your-app-key"
VOLC_ASR_ACCESS_KEY = "your-access-key"
```

### 外观定制
在`COLORS`字典中修改配色方案：

```python
COLORS = {
    'primary': '#1e293b',      # 主色
    'secondary': '#334155',    # 辅助色
    'accent': '#3b82f6',       # 强调色
    # ... 更多颜色配置
}
```

## 📱 响应式设计

应用支持多种设备：

### 桌面端 (>1200px)
- 三栏布局（侧边栏 + 主内容 + 详情栏）
- 完整功能展示
- 优化的键盘操作

### 平板端 (768px-1200px)
- 两栏布局（侧边栏 + 主内容）
- 触摸友好的交互
- 简化的详情面板

### 移动端 (<768px)
- 单栏布局
- 底部导航栏
- 手势操作支持
- 优化的触摸体验

## 🔐 安全考虑

### 数据安全
- 本地数据库存储，无需网络连接
- 敏感信息加密存储
- 定期自动备份
- 数据导出和迁移支持

### 应用安全
- 输入验证和清理
- SQL注入防护
- XSS攻击防护
- 文件上传安全检查

## 🚀 性能优化

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

## 🌐 浏览器兼容性

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ⚠️ IE 不支持

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交Issue和Pull Request！

### 开发环境设置

1. Fork本项目
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个Pull Request

### 开发指南

#### 代码风格
- 使用Black进行代码格式化
- 遵循PEP 8规范
- 添加类型注解

#### 测试
- 编写单元测试
- 运行集成测试
- 确保所有测试通过

#### 文档
- 更新README.md
- 添加代码注释
- 更新API文档

## 🙏 致谢

- **Streamlit** - 优秀的Web应用框架
- **DeepSeek** - 强大的AI模型支持
- **火山引擎** - 高质量的语音识别服务
- **开源社区** - 所有贡献者和用户

## 📞 支持与联系

### 问题反馈
- 📧 Email: your-email@example.com
- 🐛 Issue: [GitHub Issues](https://github.com/yourusername/lab-diary-ai/issues)
- 💬 Discussion: [GitHub Discussions](https://github.com/yourusername/lab-diary-ai/discussions)

### 更新日志
查看 [CHANGELOG.md](CHANGELOG.md) 了解最新更新。

---

<div align="center">
  <p>
    <b>Lab Diary AI</b> - 让科研记录更智能、更高效
  </p>
  <p>
    ⭐ 如果这个项目对您有帮助，请给个Star！
  </p>
</div>
