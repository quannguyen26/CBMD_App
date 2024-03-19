import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('database/cbmd_database_2024.db')
cursor = conn.cursor()

# Số cần kiểm tra
so_can_kiem_tra = 65

# Truy vấn để kiểm tra xem số đã tồn tại trong cơ sở dữ liệu hay chưa
cursor.execute("SELECT COUNT(*) FROM cbmd_news WHERE id_news = ?", (so_can_kiem_tra,))
ket_qua = cursor.fetchone()
conn.close()
# Lấy kết quả từ tuple và kiểm tra
if ket_qua[0] > 0:
    print(f"Số {so_can_kiem_tra} đã tồn tại trong cơ sở dữ liệu.")
else:
    print(f"Số {so_can_kiem_tra} chưa tồn tại trong cơ sở dữ liệu.")

# Đóng kết nối

