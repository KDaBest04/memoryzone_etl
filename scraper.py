import requests
from bs4 import BeautifulSoup
import  time
import pandas as pd
from datetime import datetime

data_list=[]

for i in range(1,4):
    print("SCRAPING!!!")
    url = f"https://memoryzone.com.vn/laptop?q=collections:2828130&page={i}&view=grid"

    response = requests.get(url)

    print(response.status_code)
    soup = BeautifulSoup(response.content, "html.parser")
    laptop_list = soup.find_all('div', class_='col-6 col-sm-3 col-md-15 product-col')

    for laptop in laptop_list:
        name_label =laptop.find('h3', class_='product-name')

        if name_label:
            name = name_label.text.strip()
        else:
            name = "Can't find"

        price_label = laptop.find('span', class_='price')
        price = price_label.text.strip()
        compare_price_label = laptop.find('span', class_='compare-price')

        if compare_price_label:
            compare_price = compare_price_label.text.strip()
        else:
            compare_price = price
        # 1. Làm sạch Giá Bán
        try:
            # Xóa dấu chấm, ký hiệu ₫, chữ đ, chữ Đ, và xóa luôn mọi khoảng trắng
            int_price = int(
                price.replace('.', '').replace('₫', '').replace('đ', '').replace('Đ', '').replace(' ', '').strip())
        except ValueError:
            int_price = 0

        # 2. Làm sạch Giá Gốc
        try:
            # LƯU Ý: Chỗ này phải dùng biến chứa giá gốc (mình đang ví dụ là compare_price)
            int_compare_price = int(
                compare_price.replace('.', '').replace('₫', '').replace('đ', '').replace('Đ', '').replace(' ', '').strip())
        except ValueError:
            int_compare_price = 0
        date = datetime.now().strftime('%Y-%m-%d')

        laptop_item = {
            "Ten":name,
            "Gia ban":int_price,
            "Gia goc":int_compare_price,
            "Ngay_cap_nhat": date
        }
        data_list.append(laptop_item)
    time.sleep(2)

df = pd.DataFrame(data_list, columns=['Ten', 'Gia ban', 'Gia goc','Ngay_cap_nhat'])
df.to_csv('laptop_data.csv', index=False, encoding='utf-8-sig')
print('done')

