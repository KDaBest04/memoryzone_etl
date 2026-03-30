import os
import pandas as pd
from sqlalchemy import create_engine

# 1. ĐỌC DỮ LIỆU TỪ FILE CSV
try:
    print("Đang đọc dữ liệu từ file laptop_data.csv...")
    df = pd.read_csv('laptop_data.csv')
    df = df.drop_duplicates(subset=['Ten', 'Ngay_cap_nhat'])
    print(f"Đã đọc thành công {len(df)} dòng dữ liệu.")
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file laptop_data.csv. Bạn đã chạy file cào dữ liệu chưa?")
    exit()

# 2. LẤY KẾT NỐI TỪ BIẾN MÔI TRƯỜNG (BẢO MẬT TUYỆT ĐỐI)
# Thay vì viết thẳng mật khẩu ra đây, code sẽ tự đi tìm biến có tên 'DATABASE_URL'
DB_URL = os.environ.get('DATABASE_URL')

if not DB_URL:
    print("Lỗi: Không tìm thấy biến môi trường DATABASE_URL. Hãy kiểm tra lại cài đặt Secrets trên GitHub!")
    exit()

# 3. ĐẨY LÊN CLOUD NEON
print("Đang khởi động phi thuyền kết nối với máy chủ Neon (Singapore)...")
try:
    engine = create_engine(DB_URL)

    df.to_sql('laptop_prices_history', engine, if_exists='append', index=False)

    print("Success!")

    # --- ĐOẠN CODE KIỂM TRA ---
    print("\nĐang kiểm tra lại tổng số lượng laptop trên mây...")
    check_df = pd.read_sql("SELECT COUNT(*) FROM laptop_prices_history", engine)
    tong_so_dong = check_df.iloc[0, 0]
    print(f"Báo cáo sếp: Tổng số dòng hiện tại trong Database Neon là: {tong_so_dong} dòng!")

except Exception as e:
    print(f"Ối, có lỗi xảy ra khi đẩy lên server: {e}")