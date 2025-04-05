# アクティブコンテキスト

## 現在のフォーカス

フォーム送信時に一意な処理 ID を生成し、関連するログ (`app.py`, `greet.py`) に含めるように修正。

## 最近の変更

- `src/app.py` を修正:
  - `uuid` と `structlog` をインポート。
  - フォーム送信時に `processing_id` を生成。
  - `structlog.contextvars.bind_contextvars` で `processing_id` をバインド。
  - `generate_greeting` に `processing_id` を渡す。
  - `try...finally` で `structlog.contextvars.clear_contextvars()` を呼び出す。
- `src/greet.py` を修正:
  - `generate_greeting` 関数の引数に `processing_id` を追加。
  - 関数内で `processing_id` をログコンテキストにバインド。
  - `try...except...finally` (暗黙的) でコンテキストをクリア。
- 関連するメモリーバンクファイル (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`) を更新。

## 次のステップ

1. 残りのメモリーバンクファイル (`progress.md`) を更新して、処理 ID のログ追加を反映する。
2. ローカルで `uv run streamlit run src/app.py` を実行し、アプリが動作し、ログに `processing_id` が含まれることを確認する。
3. `make run` でコンテナを実行し、ログに `processing_id` が含まれることを確認する。

## アクティブな決定事項

- アプリケーションのコア機能を、フォーム入力と外部スクリプトとの JSON/Pydantic ベースの連携に変更。
- データ交換フォーマットとして JSON を使用し、その構造定義と検証に Pydantic を利用する (**入力・出力双方**)。
- 外部スクリプトへのデータ渡しは **JSON 文字列をコマンドライン引数として** 使用する。
- すべての Python コード (`app.py`, `greet.py`, `model.py`, `logger.py`) は `src` ディレクトリに配置する。
- `greet.py` のロジックは関数 (`generate_greeting`) として提供し、`app.py` から直接インポートして使用する。 (`subprocess` は使用しない)
- ログ設定は `src/logger.py` に共通化する。
- **リクエストごとの処理 ID (`processing_id`) を生成し、`structlog.contextvars` を使用して関連ログに含める。**
- Pydantic モデル定義は `src/model.py` に配置する。
- アプリケーションの配布には Docker を使用する。
- ログ出力には `structlog` を使用し、コンソールとログファイル (`log/app.log`, `log/greet.log`) に出力する。
- Docker 実行時には、ログ永続化のためにホストの `log` ディレクトリを `/app/log` にマウントする。
- Docker 操作は `Makefile` を使用して行う。
- Streamlit のツールバー設定 (`config.toml`) は維持する (`toolbarMode = "minimal"`)。
- **ローカル実行時に `PYTHONPATH` の設定は不要。**
