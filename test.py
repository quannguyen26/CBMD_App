import datetime

# Nhập giờ và phút từ bàn phím
hour = int(input("Nhập giờ hiện tại (0-23): "))
minute = int(input("Nhập phút hiện tại (0-59): "))

# Làm tròn phút sao cho chia hết cho 10
minute_rounded = (minute // 10) * 10

# Tạo một đối tượng datetime với thời gian hiện tại và lùi đi 10 phút
current_time = datetime.datetime.now().replace(hour=hour, minute=minute_rounded)
new_time = current_time - datetime.timedelta(minutes=10)

print("Thời gian hiện tại:", current_time.strftime("%H:%M"))
print("Thời gian sau khi lùi 10 phút:", new_time.strftime("%H:%M"))
