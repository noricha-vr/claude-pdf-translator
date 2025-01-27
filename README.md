# Claude PDF Translator

PDFファイルを画像に変換し、Claude APIを使用して日本語に翻訳するPythonツールです。

## セットアップ

### 1. 必要なツール

- Python 3.10以上
- Anthropic API Key
- uv (Python パッケージマネージャー)

### 2. uvのインストール

#### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. プロジェクトのセットアップ

```bash
# プロジェクトディレクトリに移動
cd claude-pdf-translator
```

### 4. 依存パッケージのインストール

#### uvを使用する場合（推奨）
```bash
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install .
```

#### pipを使用する場合
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 5. 環境変数の設定

#### macOS/Linux
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

#### Windows
```bash
# コマンドプロンプト
set ANTHROPIC_API_KEY=your-api-key-here

# PowerShell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

## 使用方法

1. PDFを画像に変換

```bash
python pdf_to_png.py
```

- 入力: PDFファイル（デフォルト: sample.pdf）
- 出力: `output/` ディレクトリに連番のPNG画像が生成されます（001.png, 002.png, ...）

2. 画像を翻訳

```bash
python main.py
```

- 入力: `output/` ディレクトリ内のPNG画像
- 出力: `translated.md`（翻訳結果のMarkdownファイル）

## ファイル構成

```
.
├── README.md           # このファイル
├── main.py            # 翻訳実行スクリプト
├── pdf_to_png.py      # PDF→PNG変換スクリプト
├── .gitignore         # Git除外設定
├── .python-version    # Python環境設定
├── pyproject.toml     # プロジェクト設定と依存関係
└── output/           # 変換された画像の出力先
```

## 注意事項

- 大きなPDFファイルの場合、変換に時間がかかる場合があります
- APIの利用制限に注意してください
- 画像の品質によって翻訳精度が変わる可能性があります
- 翻訳結果は `translated.md` に保存されます
- Windowsの場合、パスの区切り文字は `\` を使用してください
- パッケージのインストールは以下のいずれかを選択できます：
  - uv（推奨）: 高速なインストールと依存関係の管理を提供
  - pip: Pythonの標準パッケージインストーラー

## ライセンス

MIT License
