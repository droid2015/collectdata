# Tạo một tệp tin có tên là app.py
from datetime import datetime as dt
import os
from threading import Thread
import time
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from get_gold import get_gold_price

app = Flask(__name__)
# Thiết lập cấu hình cơ sở dữ liệu từ biến môi trường DATABASE_URL của Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#sua loi bang string postgresql
db = SQLAlchemy(app)
# Khởi tạo biến global để lưu trữ dữ liệu giá vàng
gold_entries = []
@app.route('/')
def hello():
    return 'Hello, World!'
@app.route('/gold_table')
def gold_table():
    # Lấy ngày lớn nhất từ cơ sở dữ liệu
    max_update_time = db.session.query(db.func.max(GoldEntry.update_time)).scalar()
    # Kiểm tra xem có ngày lớn nhất hay không
    if max_update_time:
        # Lấy tất cả bản ghi có ngày cập nhật bằng ngày lớn nhất
        latest_entries = GoldEntry.query.filter_by(update_time=max_update_time).all()
        return render_template('gold_table.html', gold_entries=latest_entries)
# Kiểm tra xem có bản ghi nào hay không
    else:
        return render_template('gold_table.html', gold_entries=[])
# Định nghĩa mô hình cho bảng giá vàng
class GoldEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    buy_price = db.Column(db.Float)  # Kiểu số
    buy_price_change = db.Column(db.Float)  # Kiểu số
    sell_price = db.Column(db.Float)  # Kiểu số
    sell_price_change = db.Column(db.Float)  # Kiểu số
    update_time = db.Column(db.DateTime, default=dt.utcnow)  # Kiểu ngày giờ

def update_gold_data():
    previous_update_time = None
    while True:
        update_time, new_gold_entries = get_gold_price(previous_update_time)
        #luu thoi gian
        
        if update_time and new_gold_entries:
            # Chỉ cập nhật và lưu vào cơ sở dữ liệu nếu update_time lớn hơn previous_update_time
            if previous_update_time is None or update_time > previous_update_time:
                previous_update_time = update_time
                # Lưu dữ liệu vào cơ sở dữ liệu
                save_to_database(new_gold_entries)
        # Chờ 1-2 phút trước khi lấy dữ liệu tiếp theo        
        time.sleep(120)
def save_to_database(entries):
    # Xóa dữ liệu cũ trong bảng
    #GoldEntry.query.delete()
    with app.app_context():
    # Thêm dữ liệu mới vào cơ sở dữ liệu
        for entry in entries:
            db.session.add(GoldEntry(
                name=entry['name'],
                buy_price=entry['buy_price'],
                buy_price_change=entry['buy_price_change'],
                sell_price=entry['sell_price'],
                sell_price_change=entry['sell_price_change'],
                update_time=entry['update_time']
            ))

        # Commit để lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()
# Đặt tiến trình cập nhật dữ liệu giá vàng thành một luồng
update_thread = Thread(target=update_gold_data)
# Đặt tiến trình ở chế độ daemon để nó sẽ kết thúc khi chương trình chính kết thúc
update_thread.daemon = True
update_thread.start()
# Tạo bảng trong cơ sở dữ liệu (chỉ cần làm một lần khi triển khai ứng dụng lần đầu)
# with app.app_context():
#      db.create_all()
if __name__ == '__main__':
    app.run()


