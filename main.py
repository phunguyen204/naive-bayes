import numpy as np
from library.naive_bayes import MultinomialNaiveBayesFromScratch

X = np.array([
    [2,1,0,0],
    [1,1,1,0],
    [0,0,2,3],
    [5,0,1,0]
    ])

y = np.array([0,0,1,1])

model = MultinomialNaiveBayesFromScratch()

model.fit(X,y)
print(f"fearures log: {model.features_log_prob_}\n")
print(f"classes log prior: {model.classes_log_prior_}")
X_predict = np.array([[1,0,4,7]])
predict = model.predict(X_predict=X_predict)

print(predict)