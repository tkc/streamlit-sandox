import streamlit as st
from datetime import datetime
import uuid

from greet import generate_greeting
from model import GreetingOutput
from logger import configure_logging

# ロガーの設定
log = configure_logging("app_simple.log")

def main():
    """シンプルなStreamlitアプリケーション"""
    # アプリケーションのタイトルと説明
    st.title("外部スクリプト連携アプリ")
    st.write("メッセージを入力して挨拶を生成します")
    
    # 入力フォーム
    with st.form("greet_form"):
        message = st.text_input("メッセージを入力してください", "World")
        submitted = st.form_submit_button("挨拶を生成")
    
    # フォームが送信された場合の処理
    if submitted:
        # 処理IDの生成
        processing_id = str(uuid.uuid4())
        log.info("フォーム送信", message=message, processing_id=processing_id)
        
        if not message:
            st.warning("メッセージを入力してください")
            return
        
        # 挨拶の生成処理
        with st.spinner("挨拶を生成中..."):
            try:
                # 外部関数呼び出し
                result = generate_greeting(message, processing_id=processing_id)
                
                # 結果の検証と表示
                output = GreetingOutput.model_validate(result)
                
                # 結果表示
                st.success("生成完了")
                st.markdown(f"### {output.greeting}")
                
                # 詳細情報の表示（折りたたみ可能）
                with st.expander("詳細情報"):
                    st.write(f"ステータス: {output.status}")
                    
                    # タイムスタンプのフォーマット
                    if isinstance(output.timestamp, datetime):
                        formatted_time = output.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        formatted_time = str(output.timestamp)
                        
                    st.write(f"タイムスタンプ: {formatted_time}")
                    st.write(f"入力メッセージ: {output.input_message}")
                    st.write(f"Python バージョン: {output.python_version}")
                
                # エラーメッセージがある場合は表示
                if output.error_message:
                    st.error(f"エラー: {output.error_message}")
                    
            except Exception as e:
                st.error(f"処理中にエラーが発生しました: {e}")
                log.exception("予期せぬエラー", processing_id=processing_id)

if __name__ == "__main__":
    main()
