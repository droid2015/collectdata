import requests
from bs4 import BeautifulSoup
from datetime import datetime
# Lấy dữ liệu giá vàng từ một API
def get_gold_price(previous_update_time=None):
    url = "https://bieudogiavang.vn/"
    # Gửi yêu cầu GET để tải nội dung trang web
    response = requests.get(url)
    # Kiểm tra xem yêu cầu có thành công không (status code 200 là thành công)
    if response.status_code == 200:
    # Sử dụng BeautifulSoup để phân tích nội dung HTML
        soup = BeautifulSoup(response.text, "html.parser")
        # Tìm thời gian cập nhật
        thoigian = soup.select_one(".text-amber-500").text.strip().split("lúc")[1].strip()
        thoigian = thoigian.replace(" ", "")
        update_time = datetime.strptime(thoigian, "%H:%Mngày%d/%m/%Y")
        if previous_update_time is None or update_time > previous_update_time:
            gold_entries = []
            gold_table = soup.find("table", {"class": "min-w-full divide-y font-base text-sm divide-gray-200 text-gray-800"})
            rows = gold_table.select("tbody tr")
            if rows:
                # In thông tin giá vàng
                for number, row in enumerate(rows, start=1):
                    name = row.select_one(".w-64 span").text.strip()
                    buy_price = row.select(".text-right")[0].select_one(".tabular-nums").text.strip().replace(".", "")
                    buy_price_change = row.select(".text-right")[0].select_one(".text-red-500")
                    if buy_price_change:
                        buy_price_change = buy_price_change.text.strip()
                    sell_price = row.select(".text-right")[1].select_one(".tabular-nums").text.strip().replace(".", "")
                    sell_price_change = row.select(".text-right")[1].select_one(".text-red-500")
                    if sell_price_change:
                        sell_price_change = sell_price_change.text.strip()
                    entry = {
                        'update_time':update_time,
                        'number': number,
                        'name': name,
                        'buy_price': buy_price,
                        'buy_price_change': buy_price_change,
                        'sell_price': sell_price,
                        'sell_price_change': sell_price_change
                    }
                    gold_entries.append(entry)

                return update_time, gold_entries
        # kg co data moi    
        return  update_time, None   
    return None, None
