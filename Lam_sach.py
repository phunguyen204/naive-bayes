import os
import csv

def clean_and_log(folder_path, label, log_writer):
    # Lấy danh sách file
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    valid_count = 0
    removed_count = 0
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        
        # Tiêu chí 1: Bị lẫn file hệ thống 'cmds' của máy chủ
        if file == 'cmds':
            log_writer.writerow([file, label, "File hệ thống (không phải cấu trúc email)"])
            os.remove(file_path) # Xóa file rác khỏi tập dữ liệu
            removed_count += 1
            continue
            
        # Tiêu chí 2: File rỗng (không có byte dữ liệu nào)
        if os.path.getsize(file_path) == 0:
            log_writer.writerow([file, label, "File rỗng (0 KB)"])
            os.remove(file_path)
            removed_count += 1
            continue
            
        valid_count += 1
        
    print(f"[{label}] Giữ lại: {valid_count} file | Đã loại bỏ: {removed_count} file")

# Tạo và mở file CSV để ghi nhật ký (log)
log_file = "cleaning_log.csv"
with open(log_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    # Viết dòng tiêu đề cho bảng
    writer.writerow(["Tên file", "Nhãn", "Lý do loại bỏ"]) 
    
    print("=== BẮT ĐẦU LÀM SẠCH DỮ LIỆU ===")
    clean_and_log("data/raw/easy_ham", "HAM", writer)
    clean_and_log("data/raw/spam", "SPAM", writer)
    
print(f"\n-> Hoàn tất! Đã xuất nhật ký làm sạch ra tệp: {log_file}")