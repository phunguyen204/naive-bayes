import numpy as np

class MultinomialNaiveBayesFromScratch:
    def __init__(self, alpha = 1.0):
        self.alpha = alpha # Zero Frequency
        self.classes__ = None
        self.classes_log_prior_ = None
        self.features_log_prob_ = None

    def _check_inputs(self,X,y = None):
        #1. Kiểm tra X phải numpy array k --> ép kiểu qua 
        if not isinstance(X,np.ndarray):
            X = np.array(X)

        #2. check xem X có âm hay không vì xác xuất không thể có thể âm đc
        if ((X < 0).any()):
            raise ValueError("Kiểm tra lại ma trận X. Đang xuất hiện số âm")

        # 3. Kiểm tra y nếu y != None
        if y is not None:
            # kiểm tra và ép y sang --> array
            if not isinstance(y,np.ndarray):
                y = np.array(y)
            # Kiểm tra số dòng của X = số cột của y không
            if X.shape[0] != y.shape[0]:
                raise ValueError(f"Số lượng không khớp. Mẫu X: {X.shape[0]} và nhãn y: {y.shape[0]}")
            
            return X,y
        return X

    def fit(self,X,y):
        """
        Train mô hình
        X: Matrix count word (n_samples, n_features)
        y: Labels (n_samples)
        """
        X,y = self._check_inputs(X,y)
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
            self.classes_log_prior_[idx] = np.log(X_c.shape[0]/X.shape[0])

            N_yi = X_c.sum(axis = 0) + self.alpha

            N_y = np.sum(N_yi)

            self.features_log_prob_[idx,:] = np.log(N_yi/N_y)

        return self

    def predict_log_proba(self, X_predict):
        """
        Tránh trường hợp Overflow --> tràn số 
        """
        X_predict = self._check_inputs(X_predict)
        log_proby = X_predict @ (self.features_log_prob_).T + self.classes_log_prior_

        return log_proby

    def predict(self, X_predict):

        log_proby = self.predict_log_proba(X_predict)

        best_classes_indies = np.argmax(a = log_proby,axis = 1)

        return self.classes__[best_classes_indies]
