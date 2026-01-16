import gradio as gr
import json
import uuid
from src.workflow.graph import app
from src.models.state import PPTOutline, SlideContent
from src.utils.logger import logger
from src.utils.docx_parser import DocxParser
from src.utils.whisper_asr import WhisperASR

def process_input(input_text, upload_file):
    """处理混合输入"""
    final_text = input_text or ""
    if upload_file is not None:
        file_path = upload_file.name
        if file_path.endswith(".docx"):
            final_text = f"{final_text}\n\n参考文档内容：\n{DocxParser.parse(file_path)}"
        elif file_path.endswith((".mp3", ".wav", ".m4a", ".flac")):
            final_text = f"{final_text}\n\n语音转录内容：\n{WhisperASR.transcribe(file_path)}"
    return final_text

def start_workflow(input_text, upload_file):
    """启动工作流并运行到第一个中断点 (Planner)"""
    combined_text = process_input(input_text, upload_file)
    if not combined_text.strip():
        return gr.update(visible=False), "请输入需求", ""
    
    # 为当前会话生成唯一的 thread_id
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    logger.info(f"UI: Starting new workflow session: {thread_id}")
    
    initial_state = {
        "input_text": combined_text,
        "input_files": [],
        "outline": None,
        "slides": [],
        "current_step": "start",
        "is_approved": False,
        "error": None,
        "generated_file": None
    }
    
    try:
        # 运行工作流，它会在 planner 之后中断
        app.invoke(initial_state, config=config)
        
        # 获取中断后的状态
        state = app.get_state(config).values
        outline = state.get("outline")
        
        if outline:
            outline_str = f"标题: {outline.title}\n" + "\n".join([f"- {c}" for c in outline.chapters])
            return gr.update(visible=True), outline_str, thread_id
        return gr.update(visible=False), "未能生成大纲", thread_id
    except Exception as e:
        logger.exception("UI Error in start_workflow")
        return gr.update(visible=False), f"系统异常: {str(e)}", ""

def resume_to_details(thread_id, outline_text):
    """从大纲中断点恢复，运行到第二个中断点 (Image Advisor)"""
    if not thread_id: return gr.update(visible=False), "无效的会话"
    
    config = {"configurable": {"thread_id": thread_id}}
    logger.info(f"UI: Resuming session {thread_id} to details...")
    
    try:
        # 1. 解析人工修改后的大纲并更新状态
        lines = outline_text.strip().split("\n")
        title = lines[0].replace("标题: ", "").strip()
        chapters = [line.replace("- ", "").strip() for line in lines[1:] if line.strip()]
        new_outline = PPTOutline(title=title, chapters=chapters)
        
        # 更新状态：覆盖 outline 并标记已批准
        app.update_state(config, {"outline": new_outline, "is_approved": True}, as_node="planner")
        
        # 2. 继续运行，它会在 image_advisor 之后中断
        app.invoke(None, config=config)
        
        # 3. 获取最新状态
        state = app.get_state(config).values
        slides = state.get("slides", [])
        slides_json = json.dumps([s.dict() for s in slides], indent=2, ensure_ascii=False)
        
        return gr.update(visible=True), slides_json
    except Exception as e:
        logger.exception("UI Error in resume_to_details")
        return gr.update(visible=False), f"生成详情异常: {str(e)}"

def resume_to_render(thread_id, slides_json):
    """从详情中断点恢复，完成最终渲染"""
    if not thread_id: return "无效的会话", None
    
    config = {"configurable": {"thread_id": thread_id}}
    logger.info(f"UI: Finalizing session {thread_id}...")
    
    try:
        # 1. 解析人工修改后的详情并更新状态
        slides_data = json.loads(slides_json)
        updated_slides = [SlideContent(**s) for s in slides_data]
        
        app.update_state(config, {"slides": updated_slides}, as_node="image_advisor")
        
        # 2. 继续运行直到结束 (现在会经过 visual_agent 节点)
        app.invoke(None, config=config)
        
        # 3. 获取结果
        state = app.get_state(config).values
        outline = state.get("outline")
        slides = state.get("slides", [])
        file_path = state.get("generated_file")

        logger.info(f"UI: Final state - outline: {outline.title if outline else 'None'}, slides: {len(slides)}, file: {file_path}")

        slides_md = ""
        slide_number = 1

        # 添加标题页预览
        if outline and outline.title:
            slides_md += f"### Slide {slide_number}: {outline.title} (标题页)\n"
            slides_md += f"**演示文稿标题页**\n\n"
            slides_md += f"**章节大纲:**\n"
            for chapter in outline.chapters:
                slides_md += f"- {chapter}\n"
            slides_md += f"\n---\n\n"
            slide_number += 1

        # 添加内容页预览
        for slide in slides:
            slides_md += f"### Slide {slide_number}: {slide.title}\n"
            for point in slide.bullet_points: slides_md += f"- {point}\n"
            if slide.image_path: slides_md += f"\n![Image]({slide.image_path})\n"
            slides_md += f"\n**视觉建议:** `{slide.image_query}` | **版式:** `{slide.layout_type}`\n\n---\n\n"
            slide_number += 1
            
        return slides_md, file_path
    except Exception as e:
        logger.exception("UI Error in resume_to_render")
        return f"渲染异常: {str(e)}", None

def create_ui():
    with gr.Blocks(title="ChatPPT - AI Agent (HITL & Persistence)") as demo:
        gr.Markdown("# 🚀 ChatPPT: 极致持久化工作流")
        
        # 隐藏的 State 用于保存 thread_id
        thread_id_state = gr.State("")
        
        with gr.Row():
            with gr.Column(scale=1):
                input_text = gr.Textbox(label="1. 输入您的 PPT 需求", placeholder="例如：人工智能在医疗领域的应用现状...", lines=3)
                upload_file = gr.File(label="或者上传参考资料 (Word 或 音频)", file_types=[".docx", ".mp3", ".wav", ".m4a", ".flac"])
                start_btn = gr.Button("开始流程 (生成大纲)", variant="primary")
                
                with gr.Group(visible=False) as outline_group:
                    gr.Markdown("### 2. 编辑大纲 (断点 1)")
                    outline_editor = gr.TextArea(label="修改标题或章节顺序", lines=8)
                    details_btn = gr.Button("继续生成文案详情", variant="primary")
                
                with gr.Group(visible=False) as details_group:
                    gr.Markdown("### 3. 编辑详情 (断点 2)")
                    details_editor = gr.Code(label="编辑文案、配图建议或版式 (JSON)", language="json", lines=15)
                    render_btn = gr.Button("完成最终渲染", variant="secondary")

            with gr.Column(scale=1):
                gr.Markdown("### 4. 最终成品预览")
                download_output = gr.File(label="下载生成的 PPT 文件")
                slides_output = gr.Markdown(label="预览内容", value="等待渲染完成后生成...")
                session_info = gr.Label(label="当前会话 ID (Thread ID)")
        
        # 交互逻辑：使用 thread_id 实现断点续传
        start_btn.click(
            fn=start_workflow, 
            inputs=[input_text, upload_file], 
            outputs=[outline_group, outline_editor, thread_id_state]
        ).then(fn=lambda x: x, inputs=[thread_id_state], outputs=[session_info])
        
        details_btn.click(
            fn=resume_to_details, 
            inputs=[thread_id_state, outline_editor], 
            outputs=[details_group, details_editor]
        )
        
        render_btn.click(
            fn=resume_to_render, 
            inputs=[thread_id_state, details_editor], 
            outputs=[slides_output, download_output]
        )
        
    return demo

def launch_ui():
    """启动 UI（用于 main.py 调用）"""
    import os
    # 禁用代理对 localhost 的影响
    os.environ['no_proxy'] = '127.0.0.1,localhost'

    demo = create_ui()
    demo.launch(
        theme=gr.themes.Soft(),
        server_name="0.0.0.0",  # 绑定到所有接口
        server_port=7861,  # 换个端口
        show_error=True,
        share=False,
        enable_monitoring=False,
        app_kwargs={
            "timeout": 120,
            "proxy_headers": False
        }
    )

if __name__ == "__main__":
    # 如果直接运行此文件，则启动 UI
    import gradio as gr
    launch_ui()
