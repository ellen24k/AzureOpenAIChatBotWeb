import glob
import os

import streamlit as st

from pkg_db.db import fetch_all_data, delete_data, file_delete
from pkg_utils.utils import padding_set, extract_filename


def load_view():
    padding_set()

    if st.session_state['logged_in'] == False or st.session_state['admin'] == False:
        admin_pass = st.text_input('**관리자 비밀번호를 입력하세요.**', type='password')
        if st.button('관리자 로그인'):
            if admin_pass != st.secrets["passwords"]["admin_password"]:
                st.error('비밀번호가 틀렸습니다.')
                st.stop()
            else:
                st.session_state['admin'] = True
                st.write('관리자 로그인 성공')
                st.rerun()
    else:
        st.title('관리자')

        def list_temp_files():
            temp_dir = 'temp'
            if os.path.exists(temp_dir):
                files = os.listdir(temp_dir)
                for file in files:
                    print(file)
            else:
                print(f"'{temp_dir}' 디렉토리가 존재하지 않습니다.")

        list_temp_files()

        def delete_temp_files():
            temp_dir = 'temp'
            if os.path.exists(temp_dir):
                wav_files = glob.glob(os.path.join(temp_dir, '*.wav'))
                png_files = glob.glob(os.path.join(temp_dir, '*.png'))

                for file in wav_files + png_files:
                    try:
                        os.remove(file)
                        print(f"{file} 삭제 완료")
                    except Exception as e:
                        print(f"{file} 삭제 실패: {e}")
            else:
                print(f"'{temp_dir}' 디렉토리가 존재하지 않습니다.")

        if st.button('임시 파일 삭제'):
            delete_temp_files()

        data = fetch_all_data()

        if data.empty:
            st.write("No data available or table does not exist.")
        else:
            for index, row in data.iterrows():
                st.image(row['img_url'], use_column_width=True, caption=f"{row['content']}")
                if st.button(row['date'] + ' 삭제'):
                    delete_data(row['date'])
                    img_file_name = extract_filename(row['img_url'])
                    wav_file_name = extract_filename(row['wav_url'])

                    file_delete("ChatBotFiles", img_file_name)
                    file_delete("ChatBotFiles", wav_file_name)
                    st.rerun()

                st.markdown("---")
