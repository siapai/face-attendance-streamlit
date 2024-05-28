import streamlit as st
import constants

st.set_page_config(page_title="Report", page_icon="📉")

if 'authentication_status' in st.session_state and st.session_state['authentication_status']:

    with st.spinner('Retrieving data from redis...'):
        import face_real_rec as face_rec

    st.subheader('資料日誌')

    def load_logs(name, end=-1):
        logs_list = face_rec.r.lrange(name, start=0, end=end)
        clean_list = [x.decode('utf-8') for x in logs_list]
        return clean_list


    tab1, tab2 = st.tabs(['註冊人', '考勤日誌'])
    col1, col2 = st.columns([1, 1])

    with tab1:
        redis_face_db = face_rec.retrieve_data(name=constants.REGISTER_KEY)
        if st.button('Refresh Data'):
            redis_face_db = face_rec.retrieve_data(name=constants.REGISTER_KEY)
        with st.spinner('Retrieving data from redis...'):
            if not redis_face_db.empty:
                st.dataframe(redis_face_db[['Name', 'User_Id']])

    with tab2:
        if st.button('Refresh Logs'):
            st.write(load_logs(name=constants.LOG_KEY))
        else:
            st.write(load_logs(name=constants.LOG_KEY))
else:
    st.warning('您沒有權限')
