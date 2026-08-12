# ============================================================
# 5.1 Kiểm chứng chéo - 5-FOLD CROSS VALIDATION
#
# Mục đích:
# - Kiểm tra model có ổn định hay không
# - Chỉ sử dụng X_train, y_train
# - Không sử dụng Test trong Cross Validation
# - Không sử dụng sklearn
# ============================================================
import numpy as np
from library.naive_bayes import MultinomialNaiveBayesFromScratch
from Evaluation import ModelEvaluation

print("\n")
print("=" * 60)
print("5-FOLD CROSS VALIDATION")
print("=" * 60)


def k_fold_cross_validation(X, y, k=5, alpha=1.0, seed=42):

    # --------------------------------------------------------
    # Bước 1: Tạo danh sách index
    # --------------------------------------------------------

    indices = np.arange(len(X))

    # Đặt seed để mỗi lần chạy ra kết quả giống nhau
    np.random.seed(seed)

    # Trộn ngẫu nhiên dữ liệu
    np.random.shuffle(indices)

    # Chia dữ liệu thành K phần
    folds = np.array_split(indices, k)

    # Danh sách lưu kết quả từng Fold
    accuracy_scores = []
    precision_scores = []
    recall_scores = []
    f1_scores = []

    # --------------------------------------------------------
    # Bước 2: Chạy từng Fold
    # --------------------------------------------------------

    for fold in range(k):

        # Fold hiện tại được dùng để Validation
        val_indices = folds[fold]

        # Các Fold còn lại được dùng để Train
        train_indices = np.concatenate(
            [
                folds[i]
                for i in range(k)
                if i != fold
            ]
        )

        # Tạo dữ liệu Train của Fold
        X_train_fold = X[train_indices]
        y_train_fold = y[train_indices]

        # Tạo dữ liệu Validation của Fold
        X_val_fold = X[val_indices]
        y_val_fold = y[val_indices]

        # ----------------------------------------------------
        # Bước 3: Tạo model mới cho từng Fold
        # ----------------------------------------------------

        cv_model = MultinomialNaiveBayesFromScratch(
            alpha=alpha
        )

        # Train model
        cv_model.fit(
            X_train_fold,
            y_train_fold
        )

        # Dự đoán trên Fold Validation
        y_pred_fold = cv_model.predict(
            X_val_fold
        )

        # ----------------------------------------------------
        # Bước 4: Evaluation từng Fold
        # ----------------------------------------------------
        evaluation = ModelEvaluation(
            y_val_fold,
            y_pred_fold
        )

        accuracy = evaluation.accuracy()
        precision = evaluation.precision()
        recall = evaluation.recall()
        f1 = evaluation.f1_score()

        # Lưu kết quả
        accuracy_scores.append(accuracy)
        precision_scores.append(precision)
        recall_scores.append(recall)
        f1_scores.append(f1)


        # In kết quả từng Fold
        print(f"\nFold {fold + 1}")

        print(f"Accuracy : {accuracy:.4f}")

        print(f"Precision: {precision:.4f}")

        print(f"Recall   : {recall:.4f}")

        print(f"F1-score : {f1:.4f}")

    # --------------------------------------------------------
    # Bước 5: Tính giá trị trung bình
    # --------------------------------------------------------

    mean_accuracy = np.mean(accuracy_scores)

    mean_precision = np.mean(precision_scores)

    mean_recall = np.mean(recall_scores)

    mean_f1 = np.mean(f1_scores)

    # --------------------------------------------------------
    # Bước 6: Tính độ lệch chuẩn
    # --------------------------------------------------------

    std_accuracy = np.std(accuracy_scores)

    std_precision = np.std(precision_scores)

    std_recall = np.std(recall_scores)

    std_f1 = np.std(f1_scores)

    # --------------------------------------------------------
    # Bước 7: In kết quả tổng hợp
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("KẾT QUẢ TRUNG BÌNH 5-FOLD CROSS VALIDATION")
    print("=" * 60)

    print(
        f"Accuracy : "
        f"{mean_accuracy:.4f} "
        f"+/- {std_accuracy:.4f}"
    )

    print(
        f"Precision: "
        f"{mean_precision:.4f} "
        f"+/- {std_precision:.4f}"
    )

    print(
        f"Recall   : "
        f"{mean_recall:.4f} "
        f"+/- {std_recall:.4f}"
    )

    print(
        f"F1-score : "
        f"{mean_f1:.4f} "
        f"+/- {std_f1:.4f}"
    )


    # --------------------------------------------------------
    # Bước 8: Đánh giá độ ổn định của Model
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("ĐÁNH GIÁ ĐỘ ỔN ĐỊNH MODEL")
    print("=" * 60)


    if std_f1 < 0.02:

        print("Model có độ ổn định TỐT.")

        print(
            "F1-score giữa các Fold "
            "có độ chênh lệch rất nhỏ."
        )


    elif std_f1 < 0.05:

        print("Model có độ ổn định KHÁ.")

        print(
            "F1-score giữa các Fold "
            "có một số chênh lệch nhỏ."
        )


    else:

        print("Model CHƯA THỰC SỰ ỔN ĐỊNH.")

        print(
            "F1-score có sự biến động "
            "khá lớn giữa các Fold."
        )


    # Trả về kết quả để có thể sử dụng sau này
    return {
        "accuracy_mean": mean_accuracy,
        "accuracy_std": std_accuracy,

        "precision_mean": mean_precision,
        "precision_std": std_precision,

        "recall_mean": mean_recall,
        "recall_std": std_recall,

        "f1_mean": mean_f1,
        "f1_std": std_f1
    }


