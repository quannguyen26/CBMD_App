import re

processed_text = ""
processed_text_2 = ""

with open('Warning_thunderstorm_202403051400.txt', 'r', encoding='utf-8') as file:
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

# In ra từ điển đã chỉ định
print(specified_provinces)
