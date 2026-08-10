import os
import re
from collections import Counter
import matplotlib.pyplot as plt

# 1. Hàm đọc dữ liệu và trích xuất đặc trưng cơ bản
def load_and_extract(folder_path):
    lengths = []
    all_words = []
    
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Tách phần body
                parts = content.split('\n\n', 1)
                if len(parts) == 2:
                    body = parts[1]
                    lengths.append(len(body))
                    # Lọc lấy các từ tiếng Anh (bỏ qua dấu câu, số)
                    words = re.findall(r'\b[a-zA-Z]{3,}\b', body.lower())
                    all_words.extend(words)
    return lengths, all_words

print("Đang đọc và phân tích dữ liệu")
ham_lengths, ham_words = load_and_extract("data/raw/easy_ham")
spam_lengths, spam_words = load_and_extract("data/raw/spam")

# 2. Chuẩn bị khung vẽ biểu đồ (1 hàng, 3 cột)
plt.figure(figsize=(15, 5))

# Biểu đồ 1: Phân bố nhãn
plt.subplot(1, 3, 1)
labels = ['Ham', 'Spam']
counts = [len(ham_lengths), len(spam_lengths)]
plt.bar(labels, counts, color=['#4CAF50', '#F44336'])
plt.title('Phân bố nhãn dữ liệu')
plt.ylabel('Số lượng Email')
for i, v in enumerate(counts):
    plt.text(i, v + 20, str(v), ha='center', fontweight='bold')

# Biểu đồ 2: Phân bố độ dài email (dùng Boxplot)
plt.subplot(1, 3, 2)
plt.boxplot([ham_lengths, spam_lengths], tick_labels=['Ham', 'Spam'])
plt.title('Độ dài nội dung Email (Ký tự)')
plt.yscale('log') # Dùng log scale vì có những email cực kỳ dài
plt.ylabel('Log(Số ký tự)')

# Biểu đồ 3: Top 10 từ phổ biến nhất trong nhóm SPAM
# Loại bỏ một số stop-words cơ bản để biểu đồ có ý nghĩa hơn
stop_words = {'the', 'and', 'that', 'this', 'for', 'with', 'you', 'have', 'from', 'are', 'not', 'your', 'all', 'out', 'will', 'can', 'has'}
spam_filtered = [w for w in spam_words if w not in stop_words]
top_spam = Counter(spam_filtered).most_common(10)
words_spam, counts_spam = zip(*top_spam)

plt.subplot(1, 3, 3)
plt.barh(words_spam, counts_spam, color='#F44336')
plt.title('Top 10 từ xuất hiện nhiều nhất trong SPAM')
plt.xlabel('Tần suất')
plt.gca().invert_yaxis() # Đảo ngược trục Y để từ nhiều nhất lên đầu

plt.tight_layout()
plt.show()