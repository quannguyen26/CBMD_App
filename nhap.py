import threading
import time

def worker():
    """Thread worker function"""
    print('Worker is starting')
    time.sleep(2)  # Giả sử công việc mất 2 giây
    print('Worker is finished')

# Tạo một thread mới để chạy hàm worker
t = threading.Thread(target=worker)

# Khởi động thread
t.start()

# Đợi cho đến khi thread t hoàn thành
t.join()

print('Main Thread: Waiting for the worker thread to complete.')

# Khi t.join() hoàn thành, chương trình chính sẽ tiếp tục thực thi
print('Main Thread: All done.')
