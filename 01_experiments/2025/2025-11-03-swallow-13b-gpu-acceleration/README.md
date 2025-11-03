# WSL2 + CUDA 13.0 環境構築ガイド ～Swallow-13Bによる環境検証～

## 📜 この設計図について

この設計図は、WSL2 Ubuntu 24.04.1 LTS 環境で、CUDA 13.0環境を構築し、Swallow-13Bで動作検証するための完全ガイドです。

**目的:**
- WSL2 + CUDA 13.0環境の完全構築
- Swallow-13Bによる環境検証（GPU動作確認）
- Mixtral 8x7B実行への準備

**環境:**
- OS: Windows 11 + WSL2 Ubuntu 24.04.1 LTS
- GPU: NVIDIA GeForce RTX 5070 Ti 16GB
- CUDA: 13.0
- Python: 3.12 (Miniforge)

## 🪟 Windows側の準備（必須）

### NVIDIA Studioドライバーの更新

WSL2でCUDAを使用する前に、Windows側のNVIDIAドライバーを最新版に更新する必要があります。

#### 手動ダウンロード方式

1. [NVIDIA Drivers ページ](https://www.nvidia.com/ja-jp/drivers/)にアクセス
2. 製品タイプ: GeForce
3. 製品シリーズ: GeForce RTX 50 Series
4. 製品: GeForce RTX 5070 Ti
5. オペレーティングシステム: Windows 11
6. ドライバータイプ: Studio Driver（推奨）
7. ダウンロード・インストール

#### NVIDIAアプリ方式（推奨）

GeForce Experienceのダウンロードボタンから、NVIDIAアプリ（NVIDIA App）をインストールします。

1. NVIDIAアプリを起動
2. 「ドライバー」タブを選択
3. 「Studio Driver」を選択（AI/ML作業に最適化）
4. 「カスタムインストール」を選択
5. 「クリーンインストール」にチェックを入れる
6. インストール実行

**重要:** クリーンインストールにより、古いドライバーの残骸が完全に削除され、新しいドライバーがクリーンな状態でインストールされます。

#### 確認方法

```bash
# WSL2内で確認
nvidia-smi
# → CUDAバージョンとドライバーバージョンが表示される
```

## 🏜️ 仮想砂漠の準備（WSL2 Ubuntu）

### ROPsの確認

NVIDIA® GeForce RTX™ 5070 Tiには96個のRender Output Units (ROPs)が含まれている。
初期不良の経験から、気になる場合はTechPowerUp GPU-Zで ROPsを確認すること。

### ビルド環境の準備

WSL2 Ubuntu 24.04.1 LTSにビルド環境を準備する。

```bash
# ビルドツール追加
sudo apt-get update
sudo apt-get install -y build-essential cmake
```

## ⚡ GPUの魔力を解き放つ（CUDA 13.0インストール）

AIを動作させるため、CUDA(Compute Unified Device Architecture：クーダ)をインストールする。

```bash
# 1. 既存の古いCUDA関連を削除
sudo apt-get --purge remove "*cuda*" "*cublas*" "*cufft*" "*cufile*" "*curand*" \
  "*cusolver*" "*cusparse*" "*gds-tools*" "*npp*" "*nvjpeg*" "nsight*" "*nvvm*"
sudo apt-get autoremove
sudo apt-get autoclean

# 2. WSL2用CUDAリポジトリ追加
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update

# 3. CUDA 13.0 Toolkitインストール
sudo apt-get -y install cuda-toolkit-13-0

# 4. 環境変数設定
echo 'export PATH=/usr/local/cuda-13.0/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-13.0/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 5. 動作確認
nvcc --version
```

### 確認方法

```bash
# Step 1: GPU認識確認
nvidia-smi
```

サンプルのソースコードを下記のコマンドで作る。

```bash
# Step 2: CUDAサンプル実行
cat << 'EOF' > test_cuda.cu
#include <stdio.h>

__global__ void hello() {
    printf("Hello from GPU!\n");
}

int main() {
    hello<<<1, 1>>>();
    cudaDeviceSynchronize();
    return 0;
}
EOF
```

ビルドし、実行してみよう。`Hello from GPU!`と表示されれば成功だ。

```bash
nvcc test_cuda.cu -o test_cuda
./test_cuda
```

デバイス情報を確認してみよう。

```bash
# Step 3: デバイス情報確認
cat << 'EOF' > device_info.cu
#include <stdio.h>

int main() {
    int deviceCount;
    cudaGetDeviceCount(&deviceCount);
    
    printf("CUDA Devices: %d\n", deviceCount);
    
    for(int i = 0; i < deviceCount; i++) {
        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, i);
        printf("Device %d: %s\n", i, prop.name);
        printf("  Compute Capability: %d.%d\n", prop.major, prop.minor);
    }
    return 0;
}
EOF
```

ビルド後、実行し、`NVIDIA GeForce RTX 5070 Ti`が表示されれば成功だ。

```bash
nvcc device_info.cu -o device_info
./device_info
```

## 🐍 Python環境の創造

### uvの召喚（高速パッケージ管理神器）

pipの代わりにuvを使用する。先頭にuvを付けるだけ。

```bash
# uv（高速 Python パッケージインストーラー）をインストール
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Miniforge環境の準備（推奨）

Miniforgeは、conda-forgeチャンネルをデフォルトで利用し、Mambaパッケージマネージャーを含む軽量なディストリビューションです。これにより、Anaconda社の商用ライセンス制限を回避し、高速なパッケージ管理が可能になります。

```bash
# Miniforge (Mambaforge) インストーラーをダウンロード
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh
```

シェル実行後の入力は下記の通り。後は、Enterキーのみ。

```bash
# ライセンス同意
Do you accept the license terms? [yes|no]
>>> yes
```

Miniforge有効化

```bash
source ~/miniforge3/bin/activate
```

### Python環境の作成

安定動作しそうな、Python 3.12をインストールする。

```bash
# mamba を使用して環境を作成（Miniforge/Mambaforgeでは最初から mamba が使える）
mamba create -n ai_env python=3.12 -y
```

ai_envをアクティベートする。

```bash
eval "$(mamba shell hook --shell bash)"
mamba activate ai_env
```

### AIライブラリのインストール

ai_env環境がアクティブな状態で実行する。

#### 【重要】llama-cpp-pythonはソースビルド必須

llama-cpp-pythonは、mambaでインストールせず、uvで必ずソースからビルドすること。

**理由:**
- プリビルド版は汎用的に作られており、特定のGPUに最適化されていない
- ソースビルドにより、RTX 5070 Ti（Compute Capability 12.0）に完全最適化
- 実測で約14倍の性能差（詳細は「性能測定結果」セクション参照）

**推奨:** 以下の手順に従い、必ずuv(or pip)でソースビルドを実行する。

#### インストール手順

```bash
# ⚠️ 注意: ai_env 環境がアクティブな状態で実行

# ⚠️ 最重要: NumPy 1.x系を最初にインストール（依存関係を先に固定）
mamba install -y "numpy>=1.20,<2.0"

# コンパイラのインストール
mamba install -y gxx_linux-64

# 科学計算ライブラリ（NumPy 1.x環境でインストール）
mamba install -y scipy scikit-learn

# GPU用をインストール（NumPy 1.x環境で）
mamba install -y faiss-gpu

# PyTorchのインストール
mamba install -y pytorch torchvision torchaudio

# ⚠️ 重要: llama-cpp-python は uv で CUDA 対応版をソースからビルドインストール
cat > /tmp/constraints.txt << 'EOF'
numpy>=1.20,<2.0
EOF

CMAKE_ARGS="-DGGML_CUDA=on" uv pip install llama-cpp-python --force-reinstall --no-cache-dir --constraint /tmp/constraints.txt

# データ効率化
mamba install -y pyarrow datasets

# 機械学習モデルのハブ
mamba install -y huggingface_hub

# LLMアプリケーション開発
mamba install -y langchain-community langchain-huggingface sentence-transformers

# デモ/UI構築
mamba install -y gradio
```

インストール後、下記の確認を行う。

```bash
# 最終確認
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import faiss; print('faiss OK')"
python -c "from llama_cpp import Llama; print('llama-cpp-python OK')"
```

現時点の版数例：

```bash
NumPy: 1.26.4
PyTorch: 2.8.0
faiss OK
llama-cpp-python OK
```

## 🤖 環境検証（Swallow-13B）

### モデルのダウンロード

環境が正しく構築されたかを検証するため、Swallow-13B Q4_K_M量子化版をダウンロードします。

```bash
# Swallow-13B Q4_K_M量子化版をダウンロード
wget https://huggingface.co/mmnga/tokyotech-llm-Swallow-13b-instruct-v0.1-gguf/resolve/main/tokyotech-llm-Swallow-13b-instruct-v0.1-Q4_K_M.gguf
```

### RAG知識の準備

`rag.txt`ファイルを作成し、賢者が参照する知識を記載する。

### 実行手順

```bash
# 対話システムの起動
python swallow-13b.py
```

起動後、ターミナルに以下のようなメッセージとURLが表示されます：

```
準備完了。賢者との対話を開始できます。

Running on local URL:  http://127.0.0.1:7860
```

Ctrlキーを押しながらURLをクリックすると、ブラウザでGradio UIが開きます。

**使用方法:**
1. 「旅人からの問いかけ」欄に質問を入力
2. 「質問」ボタンをクリック
3. 約1秒で「賢者の応答」欄に回答が表示される

**推論時間について:**
- GPU使用時: 約1秒（回答の文字数により変動）
- CPU使用時: 約20秒
- プリビルドGPU版: 約10秒

この約27倍の速度差が、ソースビルド版の最大の利点です。

## 🔧 トラブルシューティング

### NumPy 2.x問題

llama-cpp-pythonをpipでインストールすると、NumPyが2.xにアップグレードされ、faissとの互換性問題が発生する。

**解決策:** constraints.txtを使用して、NumPy 1.x系を維持する。

```bash
cat > /tmp/constraints.txt << 'EOF'
numpy>=1.20,<2.0
EOF

CMAKE_ARGS="-DGGML_CUDA=on" uv pip install llama-cpp-python --force-reinstall --no-cache-dir --constraint /tmp/constraints.txt
```

### CUDA未検出問題

llama-cpp-pythonがCUDAを認識しない場合、ソースビルドが正しく行われていない可能性がある。

**確認方法:**

```python
from llama_cpp import Llama
llm = Llama(model_path="tokyotech-llm-Swallow-13b-instruct-v0.1-Q4_K_M.gguf", n_gpu_layers=35)
# GPU layersが正常にロードされるか確認
```

### メモリ不足問題

13Bモデルは約8GB以上のVRAMを必要とする。メモリ不足の場合、`n_gpu_layers`の値を減らす。

```python
llm = Llama(model_path="...", n_gpu_layers=20)  # 値を減らす
```

## 📊 性能測定結果

RTX 5070 Ti 16GB環境での実測値（Swallow-13B Q4_K_M量子化版）：

### 基本性能

- **モデルロード時間:** 約6秒（初回起動時のみ）
- **GPU使用率:** 約80-90%
- **VRAM使用量:** 約8-10GB

### 推論時間（回答の長さに応じて変動）

| 回答の長さ | トークン数 | 推論時間 | 用途例 |
|:---------|:----------|:--------|:------|
| 短文 | 約14-30 tokens | 0.25-0.46秒 | 簡潔な回答 |
| 中文 | 約50 tokens | 0.74秒 | 標準的な回答 |
| 長文 | 約107 tokens | 1.39秒 | 詳細な説明 |

### トークン生成速度

- **平均速度:** 約65-77 tokens/second
- **初回応答:** 約1.67秒（294 tokens、キャッシュなし）
- **2回目以降:** キャッシュヒットにより高速化

### 最適化効果

**prefix-match cache:**
- RAGシステムのコンテキスト（258 tokens）が自動的にキャッシュ
- 2回目以降のprompt評価時間がほぼ0秒に短縮
- 連続した問いかけで大幅な性能向上

### インストール方法別の性能比較

| 方式 | 推論時間（50 tokens） | 相対速度 |
|:-----|:--------------------|:--------|
| CPU版のみ | 約20秒 | 1x |
| mamba install版 | 約10秒 | 2x |
| **ソースビルド版** | **約0.74秒** | **約27x** |

**結論:** ソースビルド版により、CPU版と比較して約27倍の高速化を実現。

## 🎯 次回ログイン時の手順

次回ログイン時は、下記のコマンドを実行し、AI環境に変更する必要がある。

```bash
source ~/miniforge3/bin/activate
eval "$(mamba shell hook --shell bash)"
mamba activate ai_env
```

## 📚 参考資料

- [NVIDIA Drivers ページ](https://www.nvidia.com/ja-jp/drivers/)
- [CUDA Toolkit Documentation](https://docs.nvidia.com/cuda/)
- [llama-cpp-python GitHub](https://github.com/abetlen/llama-cpp-python)
- [Swallow-13B Model](https://huggingface.co/mmnga/tokyotech-llm-Swallow-13b-instruct-v0.1-gguf)
- [LangChain Documentation](https://python.langchain.com/)

## ⚠️ 重要な注意事項

1. **ソースビルドは必須:** プリビルド版は約14倍遅い
2. **NumPy 1.x系維持:** constraints.txtを利用したビルド
3. **CUDA環境変数:** 毎回ログイン時に設定が必要(AI専用なら環境変数に設定)
4. **GPU互換性:** RTX 50シリーズはCompute Capability 12.0以上が必要
5. **環境検証:** Swallow-13Bでの検証後、Mixtral 8x7B実行へ進む

---

**この設計図により、Mixtral 8x7B実行のための完璧な環境が完成する。**