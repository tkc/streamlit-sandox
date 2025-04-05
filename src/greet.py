import time

import structlog  # Import structlog for contextvars
from pydantic import ValidationError

from model import GreetingInput, GreetingOutput  # Import from model within src

# Get logger instance configured in app.py
# Logs will go to console and app.log
log = structlog.get_logger(__name__) # Get logger by name

def generate_greeting(input_message: str, processing_id: str) -> dict:
    """
    入力メッセージと処理 ID を受け取り、挨拶メッセージを生成する関数。

    Args:
        input_message (str): 入力メッセージ
        processing_id (str): この処理リクエストの一意な ID

    Returns:
        dict: GreetingOutput モデルに対応する辞書。エラー時は status='error' を含む。
    """
    structlog.contextvars.bind_contextvars(processing_id=processing_id)
    # Log will include processing_id
    log.info("generate_greeting called", input_message=input_message)
    input_msg_for_output = input_message # Use original input for output model
    input_data_dict: dict = {} # Initialize dict for potential error logging

    try:
        # Pydantic モデルで入力を検証 (辞書として渡す)
        try:
            log.debug("Attempting to validate input with Pydantic")
            input_data_dict = {"message": input_message} # Assign here
            validated_input = GreetingInput.model_validate(input_data_dict)
            # Use validated message for processing if needed,
            # but keep original for output
            processing_message = validated_input.message
            log.info("Successfully validated input", message=processing_message)
        except ValidationError as e:
            log.error(
                "Input validation failed",
                error=str(e),
                input_data=input_data_dict,
                exc_info=True,
            )
            # Pydantic 検証エラー
            raise ValueError(f"入力データの検証に失敗しました: {e}")

        # 簡単な処理（ここでは受け取ったメッセージを使って挨拶を生成）
        log.info("Generating greeting message", message=processing_message)
        greeting_msg = (
            f"こんにちは、{processing_message}さん！ greet.py からのメッセージです。"
        )
        time.sleep(0.5) # 少し待機

        # Pydantic モデルを使用して出力データを作成
        log.debug("Creating output data model")
        output_data = GreetingOutput(
            input_message=input_msg_for_output, # Use original input here
            greeting=greeting_msg
        )
        log.info("Successfully created output data")
        # Return the model dump (dictionary)
        # Use mode='json' for datetime serialization
        result_dict = output_data.model_dump(mode="json")
        structlog.contextvars.clear_contextvars() # Clear context on success
        return result_dict

    except ValueError as e:
         # Pydantic 検証エラーなど、他の ValueError
         # Log includes processing_id
        log.error(
            "ValueError during processing (likely validation)",
            error=str(e),
            exc_info=True,
        )
        # Return an error structure consistent with GreetingOutput if possible
        error_output = GreetingOutput(
            input_message=input_msg_for_output,
            greeting="エラーが発生しました。",
            status="error",
            error_message=str(e)
        )
        result_dict = error_output.model_dump(mode="json")
        structlog.contextvars.clear_contextvars() # Clear context on error
        return result_dict
    except Exception as e:
        # その他の予期せぬエラー
        # Log includes processing_id
        log.exception("Unexpected error occurred in generate_greeting")
        error_output = GreetingOutput(
            input_message=input_msg_for_output,
            greeting="エラーが発生しました。",
            status="error",
            error_message=f"予期せぬエラーが発生しました: {str(e)}",
        )
        result_dict = error_output.model_dump(mode="json")
        structlog.contextvars.clear_contextvars() # Clear context on exception
        return result_dict

# Removed the main() function and if __name__ == "__main__": block
# as this module is now intended to be imported.
