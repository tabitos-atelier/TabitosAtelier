"""
賢者召喚の呪文 ～Swallow-13B RAGシステム～

この呪文は、130億の言葉を持つ賢者を召喚し、
古文書（rag.txt）の知識を用いて問いに答える、
対話の儀式である。

必要な神器:
- llama-cpp-python (CUDA対応)
- langchain-community
- langchain-huggingface
- sentence-transformers
- faiss-gpu
- gradio

使用法:
    python swallow-13b.py

ブラウザで http://127.0.0.1:7860 にアクセスし、対話を開始する。
"""
import sys
import time
import gradio as gr
from llama_cpp import Llama
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

# ================================================================
# 【第一段階：賢者の召喚と知識の書庫構築】
# ================================================================

print("賢者召喚の儀式を開始します...")
print("- 賢者の本体を読み込んでいます...")

# 賢者（LLMコア）を召喚する
# n_gpu_layers: GPUに委ねる層の数（-1 = 全層をGPUに委ねる, 0 = CPUのみで動作）
# n_ctx: 記憶の器の大きさ（文脈窓）
start_time = time.time()
llm = Llama(
    model_path="tokyotech-llm-Swallow-13b-instruct-v0.1-Q4_K_M.gguf",
    n_gpu_layers=-1,
    n_ctx=4096,
    verbose=True
)
end_time = time.time()

print(f"- 賢者の召喚に成功しました。（ロード時間: {end_time - start_time:.2f} 秒）")
print("- 古文書（rag.txt）から知識を読み込んでいます...")

# 古文書（RAG知識ベース）を読み込む
try:
    with open("rag.txt", "r", encoding="utf-8") as f:
        rag_text = f.read()
except FileNotFoundError:
    print("!! 致命的エラー: rag.txt が見つかりません。")
    sys.exit(1)

# 古文書を段落ごとに分割
texts = rag_text.split("\n\n")

print(f"- 古文書から {len(texts)} 個の知識の欠片を抽出しました。")
print("- 知識の欠片を魔法の文字（ベクトル）に変換しています...")

# テキストをベクトルに変換する埋め込みモデルを召喚
embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-large')

print("- 索引書庫を構築しています...")

# 索引書庫（FAISSベクトルストア）を構築する
vectorstore = FAISS.from_texts(texts, embedding=embeddings)
retriever = vectorstore.as_retriever()

print("- 索引書庫の構築が完了しました。")
print("- 問いかけの作法（プロンプトテンプレート）を定義しています...")

# 問いかけの作法（プロンプトテンプレート）を定義する
template = """
### 指示:
提供されたコンテキスト情報のみを使用して、質問に答えてください。
コンテキストに答えがない場合は、「分かりません」と答えてください。

コンテキスト:
{context}

質問:
{question}

### 応答:
"""
prompt_template = PromptTemplate.from_template(template) 

print("\n準備完了。賢者との対話を開始できます。\n")

# ================================================================
# 【第二段階：対話の関数を定義する】
# ================================================================

def chat_with_sage(question):
    """
    賢者（LLM）とRAG知識の書庫を用いた対話ロジック。
    
    Args:
        question (str): 旅人からの問いかけ
        
    Returns:
        str: 賢者からの応答（推論時間を含む）
    """
    if not question.strip():
        return (
            "--- 賢者の応答 ---\n"
            "問いかけがありません。何かお尋ねください。\n"
            "------------------------------------------\n"
            "(推論時間: 0.00 秒)"
        )

    # 【計測開始】推論の開始時間
    inference_start_time = time.time()

    # 1. 索引書庫から関連する知識を検索
    retrieved_docs = retriever.invoke(question) 
    context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # 2. プロンプトを組み立てる
    final_prompt = prompt_template.format(context=context_text, question=question)

    # 3. 賢者（LLM）への問いかけ
    response = llm(
        final_prompt,
        max_tokens=512,  # 応答の最大長さ
        stop=["###", "ユーザー:", "質問:", "コンテキスト:", "\n\n"],  # 停止条件
        echo=False,  # プロンプトを応答に含めない
        stream=False,  # ストリーミングなし
    )

    # 【計測終了】推論の終了時間
    inference_end_time = time.time()
    
    # 応答テキストを抽出
    result_text = response['choices'][0]['text'].strip()
    
    return (
        "--- 賢者の応答 ---\n"
        f"{result_text}\n"
        "------------------------------------------\n"
        f"(推論時間: {inference_end_time - inference_start_time:.2f} 秒)"
    )

# ================================================================
# 【第三段階：水晶玉（Gradio UI）を創造し、対話の場を開く】
# ================================================================

with gr.Blocks(title="賢者召喚の水晶玉 - Swallow-13B RAG対話システム", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown(
        """
        # 賢者召喚の水晶玉 ～ Swallow-13B RAG対話システム ～
        
        130億の言葉を持つ賢者との対話をお楽しみください。
        賢者は古文書（rag.txt）の知識を用いて、あなたの問いに答えます。
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            input_textbox = gr.Textbox(
                label="旅人からの問いかけ",
                lines=5,
                placeholder="賢者への問いかけを入力してください...",
            )
            
            with gr.Row():
                clear_btn = gr.Button("クリア", variant="secondary")
                submit_btn = gr.Button("質問", variant="primary")

        with gr.Column(scale=1):
            output_textbox = gr.Textbox(
                label="賢者の応答",
                lines=10, 
                placeholder="(賢者の言葉がここに現れます)", 
                interactive=False 
            )

    # 問いかけボタンの制御ロジック
    submit_btn.click(
        # 1. 最初に実行: 問いかけボタンを無効化（思考中）
        fn=lambda: gr.update(interactive=False),
        inputs=None,
        outputs=[submit_btn],
        queue=False 
    ).then(
        # 2. 次に実行: 対話ロジックの実行
        fn=chat_with_sage,
        inputs=[input_textbox],
        outputs=[output_textbox]
    ).then(
        # 3. 最後に実行: 問いかけボタンを有効化（思考完了）
        fn=lambda: gr.update(interactive=True),
        inputs=None,
        outputs=[submit_btn],
        queue=False
    )
    
    # 清めるボタンの機能
    clear_btn.click(
        fn=lambda: (gr.update(value=""), gr.update(value="")),
        inputs=None,
        outputs=[input_textbox, output_textbox]
    )

# 水晶玉を開き、対話の場を設ける
demo.launch(share=False, server_name="127.0.0.1")