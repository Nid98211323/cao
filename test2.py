#API
import xmlrpc.client

#LẤY NỘI DUNG BÀI VIẾT
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost
from wordpress_xmlrpc.methods.media import UploadFile
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.methods.media import GetMediaItem
import requests
import sys
# Thiết lập kết nối đến trang web WordPress của bạn
wordpress_sites = ['https://clipviet69.com/xmlrpc.php']
username = 'alovn'
password = 'huyvip98'
for site in wordpress_sites:
    try:
        client = Client(site, username, password)
        print('Kết nối thành công')
    except Exception as e:
        print('Kết nối thất bại với Server:', e)
        sys.exit()

#Bắt đầu lấy nội dung
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
# khai báo thông tin đăng nhập và URL của WordPress

# tạo client để kết nối tới WordPress và #kiểm tra kết nối
wp = xmlrpc.client.ServerProxy(site)
try:
    print('Kết nối thành công')
except Exception as e:
    print('Kết nối thất bại với Server:', e)
    sys.exit()
posts = wp.wp.getPosts(1, username, password, {'number': 0})
# sử dụng Selenium để lấy đường dẫn đến bài viết
driver = webdriver.Chrome('E:\CODE\viet69lol\chromedriver.exe',chrome_options=options)



driver.get('http://viet69.love')
url = driver.current_url

# truy cập vào trang chi tiết bài viết và lấy nội dung
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
#post.title = soup.find('div', {'class': 'thumb'}).text.strip()

title_tags = soup.find_all('a', {'class': 'clip-link'})
  

# Kiểm tra trùng lặp và ghi log
log_file = open('log.txt', 'a+')
log_file.seek(0)
log_content = log_file.read()
log_file.seek(0, 2)

for title_tag in reversed(title_tags):
    title = title_tag.get('title')
    link = title_tag.get('href')
    img = title_tag.find('img').get('src')
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tukhoa= []
    tags = driver.find_elements(By.XPATH, ".//div[@id='details']/a")
    for tag in tags:
        tukhoa.append(tag.text)
    
    try:
        if driver.find_element(By.CLASS_NAME, "movieLoader iframe").is_displayed():
            print("Đã tìm thấy video")
            print("-----------------------------------------")
            embed = driver.find_element(By.CLASS_NAME, "movieLoader iframe").get_attribute('src')
            
                
    except:
        print("Không tìm thấy video")
    # Kiểm tra trùng lặp 
    if log_content.find(link) != -1:
        print('Bài viết đã có trên server.')
        continue

    # Tạo bài viết mới và lưu ảnh đại diện
    post = WordPressPost()
    post.title = title
    post.content = ''
    post.post_status = 'publish'
    post.terms_names = {
    'category': ['Clip Sex Việt Nam – Phim sex Việt Nam'],
    'post_tag': tukhoa
}

    # Tải xuống ảnh từ URL
    image_url = img
    image_content = requests.get(image_url).content

    # Upload ảnh lên trang WordPress
    data = {
        'name': f'{title}.jpg',
        'type': 'image/jpeg',
        'bits': image_content,
        'overwrite': True
    }
    response = client.call(media.UploadFile(data))
    print ("Đã tải ảnh lên server", response['id'], "")

    # Lưu ảnh đại diện cho bài viết
    post.thumbnail = response['id']
    # Lấy ID của ảnh đại diện của bài viết
    thumbnailid = post.thumbnail
    # Lấy thông tin ảnh đại diện
    attachment = client.call(GetMediaItem(thumbnailid))
    # Lấy URL của ảnh đại diện
    thumbnail_url = attachment.link
    # Đăng bài viết lên trang WordPress
    post.custom_fields = [
    {'key': 'embed', 'value': f'<iframe id="playerV4_1" src="{embed}" width="640" height="480" allowfullscreen=""></iframe>'},
    {'key': 'thumb', 'value': thumbnail_url},
    {'key': 'thumbs', 'value': thumbnail_url},
    {'key': 'hd_video', 'value': 'on'}
]
    post_id = client.call(NewPost(post))
 
    
    # Kiểm tra xem bài viết đã được tạo thành công hay chưa
    if post_id:
        print('Đã tạo bài viết :', post.title)

        # Ghi log vào file
        log_file.write(link + '\n')
        log_file.flush()
    else:
        print('Lỗi không thể tạo liên hệ Niddz.')
        
log_file.close()

# Đóng trình duyệt
driver.close()

#xóa log
import os
import datetime

log_filename = "log.txt"

if os.path.isfile(log_filename):
    # Tính toán ngày hiện tại và ngày 7 ngày trước đó
    now = datetime.datetime.now()
    ago = now - datetime.timedelta(days=7)

    # Lấy thông tin thời gian của file log
    log_timestamp = os.path.getctime(log_filename)
    log_time = datetime.datetime.fromtimestamp(log_timestamp)

    # Nếu file log được tạo trước 7 ngày thì xóa nó
    if log_time < ago:
        os.remove(log_filename)
        print("Xóa file log thành công")
    else:
        print("--------------------------------------")
        print("Chưa đến ngày xóa log")
else:
    print("Không tìm thấy file log")


