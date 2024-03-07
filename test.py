from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import glob
import sys
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

op = webdriver.ChromeOptions()
prefs = {'download.default_directory' : resource_path('fast_warning')}
op.add_experimental_option('prefs', prefs)
op.add_argument("--window-size=50,50")
service=Service(executable_path='chromedriver.exe')
driver=webdriver.Chrome(service=service, options=op)
driver.minimize_window()
driver.get("http://hymetnet.gov.vn")
find=driver.find_element(By.XPATH,'//h6[@class="widget__title"]')
click=find.find_element(By.TAG_NAME,"a")
click.click()
name_file_warning=click.text
driver.quit()

# Đường dẫn đến thư mục chứa các file .tmp
folder_path = resource_path('fast_warning')
# Tìm tất cả các file .tmp trong thư mục
tmp_files = glob.glob(os.path.join(folder_path, '*.tmp'))
# Kiểm tra xem có file .tmp không
if tmp_files:
    newest_tmp_file = max(tmp_files, key=os.path.getctime)
    
import re

processed_text = ""
processed_text_2 = ""

with open(newest_tmp_file, 'r', encoding='utf-8') as file:
    for line in file:
        line = line[:line.rfind(',')] if ',' in line else line
        processed_text += line.strip() + "\n"

pattern = r'(\d{2}:\d{2} \d{2}/\d{2}/\d{4} \(\+10 phút\):.*?)(?=\d{2}:\d{2}|\Z)'
matches = re.findall(pattern, processed_text, re.DOTALL)

processed_text_2 = '\n'.join(matches)

# Loại bỏ các dòng trống (không có kí tự) trong processed_text_2
processed_text_2_lines = processed_text_2.split('\n')
processed_text_2 = '\n'.join(line for line in processed_text_2_lines if line.strip())
processed_text_2 = '\n'.join(line for line in processed_text_2_lines if ' (+10 phút)' not in line.strip())
province_districts = {}

# Tách dữ liệu thành các dòng
lines = processed_text_2.strip().split('\n')

# Xử lý từng dòng để tạo từ điển
for line in lines:
    district, province = line.split(', ')
    province = province.strip()  # Loại bỏ các khoảng trắng dư thừa
    if province in province_districts:
        province_districts[province].append(district)
    else:
        province_districts[province] = [district]

# In ra từ điển
specified_provinces = {'Lai Châu': [],'Điện Biên': [],'Sơn La': [],'Hòa Bình': [],'Lào Cai': [],'Yên Bái': []}
# Duyệt qua từng cặp key-value trong từ điển province_districts
for province, districts in province_districts.items():
    # Nếu tỉnh này nằm trong danh sách các tỉnh chỉ định
    if province in specified_provinces:
        specified_provinces[province] = districts
print(province_districts)
# In ra từ điển đã chỉ định
print(specified_provinces)



