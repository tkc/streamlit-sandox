# Streamlit + 外部スクリプト連携 (Pydantic) デモ

## ローカルでの実行方法

1.  このリポジトリをクローンします:

    ```bash
    git clone <repository-url>
    cd streamlit-sandox
    ```

2.  (推奨) 仮想環境を作成して有効化します:

    ```bash
    python -m venv .venv
    source .venv/bin/activate # Linux/macOS
    # .venv\Scripts\activate # Windows
    ```

3.  依存パッケージをインストールします (`uv` を使用する場合):

    ```bash
    pip install uv
    uv pip install -r requirements.txt
    ```

4.  Streamlit アプリを起動します (`uv` を使用する場合):
    ```bash
    uv run streamlit run src/app.py
    ```

アプリケーションはデフォルトで http://localhost:8501 で起動します。

## Docker での実行方法 (Makefile 使用)

プロジェクトルートにある `Makefile` を使用して、Docker 操作を簡単に行えます。

- **イメージのビルド:**
  ```bash
  make build
  ```
- **コンテナの実行 (バックグラウンド、ログマウント付き):**
  ```bash
  make run
  ```
  実行後、Web ブラウザで http://localhost:8501 にアクセスしてください。ログはホストの `./log` ディレクトリに出力されます。
- **実行中のコンテナのログ表示:**
  ```bash
  make logs
  ```
- **コンテナの停止:**
  ```bash
  make stop
  ```
- **コンテナの削除 (停止後):**
  ```bash
  make rm
  ```
- **ビルドしたイメージの削除:**
  ```bash
  make clean
  ```
- **ビルドと実行を一度に:**
  ```bash
  make all
  ```
- **利用可能なコマンド一覧表示:**
  ```bash
  make help
  ```
