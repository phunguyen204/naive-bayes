import os
import json
import csv
import sys
# Them thu muc hien tai vao duong dan de import module preprocess
sys.path.append(os.path.dirname(__file__))


from preprocess import TienXuLyEmail

class XayDungTuDien:
    def __init__(self, min_df=5, max_df_ratio=0.8):
        """Khoi tao tham so loc tu"""
        self.min_df = min_df
        self.max_df_ratio = max_df_ratio
        self.vocab = {}
        self.preprocessor = TienXuLyEmail()

    def tao_tu_dien(self, train_files_csv, output_vocab_json):
        # 1. Doc danh sach file Train tu CSV
        train_files = []
        with open(train_files_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Bo qua dong tieu de
            for row in reader:
                train_files.append(row[0])
            
        total_docs = len(train_files)
        print(f"Bat dau xay dung tu dien tu {total_docs} file train...")
        
        # Dem tan suat
        doc_freq = {}
        
        # 2. Xu ly tung file de dem
        for file_path in train_files:
            # GỌI TIỀN XỬ LÝ (TỪ FILE preprocess.py): 
            # Gọi hàm xu_ly_email để dọn rác HTML (xóa head, style, script) và lấy danh sách chữ
            tokens = self.preprocessor.xu_ly_email(file_path)
            # Lay tu duy nhat trong email
            unique_tokens = []
            for token in tokens:
                if token not in unique_tokens:
                    unique_tokens.append(token)
            
            for token in unique_tokens:
                if token in doc_freq:
                    doc_freq[token] += 1
                else:
                    doc_freq[token] = 1
            
        # 3. Loc tu vung
        max_df = total_docs * self.max_df_ratio
        valid_words = []
        
        for word, count in doc_freq.items():
            if self.min_df <= count <= max_df:
                valid_words.append(word)
                
        # 4. Gan index (0 cho <UNK>)
        self.vocab = {"<UNK>": 0}
        
        for idx, word in enumerate(sorted(valid_words), start=1):
            self.vocab[word] = idx
            
        # 5. Luu tu dien
        with open(output_vocab_json, 'w', encoding='utf-8') as f:
            json.dump(self.vocab, f, ensure_ascii=False, indent=4)
            
        print("=== BAO CAO TU DIEN ===")
        print(f"Tong so tu thu thap: {len(doc_freq)}")
        print(f"So tu giu lai sau khi loc: {len(valid_words)}")
        print(f"Kich thuoc Vocabulary (tinh ca <UNK>): {len(self.vocab)}")
        print(f"Luu thanh cong tai: {output_vocab_json}")


if __name__ == "__main__":
    builder = XayDungTuDien(min_df=5, max_df_ratio=0.5)
    builder.tao_tu_dien(
        train_files_csv="../data/train_files.csv",
        output_vocab_json="../data/vocabulary.json"
    )
