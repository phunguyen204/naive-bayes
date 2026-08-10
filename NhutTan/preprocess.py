import re

class TienXuLyEmail:
    def __init__(self):
        pass

    def tach_tieu_de_va_noi_dung(self, raw_content):
        """Tach noi dung Email thanh Subject va Body"""
        # Chia Header va Body (2 dau xuong dong)
        parts = raw_content.split('\n\n', 1)
        
        header = parts[0]
        body = parts[1] if len(parts) == 2 else ""

        # Lay dong Subject tu Header
        subject = ""
        for line in header.split('\n'):
            if line.startswith("Subject:"):
                # Cat lay phan sau chu "Subject:" va xoa khoang trang thua
                subject = line.replace("Subject:", "").strip()
                break
                
        return subject, body

    def lam_sach_van_ban(self, text):
        """Thuc hien cac buoc lam sach chuoi van ban"""
        # 1. Chu thuong
        text = text.lower()
        # 2. Xoa HTML (bao gom cac khoi rac)
        text = re.sub(r'<head.*?>.*?</head>', ' ', text, flags=re.DOTALL)
        text = re.sub(r'<style.*?>.*?</style>', ' ', text, flags=re.DOTALL)
        text = re.sub(r'<script.*?>.*?</script>', ' ', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # 3. Thay URL
        text = re.sub(r'http[s]?://\S+', ' httpaddr ', text)
        
        # 4. Thay dia chi email
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' emailaddr ', text)
        
        # 5. Thay so
        text = re.sub(r'\b\d+\b', ' number ', text)
        
        # 6. Xoa dau cau (thay bang khoang trang)
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # 7. Xoa khoang trang thua (nhieu dau cach lien nhau)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def xu_ly_email(self, file_path):
        """Quy trinh tong the: Doc file -> Lay Subject & Body -> Clean -> Tokenize"""
        # Doc file bo qua loi encoding
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            return [] # Tra ve list rong neu loi doc
            
        # Tach Subject va Body
        subject, body = self.tach_tieu_de_va_noi_dung(content)
        
        # Ghep lai thanh 1 chuoi de xu ly chung
        full_text = subject + " " + body
        
        # Lam sach chuoi
        cleaned_text = self.lam_sach_van_ban(full_text)
        
        # Tach tu (Tokenize) - tach theo dau cach
        tokens = cleaned_text.split()
        
        return tokens

# Doan test nhanh neu chay truc tiep file nay
if __name__ == "__main__":
    test_email = (
        "Subject: BIG SALE 50%!!!\n\n"
        "Click here <a href='http://spam.com'>LINK</a> or email me at admin@spam.com. "
        "Don't miss 123 chances!!!"
    )
    
    # Ghi tam ra file de test ham xu_ly_email
    with open("test_email.txt", "w") as f:
        f.write(test_email)
        
    preprocessor = TienXuLyEmail()
    tokens = preprocessor.xu_ly_email("test_email.txt")
    print("Ket qua test tokenize:")
    print(tokens)
    
    import os
    os.remove("test_email.txt")
