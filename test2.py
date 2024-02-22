import os

# Đường dẫn đến chương trình AnyDesk.exe
anydesk_path = r'"C:\Program Files (x86)\AnyDesk\AnyDesk.exe"'

# Tạo lệnh để chạy
command = f'echo vasalaWRR2019 | {anydesk_path} 569163141 --with-password'

# Thực thi lệnh
os.system(command)
