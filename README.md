# Streamlit Sandbox

Streamlit applicationのサンドボックスプロジェクトです。

## 開発環境のセットアップ

```bash
# 開発環境のセットアップ
make setup

# 仮想環境のアクティベート
source .venv/bin/activate

# アプリケーションの実行
make run-local
```

## 利用可能なコマンド

- `make setup` - 開発環境のセットアップ
- `make sync` - 依存関係の同期
- `make run-local` - ローカルでアプリケーションを実行
- `make lint` - コードのリント
- `make typecheck` - 型チェック
- `make test` - テストの実行
- `make build` - Dockerイメージのビルド
- `make run` - Dockerコンテナの実行
