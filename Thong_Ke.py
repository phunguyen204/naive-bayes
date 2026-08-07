import os

def analyze_email_data(folder_path, label):
    # Lấy danh sách tất cả các file trong thư mục
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total_files = len(files)
    print(f"Tổng số email {label}: {total_files} file")
    
    if total_files == 0:
        return
        
    # Lấy thử 1 file đầu tiên để tách Body
    sample_file = os.path.join(folder_path, files[0])
    with open(sample_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Trong email chuẩn, Header và Body luôn được ngăn cách bởi 2 ký tự xuống dòng liên tiếp (\n\n)
    parts = content.split('\n\n', 1) 
    
    if len(parts) == 2:
        header, body = parts
        print(f"--- Trích xuất Body mẫu từ {label} ---")
        # In thử 150 ký tự đầu tiên của phần Body
        print(body[:150] + "...\n(Đã cắt bớt)\n")
    else:
        print(f"--- File này có cấu trúc bất thường, không tìm thấy Body! ---\n")

# Đường dẫn tới 2 thư mục dữ liệu em vừa tải về
ham_dir = "data/raw/easy_ham"
spam_dir = "data/raw/spam"

print("=== BÁO CÁO THỐNG KÊ DỮ LIỆU ===")
analyze_email_data(ham_dir, "HAM")
analyze_email_data(spam_dir, "SPAM")