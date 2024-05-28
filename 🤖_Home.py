import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
st.set_page_config(page_title="Face Attendance", page_icon="🤖")
st.header("使用人臉辨識的考勤系統")

with open('./config.yaml', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('Login', 'main')

with st.spinner("Loading Models and Connecting to Redis DB"):
    import face_real_rec

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = authentication_status

if authentication_status == False:
    st.error("使用者/密碼不正確")

if authentication_status is None:
    st.warning("請輸入您的使用者和密碼")

if authentication_status:
    st.subheader(f'歡迎  *{name}* 🤖')
    st.markdown('''
        #### 人臉預測 (Face Prediction)
        - 偵測臉部並預測該人的姓名
        - 系統將記錄識別的人和時間戳，然後每 30 秒儲存到資料庫
        
        #### 登記 (Registration)
        - 使用姓名和 ID 註冊新人
        - 採集臉部樣本，建議200-300個樣本
        
        #### 紀錄 (Logs)
        - 顯示所有註冊人員
        - 顯示人臉預測結果
    ''')
    authenticator.logout("登出", "sidebar")
