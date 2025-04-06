import uuid
from datetime import datetime

import streamlit as st
from pydantic import ValidationError

from src.greet import generate_greeting
from src.logger import configure_logging
from src.model import GreetingOutput

log = configure_logging("app.log")
log.info("アプリケーション開始")


def main():
    """Streamlitアプリのメイン関数"""
    # アプリのタイトルと説明
    st.title("外部スクリプト連携アプリ")
    st.write(
        "下のフォームにメッセージを入力し、ボタンを押すと "
        "`greet.py` スクリプトが実行され、その結果が表示されます。"
    )

    # 入力フォーム
    with st.form("greet_form"):
        message_input = st.text_input("メッセージを入力してください", "World")
        submitted = st.form_submit_button("greet.py を実行")

    # フォーム送信時の処理
    if submitted:
        process_submission(message_input)


def process_submission(message: str):
    """フォーム送信の処理"""
    # 処理IDの生成
    processing_id = str(uuid.uuid4())
    log.info("フォーム送信", message=message, processing_id=processing_id)

    # メッセージの検証
    if not message:
        st.warning("メッセージを入力してください。")
        return

    # 処理の実行
    with st.spinner("挨拶を生成中..."):
        try:
            # 外部関数の呼び出し
            output_dict = generate_greeting(message, processing_id=processing_id)
            status = output_dict.get("status", "")
            log.info("結果受信", result_status=status, processing_id=processing_id)

            # 結果の検証と表示
            try:
                parsed_output = GreetingOutput.model_validate(output_dict)
                log.info(
                    "結果検証成功",
                    status=parsed_output.status,
                    processing_id=processing_id,
                )

                # 挨拶の表示
                st.markdown(f"### {parsed_output.greeting}")

                # 詳細情報の表示
                st.success(f"ステータス: {parsed_output.status}")

                # タイムスタンプのフォーマット
                formatted_timestamp = format_timestamp(parsed_output.timestamp)
                st.write(f"タイムスタンプ: {formatted_timestamp}")
                st.write(f"入力メッセージ: {parsed_output.input_message}")
                st.caption(f"実行 Python: {parsed_output.python_version}")

                # エラーメッセージの表示
                if parsed_output.error_message:
                    st.error(f"処理エラー: {parsed_output.error_message}")

            except ValidationError as e:
                log.error(
                    "検証エラー",
                    error=str(e),
                    raw_output=output_dict,
                    processing_id=processing_id,
                )
                st.error("処理結果の形式が無効です:")
                st.json(output_dict)
                st.code(str(e))

        except Exception as e:
            log.exception("予期せぬエラー", processing_id=processing_id)
            st.error(f"予期せぬエラーが発生しました: {e}")


def format_timestamp(timestamp):
    """タイムスタンプを適切にフォーマット"""
    if isinstance(timestamp, datetime):
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(timestamp, str):
        # 文字列の場合はパースを試みる
        try:
            timestamp_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            return timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return timestamp
    else:
        return str(timestamp)


if __name__ == "__main__":
    main()
