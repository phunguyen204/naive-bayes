import json
import csv
import numpy as np
import sys
import os

# Them thu muc hien tai vao duong dan de import module preprocess
sys.path.append(os.path.dirname(__file__))
from preprocess import TienXuLyEmail

class BieuDienBagOfWords:
    def __init__(self, vocab_json):
        """Khoi tao voi Tu dien co san"""
        with open(vocab_json, 'r', encoding='utf-8') as f:
            self.vocab = json.load(f)
            
        self.vocab_size = len(self.vocab)
        self.preprocessor = TienXuLyEmail()
        self.unk_idx = self.vocab.get("<UNK>", 0)

    def chuyen_file_thanh_vector(self, files_csv):
        """Chuyen file thanh X va y"""
        file_paths = []
        with open(files_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # bo qua tieu de
            for row in reader:
                file_paths.append(row[0])
            
        n_samples = len(file_paths)
        
        # Tao ma tran X, y
        X = np.zeros((n_samples, self.vocab_size), dtype=np.int32)
        y = np.zeros(n_samples, dtype=np.int32)
        
        print(f"Dang vector hoa {n_samples} file...")
        
        for i, file_path in enumerate(file_paths):
            # 1. Lay token
            # GỌI TIỀN XỬ LÝ (TỪ FILE preprocess.py): 
            # Gọi hàm xu_ly_email để dọn rác HTML (xóa head, style, script) và lấy danh sách chữ
            tokens = self.preprocessor.xu_ly_email(file_path)
            
            # 2. Tao vector dem
            for token in tokens:
                # Lay index cua tu, hoac <UNK>
                if token in self.vocab:
                    idx = self.vocab[token]
                else:
                    idx = self.unk_idx
                    
                X[i, idx] += 1
                
            # 3. Gan nhan
            if "/spam/" in file_path or "\\spam\\" in file_path:
                y[i] = 1
            else:
                y[i] = 0
                
        return X, y

if __name__ == "__main__":
    vectorizer = BieuDienBagOfWords(vocab_json="../data/vocabulary.json")
    
    # Vectorize tung tap du lieu va luu lai
    splits = [
        ("Train", "../data/train_files.csv", "../data/X_train.npy", "../data/y_train.npy"),
        ("Validation", "../data/val_files.csv", "../data/X_val.npy", "../data/y_val.npy"),
        ("Test", "../data/test_truoc_khi_xu_ly.csv", "../data/X_test.npy", "../data/y_test.npy"),
    ]
    
    for name, csv_path, x_path, y_path in splits:
        print(f"--- Dang xu ly tap {name} ---")
        X, y = vectorizer.chuyen_file_thanh_vector(csv_path)
        
        # Luu vao file numpy
        np.save(x_path, X)
        np.save(y_path, y)
        print(f"-> Hoan tat tap {name}. Shape X: {X.shape}, Shape y: {y.shape}")
