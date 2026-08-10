import os
import csv
import random


class ChiaDuLieu:
    def __init__(self, raw_data_dir, output_dir, train_ratio=0.7, val_ratio=0.15):
        self.raw_data_dir = raw_data_dir
        self.output_dir = output_dir
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        
        # Dam bao thu muc output ton tai
        os.makedirs(self.output_dir, exist_ok=True)

    def _lay_file_theo_nhan(self):
        """Lay file theo nhan (ham/spam)"""
        label_files = {}
        label_files['ham'] = []
        label_files['spam'] = []
        
        # Cac thu muc con tuong ung voi nhan
        label_dirs = {
            'ham': 'easy_ham',
            'spam': 'spam'
        }
        
        for label, dir_name in label_dirs.items():
            dir_path = os.path.join(self.raw_data_dir, dir_name)
            if not os.path.exists(dir_path):
                continue
                
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path):
                    label_files[label].append(file_path)
                    
        return label_files

    def chia_va_luu(self, seed=42):
        """Chia du lieu va luu CSV"""
        # Set random seed
        random.seed(seed)
        
        label_files = self._lay_file_theo_nhan()
        
        train_files, val_files, test_files = [], [], []
        
        # Chia theo ty le
        for label, files in label_files.items():
            random.shuffle(files)
            
            total = len(files)
            train_end = int(total * self.train_ratio)
            val_end = train_end + int(total * self.val_ratio)
            
            train_files.extend(files[:train_end])
            val_files.extend(files[train_end:val_end])
            test_files.extend(files[val_end:])
            
            print(f"Nhan [{label.upper()}]: Tong {total} -> Train: {train_end}, Val: {val_end - train_end}, Test: {total - val_end}")

        # Tron ngau nhien lai tap tong hop
        random.shuffle(train_files)
        random.shuffle(val_files)
        random.shuffle(test_files)

        # Luu danh sach file
        self._luu_csv(train_files, "train_files.csv")
        self._luu_csv(val_files, "val_files.csv")
        self._luu_csv(test_files, "test_truoc_khi_xu_ly.csv")
        
        print("\nDa luu danh sach file thanh cong!")

    def _luu_csv(self, data_list, filename):
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # Ghi tieu de
            writer.writerow(["DuongDan", "Nhan"])
            
            # Ghi tung dong
            for path in data_list:
                if "/spam/" in path or "\\spam\\" in path:
                    label = "spam"
                else:
                    label = "ham"
                writer.writerow([path, label])
                
        print(f" - Da luu {len(data_list)} duong dan vao {file_path}")


if __name__ == "__main__":
    # Khoi tao class chia du lieu
    splitter = ChiaDuLieu(
        raw_data_dir="../data/raw", 
        output_dir="../data",
        train_ratio=0.7, 
        val_ratio=0.15 # Ty le Test tu tinh
    )
    
    print("=== BAT DAU CHIA DU LIEU TU THU MUC RAW ===")
    splitter.chia_va_luu(seed=2024)
