# ベースイメージとして公式の Python イメージを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt requirements.txt

# 依存関係をインストール (uv を使う場合)
# RUN pip install uv
# RUN uv pip install --no-cache-dir -r requirements.txt
# 依存関係をインストール (pip を使う場合)
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit 設定ファイルをコピー (存在する場合)
COPY .streamlit/ .streamlit/

# ログディレクトリを作成
RUN mkdir log

# アプリケーションコードをコピー (src ディレクトリ全体)
COPY src/ src/

# PYTHONPATH を設定して src ディレクトリ内のモジュールをインポート可能にする
# (WORKDIR が /app なので、PYTHONPATH=/app で src.module のようにインポート可能)
ENV PYTHONPATH=/app

# Streamlit が使用するポートを公開
EXPOSE 8501

# ヘルスチェックコマンド (オプション)
HEALTHCHECK CMD streamlit hello --server.enableCORS=false --server.enableXsrfProtection=false || exit 1

# アプリケーションを実行するコマンド (src/app.py を指定)
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
