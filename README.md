# ChatPPT

ChatPPT 是一个基于 AI Agent 工作流的 PPT 自动生成系统。它能够接收文本、语音或文档输入，并通过智能工作流自动生成结构化的大纲、扩写幻灯片内容、建议配图，并最终渲染为可下载的 .pptx 文件。

## 核心特性

- **多模态输入**: 支持文本、语音（Whisper）及 Word 文档解析。
- **Agent 工作流**: 基于 LangGraph 的有向无环图架构，支持状态持久化与人工干预（Human-in-the-Loop）。
- **智能内容生成**: 自动生成逻辑严谨的 PPT 大纲与幻灯片详情。
- **AI 图片生成**: 直接使用阿里云通义万相生成创意图片，无需依赖搜索引擎。
- **专业级渲染**: 导出符合 PowerPoint 标准的 .pptx 文件。
- **LangSmith 监控**: 集成 LangSmith 进行 LLM 应用监控、调试和性能分析。

## 环境要求

- Python 3.10+
- pip 或 uv（推荐）

## 快速开始

### 方式一：使用初始化脚本（推荐）

```bash
# 一键初始化环境并安装依赖
./init_env.sh

# 激活虚拟环境
source venv/bin/activate

# 配置环境变量
cp env.example .env
# 编辑 .env 文件，填入你的 API Key

# 启动 UI
./start.sh          # 推荐：自动检查环境并启动
python main.py ui   # 或直接启动 UI
```

### 方式二：手动安装

#### 1. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
.\venv\Scripts\activate    # Windows
```

#### 2. 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. 配置环境变量

复制 `env.example` 为 `.env` 并填写相关 API Key（支持阿里云 DashScope 及针对不同 Node 的模型配置）。

```bash
cp env.example .env
```

**必需配置项：**
- `LLM_API_KEY`: 阿里云 DashScope API Key
- `LLM_API_BASE`: 默认为 `https://dashscope.aliyuncs.com/compatible-mode/v1`

**可选配置项：**
- `PLANNER_MODEL`: 大纲生成节点模型（默认：qwen-max）
- `GENERATOR_MODEL`: 内容生成节点模型（默认：qwen-plus）
- `IMAGE_ADVISOR_MODEL`: 配图建议节点模型（默认：qwen-turbo）
- `IMAGE_GEN_MODEL`: 图像生成模型（默认：wanx-v1）

**图片搜索配置：**
- `ENABLE_IMAGE_SEARCH_ENGINES`: 是否启用搜索引擎（默认 false，使用AI生成图片）
- `UNSPLASH_ACCESS_KEY`: Unsplash API Access Key（仅在启用搜索引擎时需要）
- `UNSPLASH_SECRET_KEY`: Unsplash API Secret Key（可选，用于 OAuth 应用）
- `BING_SEARCH_API_KEY`: Bing 图片搜索 API Key（仅在启用搜索引擎时需要）

**LangSmith 监控配置：**
- `LANGSMITH_API_KEY`: LangSmith API Key（可选，用于监控和调试）
- `LANGSMITH_PROJECT`: 项目名称（可选，默认 'chatppt-monitoring'）
- `LANGSMITH_ENDPOINT`: LangSmith 端点（可选，默认官方端点）

**Unsplash API 认证说明：**
- **Public Authentication**: 只需 Access Key，适合大多数应用（每月 5000 次请求）
- **Confidential Applications**: 需要 Access Key + Secret Key，用于服务器端应用（更高限制）
- **当前实现**: 使用 Public Authentication，Secret Key 支持已预留

**图片搜索策略：**
系统按以下优先级搜索图片：
1. **Unsplash API** (完全免费，无需配置)
2. **Bing Search API** (需要 API Key)
3. **占位图** (兜底方案)

#### 4. 运行应用

**启动 Web UI（推荐）：**
```bash
python main.py ui
```

**如果遇到代理相关错误：**
```bash
./start_without_proxy.sh  # 临时禁用代理启动
```

> **注意**: 如果你设置了系统代理（如 `http_proxy`, `https_proxy`），可能会影响 Gradio 的本地访问。启动脚本会自动处理这个问题。

**或运行命令行测试：**
```bash
python main.py test
```

## 项目结构

```
ppt-agent/
├── src/
│   ├── models/          # 数据模型定义
│   ├── nodes/           # LangGraph 节点（Planner, Generator, Visual Agent）
│   ├── prompts/         # 各节点的 Prompt 文件（RoleTaskFormat）
│   ├── ui/              # Gradio 交互界面
│   ├── utils/           # 工具类（LLM Factory, Image Searcher, PPT Generator）
│   └── workflow/        # LangGraph 工作流定义
├── specs/               # 需求文档与技术方案
├── data/                # 数据存储目录（输出文件）
├── tests/               # 测试文件
├── env.example          # 环境变量模板
├── requirements.txt     # Python 依赖
├── main.py              # 主入口脚本
├── start.sh             # 快速启动脚本
└── README.md
```

## LangSmith 监控集成

ChatPPT 已集成 LangSmith 进行 LLM 应用的监控和调试。当配置了相关环境变量后，系统会自动启用 LangSmith tracing。

### 配置步骤

1. **注册 LangSmith 账户**
   - 访问 [LangSmith](https://smith.langchain.com/)
   - 创建账户并获取 API Key

2. **配置环境变量**
   ```bash
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   LANGSMITH_PROJECT=chatppt-monitoring
   ```

3. **重启应用**
   - LangSmith tracing 将在应用启动时自动启用

### 监控功能

- **实时追踪**: 监控每个 LLM 调用的输入、输出和元数据
- **性能分析**: 查看 token 使用量、响应时间等指标
- **错误调试**: 快速定位和诊断问题
- **历史记录**: 保存所有交互记录用于分析

## 工作流说明

1. **输入处理**: 支持文本、Word 文档或语音输入（Whisper ASR）
2. **大纲生成** (HITL 1): 生成 PPT 大纲，支持人工编辑
3. **内容生成**: 根据大纲扩写每页幻灯片的详细文案
4. **配图建议** (HITL 2): 优化配图关键词，支持人工调整
5. **智能视觉决策**: Agent 自主决定搜索真实照片或生成创意图片
6. **PPT 渲染**: 生成最终的 .pptx 文件

## 技术文档

- [需求文档](specs/chat_ppt/requirements.md)
- [技术方案设计](specs/chat_ppt/design.md)
- [实施计划](specs/chat_ppt/tasks.md)

## 开发说明

### 虚拟环境管理

项目使用 Python 虚拟环境（venv）进行依赖隔离。每次开发前请确保已激活虚拟环境：

```bash
source venv/bin/activate  # macOS/Linux
```

退出虚拟环境：
```bash
deactivate
```

### 依赖更新

如果添加了新的依赖，请更新 `requirements.txt`：

```bash
pip freeze > requirements.txt
```

## 许可证

MIT License
