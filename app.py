# -*- coding: utf-8 -*-
"""OpenMed-NER-SpeciesDetect-ModernClinical-395M WebUI - 生物医学物种实体识别可视化界面"""
import gradio as gr
import json
from typing import Tuple, List, Dict

MODEL_NAME = "OpenMed-NER-SpeciesDetect-ModernClinical-395M"

# 示例数据（演示用）
DEMO_ENTITIES = {
    "Escherichia coli bacteria were found in the water samples.": [
        {"entity": "B-SPECIES", "word": "Escherichia coli", "start": 0, "end": 15, "score": 0.98}
    ],
    "The study included specimens from Homo sapiens and Mus musculus.": [
        {"entity": "B-SPECIES", "word": "Homo sapiens", "start": 35, "end": 48, "score": 0.96},
        {"entity": "B-SPECIES", "word": "Mus musculus", "start": 53, "end": 65, "score": 0.97}
    ],
    "Saccharomyces cerevisiae is commonly used in biotechnology applications.": [
        {"entity": "B-SPECIES", "word": "Saccharomyces cerevisiae", "start": 0, "end": 24, "score": 0.95}
    ]
}

def predict_ner(text: str, aggregation_strategy: str) -> Tuple[str, str]:
    """执行 NER 预测（演示模式）"""
    if not text.strip():
        return "请输入要分析的文本。", json.dumps({
            "status": "等待输入",
            "entities": []
        }, ensure_ascii=False, indent=2)
    
    # 演示模式：检查是否有示例数据
    if text in DEMO_ENTITIES:
        entities = DEMO_ENTITIES[text]
    else:
        # 简单的演示实体识别（基于关键词）
        entities = []
        species_keywords = [
            "Escherichia coli", "Homo sapiens", "Mus musculus", 
            "Saccharomyces cerevisiae", "Dendroaspis polylepis",
            "Canis lupus", "Arabidopsis thaliana", "Drosophila melanogaster"
        ]
        text_lower = text.lower()
        for keyword in species_keywords:
            if keyword.lower() in text_lower:
                idx = text_lower.find(keyword.lower())
                entities.append({
                    "entity": "B-SPECIES",
                    "word": keyword,
                    "start": idx,
                    "end": idx + len(keyword),
                    "score": 0.92
                })
    
    # 生成可视化结果
    if entities:
        highlighted_text = text
        offset = 0
        for entity in sorted(entities, key=lambda x: x["start"], reverse=True):
            start = entity["start"]
            end = entity["end"]
            word = entity["word"]
            score = entity["score"]
            highlighted_text = (
                highlighted_text[:start] + 
                f'<mark style="background-color: #90EE90; padding: 2px 4px; border-radius: 3px;" title="B-SPECIES (置信度: {score:.2%})">{word}</mark>' +
                highlighted_text[end:]
            )
        
        result_html = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h3 style="color: #2c3e50; margin-bottom: 10px;">识别结果</h3>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #28a745;">
                {highlighted_text}
            </div>
            <div style="margin-top: 15px;">
                <h4 style="color: #495057;">识别的实体：</h4>
                <ul style="list-style-type: none; padding: 0;">
        """
        for entity in entities:
            result_html += f"""
                    <li style="padding: 8px; margin: 5px 0; background-color: #e9ecef; border-radius: 3px;">
                        <strong>{entity['word']}</strong> 
                        <span style="color: #6c757d;">({entity['entity']})</span>
                        <span style="float: right; color: #28a745; font-weight: bold;">{entity['score']:.2%}</span>
                    </li>
            """
        result_html += """
                </ul>
            </div>
        </div>
        """
    else:
        result_html = """
        <div style="font-family: Arial, sans-serif; padding: 20px; text-align: center; color: #6c757d;">
            <p>未检测到物种实体。请尝试输入包含物种名称的文本，例如：</p>
            <ul style="text-align: left; display: inline-block;">
                <li>Escherichia coli bacteria were found in the water samples.</li>
                <li>The study included specimens from Homo sapiens and Mus musculus.</li>
                <li>Saccharomyces cerevisiae is commonly used in biotechnology applications.</li>
            </ul>
        </div>
        """
    
    # JSON 输出
    json_output = json.dumps({
        "status": "success",
        "aggregation_strategy": aggregation_strategy,
        "entities": entities,
        "total_entities": len(entities)
    }, ensure_ascii=False, indent=2)
    
    return result_html, json_output

def load_example(example_text: str) -> str:
    """加载示例文本"""
    return example_text

# 创建 Gradio 界面
with gr.Blocks(title=f"{MODEL_NAME} WebUI", theme=gr.themes.Soft()) as demo:
    gr.Markdown(f"""
    # 🧬 {MODEL_NAME} WebUI
    
    **生物医学物种实体识别可视化界面**
    
    本界面提供了 OpenMed-NER-SpeciesDetect-ModernClinical-395M 模型的交互式测试环境。
    该模型专门用于识别和提取生物医学文本中的物种实体（Species Entity）。
    
    ### 🎯 功能特点
    - **高精度识别**：基于 ModernBERT-large 架构，针对生物医学领域优化
    - **实时可视化**：直观展示识别结果，高亮显示识别的实体
    - **详细信息**：提供实体类型、置信度等详细信息
    - **批量处理**：支持单文本和批量文本处理
    
    ### 📊 支持的实体类型
    - **B-SPECIES**: 物种实体开始标记
    - **I-SPECIES**: 物种实体内部标记
    
    **注意**：当前为演示模式，未加载真实模型权重。实际部署时将加载完整模型进行推理。
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            input_text = gr.Textbox(
                label="输入文本",
                placeholder="请输入要分析的生物医学文本，例如：Escherichia coli bacteria were found in the water samples.",
                lines=5,
                value="Escherichia coli bacteria were found in the water samples."
            )
            
            aggregation_strategy = gr.Radio(
                label="聚合策略",
                choices=["simple", "first", "average", "max"],
                value="simple",
                info="定义如何将 token 预测分组为实体"
            )
            
            with gr.Row():
                predict_btn = gr.Button("识别实体", variant="primary", size="lg")
                clear_btn = gr.Button("清空", variant="secondary")
        
        with gr.Column(scale=1):
            gr.Markdown("### 📝 示例文本")
            example1 = gr.Button("示例 1: Escherichia coli", size="sm")
            example2 = gr.Button("示例 2: Homo sapiens", size="sm")
            example3 = gr.Button("示例 3: Saccharomyces cerevisiae", size="sm")
    
    with gr.Row():
        with gr.Column():
            output_html = gr.HTML(label="可视化结果")
            output_json = gr.JSON(label="JSON 输出")
    
    # 示例文本
    example_texts = [
        "Escherichia coli bacteria were found in the water samples.",
        "The study included specimens from Homo sapiens and Mus musculus.",
        "Saccharomyces cerevisiae is commonly used in biotechnology applications."
    ]
    
    # 绑定事件
    predict_btn.click(
        fn=predict_ner,
        inputs=[input_text, aggregation_strategy],
        outputs=[output_html, output_json]
    )
    
    example1.click(
        fn=lambda: example_texts[0],
        outputs=input_text
    )
    
    example2.click(
        fn=lambda: example_texts[1],
        outputs=input_text
    )
    
    example3.click(
        fn=lambda: example_texts[2],
        outputs=input_text
    )
    
    clear_btn.click(
        fn=lambda: ("", "", ""),
        outputs=[input_text, output_html, output_json]
    )
    
    # 页面加载时自动运行一次
    demo.load(
        fn=predict_ner,
        inputs=[input_text, aggregation_strategy],
        outputs=[output_html, output_json]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        share=False,
        inbrowser=False
    )
