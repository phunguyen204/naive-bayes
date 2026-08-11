class ModelEvaluation:

    def __init__(self, y_true, y_pred):
        self.y_true = y_true
        self.y_pred = y_pred

        self.TN = 0
        self.FP = 0
        self.FN = 0
        self.TP = 0

        self._confusion_matrix()

    def _confusion_matrix(self):
        """Tinh TN, FP, FN, TP"""
        for true, pred in zip(self.y_true, self.y_pred):

            if true == 0 and pred == 0:
                self.TN += 1

            elif true == 0 and pred == 1:
                self.FP += 1

            elif true == 1 and pred == 0:
                self.FN += 1

            elif true == 1 and pred == 1:
                self.TP += 1

    def accuracy(self):
        total = (self.TN + self.FP + self.FN + self.TP)

        if total == 0:
            return 0
        return (self.TP + self.TN) / total

    def precision(self):
        if self.TP + self.FP == 0:
            return 0
        return self.TP / (self.TP + self.FP)

    def recall(self):
        if self.TP + self.FN == 0:
            return 0
        return self.TP / (self.TP + self.FN)

    def f1_score(self):
        precision = self.precision()
        recall = self.recall()

        if precision + recall == 0:
            return 0
        return (2 * precision * recall / (precision + recall))

    def specificity(self):
        if self.TN + self.FP == 0:
            return 0
        return self.TN / (self.TN + self.FP)

    def error_rate(self):
        total = (self.TN + self.FP + self.FN + self.TP)

        if total == 0:
            return 0
        return (self.FP + self.FN) / total

    def print_result(self, dataset_name="TEST"):

        print("\n" + "=" * 50)

        print(f"EVALUATION - {dataset_name}")

        print("=" * 50)

        print("\nConfusion Matrix:")

        print("                  Prediction")
        print("                 HAM      SPAM")

        print(
            f"Actual HAM       "
            f"{self.TN:<8} "
            f"{self.FP}"
        )

        print(
            f"Actual SPAM      "
            f"{self.FN:<8} "
            f"{self.TP}"
        )


        print("\nMetrics:")

        print(
            f"Accuracy   : "
            f"{self.accuracy() * 100:.2f}%"
        )

        print(
            f"Precision  : "
            f"{self.precision() * 100:.2f}%"
        )

        print(
            f"Recall     : "
            f"{self.recall() * 100:.2f}%"
        )

        print(
            f"F1-score   : "
            f"{self.f1_score() * 100:.2f}%"
        )

        print(
            f"Specificity: "
            f"{self.specificity() * 100:.2f}%"
        )

        print(
            f"Error Rate : "
            f"{self.error_rate() * 100:.2f}%"
        )