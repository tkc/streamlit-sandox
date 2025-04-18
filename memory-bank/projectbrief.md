# プロジェクト概要

## プロジェクト名

Streamlit サンドボックス

## 目的

Streamlit アプリケーションでユーザー入力を受け取り、その入力を外部 Python スクリプト (`greet.py`) に渡し、スクリプトからの構造化された JSON 出力 (Pydantic モデルで定義) を解析して表示する方法をデモンストレーションする。

## 主要な要件

- Streamlit を使用してウェブアプリケーションを構築する。
- アプリ内に入力フォームと実行ボタンを配置する。
- ボタンクリック時に、フォームの入力内容をコマンドライン引数として `greet.py` に渡す。
- `greet.py` は受け取った引数を処理し、結果を Pydantic モデルで定義された構造の JSON として標準出力に出力する。
- `app.py` は `greet.py` の JSON 出力を受け取り、解析し、(オプションで Pydantic を使って検証し)、整形して表示する。
- スクリプト実行、JSON 解析、Pydantic 検証のエラーハンドリングを行う。
- 依存関係に `pydantic` を追加する。
