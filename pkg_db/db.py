import sqlite3
import threading
import glob
import os
from pkg_utils import extract_title_from_txt

class DatabaseManager:
    def __init__(self, db_name='pkg_db/data.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False) # check_same_thread=False는 다중 스레드에서 사용하기 위한 옵션
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()
        self.create_table()

    def create_table(self):
        with self.lock:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL
            )
            ''')
            self.conn.commit()

    def add_data(self, id, title):
        with self.lock:
            self.cursor.execute('''
            INSERT INTO data (id, title) VALUES (?, ?)
            ''', (id, title))
            self.conn.commit()

    def delete_data(self, data_id):
        with self.lock:
            self.cursor.execute('''
            DELETE FROM data WHERE id = ?
            ''', (data_id,))
            self.conn.commit()

    def select_data(self, data_id):
        with self.lock:
            self.cursor.execute('''
            SELECT * FROM data WHERE id = ?
            ''', (data_id,))
            return self.cursor.fetchone()

    def select_all_data(self):
        with self.lock:
            self.cursor.execute('''
            SELECT * FROM data ''')
            return self.cursor.fetchall()

    def clear_table(self):
        with self.lock:
            self.cursor.execute('DELETE FROM data')
            self.conn.commit()

    def add_data_from_history(self, history_folder='history'):
        self.clear_table()
        txt_files = glob.glob(os.path.join(history_folder, '*.txt'))
        for txt_file in txt_files:
            file_id = os.path.splitext(os.path.basename(txt_file))[0]
            with open(txt_file, 'r', encoding='utf-8') as file:
                title = extract_title_from_txt(file_id)
            self.add_data(file_id, title)

    def close(self):
        with self.lock:
            self.conn.close()


# if __name__ == '__main__':
#     pkg_db = DatabaseManager()
#     pkg_db.add_data_from_history()
#
#     all_data = pkg_db.select_all_data()
#     for row in all_data:
#         print(row)
#     pkg_db.close()
