# ChatPPT

ChatPPT 是一个基于 AI Agent 工作流的 PPT 自动生成系统。它能够接收文本、语音或文档输入，并通过智能工作流自动生成结构化的大纲、扩写幻灯片内容、建议配图，并最终渲染为可下载的 .pptx 文件。

## 核心特性

- **多模态输入**: 支持文本、语音（Whisper）及 Word 文档解析。
- **Agent 工作流**: 基于 LangGraph 的有向无环图架构，支持状态持久化与人工干预。
- **智能内容生成**: 自动生成逻辑严谨的 PPT 大纲与幻灯片详情。
- **自动配图建议**: 基于语义搜索相关图片或调用 DALL-E 生成。
- **专业级渲染**: 导出符合 PowerPoint 标准的 .pptx 文件。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `env.example` 为 `.env` 并填写相关 API Key（支持阿里云 DashScope 及针对不同 Node 的模型配置）。

```bash
cp env.example .env
```

### 3. 运行应用

```bash
python app.py
```

## 技术文档

- [需求文档](specs/chat_ppt/requirements.md)
- [技术方案设计](specs/chat_ppt/design.md)
- [实施计划](specs/chat_ppt/tasks.md)
