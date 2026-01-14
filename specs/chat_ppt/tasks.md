# 实施计划 - ChatPPT

## 第一阶段：环境与基础结构 (DONE)
- [x] 1. 初始化项目文档 (`requirements.md`, `design.md`, `tasks.md`) _需求: 0_
- [x] 2. 创建目录结构 (`src/`, `data/`, `tests/`) _需求: 0_
- [x] 3. 编写基础配置文件 (`README.md`, `.env.example`, `requirements.txt`) _需求: 0_

## 第二阶段：LangGraph 核心流转与状态管理 (DONE)
- [x] 4. 定义全局状态 `PPTState` (_需求: 2_)
- [x] 5. 实现 `Content Planner` 基础大纲生成节点 (_需求: 2_)
- [x] 6. 实现 Gradio 交互界面，支持大纲预览与修改 (HITL 1) (_需求: 2_)
- [x] 7. 实现 `Content Generator` 幻灯片文案生成节点 (_需求: 2_)
- [x] 8. 实现文案与配图建议的二次编辑 (HITL 2) (_需求: 2_)

## 第三阶段：多模态输入与配图建议 (DONE)
- [x] 8. 集成 Whisper API 实现语音转录 (_需求: 1_)
- [x] 9. 实现 Docx 文档解析器 (_需求: 1_)
- [x] 10. 实现 `Image Advisor` 搜索关键词生成节点 (_需求: 3_)
- [x] 11. 实现图片检索或生成逻辑 (_需求: 3_)

## 第四阶段：PPT 渲染导出 (DONE)
- [x] 12. 实现 `Layout Manager` 版式匹配逻辑 (_需求: 4_)
- [x] 13. 实现 `PPT Generator` 基于 `python-pptx` 的渲染引擎 (_需求: 4_)
- [x] 14. 端到端测试与优化 (_需求: 1-4_)
