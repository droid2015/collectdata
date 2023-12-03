# Tạo một tệp tin có tên là app.py
from threading import Thread
import time
from flask import Flask, render_template

from get_gold import get_gold_price

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
@app.route('/gold_table')
def gold_table():
    # Giả sử gold_entries là một danh sách các dữ liệu giá vàng
    return render_template('gold_table.html', gold_entries=gold_entries)
def update_gold_data():
    global gold_entries
    previous_update_time = None
    while True:
        update_time, new_gold_entries = get_gold_price(previous_update_time)

        if update_time and new_gold_entries:
            previous_update_time = update_time
            # Cập nhật dữ liệu giá vàng
            gold_entries = new_gold_entries

        # Chờ 1-2 phút trước khi lấy dữ liệu tiếp theo
        time.sleep(120)
# Đặt tiến trình cập nhật dữ liệu giá vàng thành một luồng
update_thread = Thread(target=update_gold_data)
# Đặt tiến trình ở chế độ daemon để nó sẽ kết thúc khi chương trình chính kết thúc
update_thread.daemon = True
update_thread.start()
if __name__ == '__main__':
    app.run()
    previous_update_time = None
    while True:
        update_time, gold_entries = get_gold_price(previous_update_time)

        if update_time and gold_entries:
            previous_update_time = update_time

        # Chờ 1-2 phút trước khi lấy dữ liệu tiếp theo
        time.sleep(120)

