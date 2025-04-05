# システムパターン

## アーキテクチャ

- Streamlit アプリケーション (`src/app.py`) がフロントエンドとして機能し、ユーザー入力を受け付ける。
- **挨拶生成ロジックは `src/greet.py` 内の関数 (`generate_greeting`) として実装される。**
- `src/app.py` は `src/greet.py` から `generate_greeting` 関数を直接インポートして呼び出す。
- `generate_greeting` 関数は入力を **Pydantic モデル (`GreetingInput`) で検証** し、処理結果を Pydantic モデル (`GreetingOutput`) に基づく辞書として返す。
- `src/app.py` は返された辞書を受け取り、Pydantic モデルで検証して結果を表示する。
- **ログ設定は `src/logger.py` に集約され、`src/app.py` と `src/greet.py` はこれを利用してログを出力する (コンソール + `log/app.log` または `log/greet.log`)。各リクエストには一意の `processing_id` が付与され、ログに含まれる。**

## 主要な技術的決定

- ウェブフレームワークとして Streamlit を採用。
- **アプリケーションロジックは関数としてモジュール化 (`src/greet.py`) し、Streamlit アプリ (`src/app.py`) から直接インポートして使用する。** (`subprocess` は使用しない)
- データ構造の定義と検証には Pydantic モデル (`src/model.py`) を使用する。
- **ログ設定は共通モジュール (`src/logger.py`) に集約し、ログ出力には `structlog` を使用する。`structlog.contextvars` を利用してリクエストごとの処理 ID をログに含める。**
- **コードは `src` ディレクトリに配置し、Python パッケージとして構成する。**
- Docker イメージ内では `PYTHONPATH` を設定して `src` 内のモジュールをインポート可能にする。

## デザインパターン

- **モジュール化:** 挨拶生成ロジックを独立した関数 (`generate_greeting`) として `src/greet.py` に分離。
- **データ転送オブジェクト (DTO):** Pydantic モデル (`GreetingInput`, `GreetingOutput`) が DTO として機能し、アプリケーション内のデータ構造を定義・検証する。
- **設定の外部化 (一部):** ログ設定を `src/logger.py` に分離。

## コンポーネントの関係

- `src/app.py`: Streamlit アプリケーション本体。フォーム送信時に `processing_id` を生成し、ログコンテキストにバインド。`src.greet.generate_greeting` 関数に `processing_id` を渡して呼び出す。`src.model` と `src.logger` をインポートする。
- `src/greet.py`: `generate_greeting` 関数を定義するモジュール。引数で受け取った `processing_id` をログコンテキストにバインドする。`src.model` と `src.logger` をインポートする。
- `src/model.py`: Pydantic モデル (`GreetingInput`, `GreetingOutput`) を定義するモジュール。
- `src/logger.py`: `structlog` の設定を行う `configure_logging` 関数を定義するモジュール。
- `requirements.txt`: 依存関係 (`streamlit`, `pydantic`, `structlog` など) を管理する。
- `.streamlit/config.toml`: Streamlit アプリケーションのクライアントサイドの動作を設定する。
- `log/app.log`, `log/greet.log`: アプリケーションのログファイル (設定による)。
- `Dockerfile`: アプリケーションのコンテナイメージをビルドする。`src` ディレクトリをコピーし、`PYTHONPATH` を設定し、`src/app.py` を実行する。
- `Makefile`: Docker 操作を簡略化する。
