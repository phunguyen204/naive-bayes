import os
import urllib.request
import tarfile

# 1. Tạo thư mục data/raw theo đúng cấu trúc 
DOWNLOAD_DIR = "data/raw"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 2. Link gốc từ máy chủ SpamAssassin (chọn bộ năm 2003 chuẩn nhất)
URLS = [
    "https://spamassassin.apache.org/old/publiccorpus/20030228_easy_ham.tar.bz2",
    "https://spamassassin.apache.org/old/publiccorpus/20030228_spam.tar.bz2"
]

def fetch_data(urls, download_dir):
    for url in urls:
        filename = url.split("/")[-1]
        filepath = os.path.join(download_dir, filename)
        
        # Tải tệp nếu chưa có
        if not os.path.isfile(filepath):
            print(f"Đang tải {filename} từ máy chủ...")
            urllib.request.urlretrieve(url, filepath)
            print(f"-> Tải xong {filename}!")
        else:
            print(f"File {filename} đã tồn tại, bỏ qua bước tải.")
            
        # Giải nén tệp .bz2
        print(f"Đang giải nén {filename}...")
        with tarfile.open(filepath, "r:bz2") as tar:
            tar.extractall(path=download_dir)
        print(f"-> Giải nén thành công vào {download_dir}/")

# Thực thi
fetch_data(URLS, DOWNLOAD_DIR)
print("Hoàn tất! Vào thư mục data/raw để xem thành quả.")