import uuid  # Import uuid for generating processing ID

import streamlit as st
import structlog  # type: ignore # Import structlog for contextvars
from pydantic import (
    ValidationError,  # Keep for potential direct validation if needed later
)

from greet import generate_greeting  # Import function directly from greet within src
from logger import configure_logging  # Import logging config function from logger.py
from model import GreetingOutput  # Import from model within src

# --- Logging Configuration ---
log = configure_logging("app.log") # Configure and get logger
# --- End Logging Configuration ---

log.info("Streamlit app started")

st.title("外部スクリプト連携アプリ (Pydantic)")
st.write(
    "下のフォームにメッセージを入力し、ボタンを押すと "
    "`greet.py` スクリプトが実行され、その結果が表示されます。"
)

# 入力フォーム
with st.form("greet_form"):
    message_input = st.text_input("メッセージを入力してください", "World")
    submitted = st.form_submit_button("greet.py を実行")

    if submitted:
        processing_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(processing_id=processing_id)
        # Log will now include processing_id
        log.info("Form submitted", message=message_input)
        st.write("---")
        st.subheader("`greet.py` の実行結果:")

        if not message_input:
            log.warning("Empty message submitted") # Log will include processing_id
            st.warning("メッセージを入力してください。")
            structlog.contextvars.clear_contextvars() # Clear context if no message
        else:
            try:
                # Log includes processing_id
                log.info(
                    "Calling generate_greeting function",
                    input_message=message_input,
                )
                # generate_greeting 関数を直接呼び出し、processing_id を渡す
                output_dict = generate_greeting(
                    message_input, processing_id=processing_id
                )
                # Log includes processing_id
                log.info(
                    "Received result from generate_greeting",
                    result_status=output_dict.get("status"),
                )

                # 結果を Pydantic モデルで検証 (generate_greeting が辞書を返すため)
                try:
                    parsed_output = GreetingOutput.model_validate(output_dict)
                    log.info(
                        "Successfully validated output from generate_greeting",
                        status=parsed_output.status,
                    )

                    # 結果を表示
                    st.success(f"ステータス: {parsed_output.status}")
                    # Handle potential datetime string from model_dump(mode='json')
                    timestamp_str = (
                        parsed_output.timestamp.isoformat()
                        if hasattr(parsed_output.timestamp, "isoformat")
                        else str(parsed_output.timestamp)
                    )
                    st.write(f"タイムスタンプ: {timestamp_str}")
                    st.write(f"入力メッセージ: {parsed_output.input_message}")
                    st.write(f"挨拶: {parsed_output.greeting}")
                    st.caption(f"実行 Python: {parsed_output.python_version}")
                    if parsed_output.error_message:
                        log.warning(
                            "generate_greeting reported an error",
                            error_message=parsed_output.error_message,
                        )
                        st.error(f"処理エラー: {parsed_output.error_message}")

                except ValidationError as e:
                    log.error(
                        "Pydantic validation failed for generate_greeting output",
                        error=str(e),
                        raw_output=output_dict,
                        exc_info=True,
                    )
                    st.error("処理結果の形式が無効です (Pydantic 検証エラー):")
                    st.json(output_dict) # 元の辞書を表示
                    st.code(str(e), language="") # 検証エラー詳細

            except Exception as e:
                # Log includes processing_id
                log.exception("Unexpected error occurred calling generate_greeting")
                st.error(f"予期せぬエラーが発生しました: {e}")
            finally:
                # Ensure context is cleared regardless of success or failure
                structlog.contextvars.clear_contextvars()
