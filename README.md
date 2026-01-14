# ChatPPT

ChatPPT 是一个基于 AI Agent 工作流的 PPT 自动生成系统。它能够接收文本、语音或文档输入，并通过智能工作流自动生成结构化的大纲、扩写幻灯片内容、建议配图，并最终渲染为可下载的 .pptx 文件。

## 核心特性

- **多模态输入**: 支持文本、语音（Whisper）及 Word 文档解析。
- **Agent 工作流**: 基于 LangGraph 的有向无环图架构，支持状态持久化与人工干预（Human-in-the-Loop）。
- **智能内容生成**: 自动生成逻辑严谨的 PPT 大纲与幻灯片详情。
- **智能视觉决策**: 基于 Tool 的 Agent 自主决定搜索真实照片或生成创意图片（支持阿里云通义万相）。
- **专业级渲染**: 导出符合 PowerPoint 标准的 .pptx 文件。

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
python src/ui/gradio_app.py
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
- `BING_SEARCH_API_KEY`: Bing 图片搜索 API Key（可选）

#### 4. 运行应用

**启动 Web UI（推荐）：**
```bash
python src/ui/gradio_app.py
```

**或运行命令行测试：**
```bash
python app.py
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
└── README.md
```

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
