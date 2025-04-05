# 進捗状況

## 動作するもの

- `requirements.txt` に `pydantic` と `structlog` が追加された。
- **すべての Python コード (`app.py`, `greet.py`, `model.py`, `logger.py`) が `src` ディレクトリに配置された。** (`cmd` ディレクトリは削除)
- **`src/logger.py` が作成 (リネーム) され、ログ設定が共通化された。**
- **`src/greet.py` が関数化 (`generate_greeting`) され、`processing_id` を受け取りログコンテキストにバインドするように修正された。**
- **`src/app.py` が修正され、`processing_id` を生成・バインドし、`generate_greeting` に渡すように変更された。**
- **`Dockerfile` が更新され、`src` ディレクトリのコピー、`PYTHONPATH` 設定、エントリーポイント (`src/app.py`) が反映された。**
- `.streamlit/config.toml` が更新され、ツールバーが最小限モード (`minimal`) に設定されている。
- `.dockerignore` が更新され、ローカルの `log` ディレクトリが除外されるようになった。
- `Makefile` が作成され、Docker 操作 (build, run, stop など) が定義された。
- **`README.md` が更新され、新しいファイル構造、ローカル実行方法 (PYTHONPATH 不要)、`Makefile` の使い方、`logger.py` について記載された。**
- すべてのメモリーバンクファイル (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`) が最新のアプリケーションの状態 (処理 ID ログ追加を含む) を反映するように更新された。

## 残っている作業

- ローカルで依存関係をインストール (`uv run pip install -r requirements.txt`) し、アプリケーションを実行 (`uv run streamlit run src/app.py`) して動作とログ出力 (`processing_id` が含まれること) を確認する。
- `Makefile` を使用して Docker イメージをビルド (`make build`) し、コンテナを実行 (`make run`) して動作とログ出力 (ホストの `./log` へ、`processing_id` が含まれること) を確認する。
- (オプション) `make stop`, `make logs` などの他の `Makefile` ターゲットの動作を確認する。

## 現在のステータス

- アプリケーションのコア機能実装、Pydantic モデル共通化、Docker 化準備、ログ機能 (`structlog`) の実装、`Makefile` の作成、コード構造のリファクタリング (`src` への集約、`greet` の関数化、ログ設定共通化 (`logger.py`))、**処理 ID のログへの追加**、および関連ドキュメント更新が完了。
- ローカルおよび Docker (`Makefile` 使用) での実行とログ出力 (`processing_id` 含む) の確認待ち。

## 既知の問題

- (なし)
