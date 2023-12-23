import requests

url = 'http://hymetnet.gov.vn/radar/Warning_thunderstorm_202312222140.txt'

response = requests.get(url)

if response.status_code == 200:
    with open('Warning_thunderstorm_202312222140.txt', 'wb') as file:
        file.write(response.content)
        print("Tệp tin đã được tải xuống thành công.")
else:
    print("Đã xảy ra lỗi trong quá trình tải xuống.")
import requests

url = 'http://hymetnet.gov.vn/radar/Warning_thunderstorm_202312222140.txt'

response = requests.get(url)

if response.status_code == 200:
    with open('Warning_thunderstorm_202312222140.txt', 'wb') as file:
        file.write(response.content)
        print("Tệp tin đã được tải xuống thành công.")
else:
    print("Đã xảy ra lỗi trong quá trình tải xuống.")
