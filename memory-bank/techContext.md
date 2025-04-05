# 技術コンテキスト

## 使用技術

- Python 3.x
- Streamlit
- Pydantic (データ検証とシリアライズ)
- **structlog (ログ出力)**
- Python 標準ライブラリ: `sys`, `json`, `datetime`, `time`, `logging`, `os` # subprocess, argparse は不要に
- **Docker (コンテナ化)**

## 開発セットアップ

- ローカルマシンで Python 環境をセットアップし、`uv` などのパッケージマネージャーを使用する。
- `uv run pip install -r requirements.txt` を実行して依存関係 (`streamlit`, `pydantic`, **`structlog`**) をインストールする。
- **プロジェクト構造:**
  - `src/app.py`: Streamlit アプリケーション
  - `src/greet.py`: 挨拶生成モジュール
  - `src/model.py`: Pydantic モデル
  - `src/logger.py`: ログ設定モジュール
  - `Makefile`: Docker 操作用
- **ログは `log/app.log` および `log/greet.log` に出力される (設定による)。各ログエントリにはリクエストごとの `processing_id` が含まれる。**
- `.streamlit/config.toml` ファイルを使用して Streamlit のクライアントサイドの動作をカスタマイズする (`toolbarMode = "minimal"`)。
- **ローカルでのアプリケーション実行:**
  - `uv run streamlit run src/app.py` (uv 使用)
  - または `streamlit run src/app.py` (直接実行)
  - (PYTHONPATH 設定は不要)
- **Docker 操作は `Makefile` (`make build`, `make run` など) を使用して行う。**

## デプロイメント

- アプリケーションは Docker を使用してコンテナ化される。
- `Dockerfile` にビルド手順が定義されている。
- `.dockerignore` ファイルで不要なファイル (`log/` など) がイメージに含まれないように管理されている。
- **Makefile ターゲット:**
  - `make build`: Docker イメージをビルドする。
  - `make run`: コンテナを実行する (ログはホストの `./log` にマウント)。
  - `make stop`: コンテナを停止する。
  - `make logs`: コンテナのログを表示する。
  - `make clean`: Docker イメージを削除する。

## 技術的制約

- Streamlit の機能と制限に依存する。
- ~~`subprocess` を使用した外部プロセス実行のセキュリティとパフォーマンスに関する考慮が必要。~~ (subprocess 不使用のため削除)
- ~~Pydantic モデルの定義が `app.py` と `greet.py` で重複している（改善の余地あり）。~~ -> **`src/model.py` に共通化して解消済み。**

## 依存関係

- `streamlit` (バージョンは `requirements.txt` を参照)
- `pydantic` (バージョンは `requirements.txt` を参照)
- **`structlog`** (バージョンは `requirements.txt` を参照)
