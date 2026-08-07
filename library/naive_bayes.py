import numpy as np

class MultinomialNaiveBayesFromScratch:
    def __init__(self, alpha = 1.0):
        self.alpha = alpha

    def fit(self,X,y):
        """
        Train mô hình
        X: Matrix count word (n_samples, n_features)
        y: Labels (n_samples)
        """

        self.classes__ = np.unique(y)

        n_classes = len(self.classes__)

        n_features = X.shape[1]# Số cột

        # KHởi TẠO PRIOR P(CLASS)
        self.classes_log_prior_ = np.zeros(n_classes)

        # KHỞI TẠO PROB P(CLASS/FEATURE)
        self.features_log_prob_ = np.zeros((n_classes,n_features))        

        for idx,c in enumerate(self.classes__):
            X_c = X[y == c]

            # Tính log của prior
            self.classes_log_prior_ = np.log(X.shape[0]/X_c.shape[0])

            N_yi = X_c.sum(axis = 0) + self.alpha

            N_y = np.sum(N_yi)

            self.features_log_prob_[idx,:] = np.log(N_yi/N_y)

        return self

    def predict():
        pass

    def predict_log_proba():
        """
        Tránh trường hợp Overflow --> tràn số 
        """

        pass

