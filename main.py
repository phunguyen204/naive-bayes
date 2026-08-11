import numpy as np
from library.naive_bayes import MultinomialNaiveBayesFromScratch 
from Evaluation import ModelEvaluation

X_train = np.load("data/X_train.npy")
Y_train= np.load("data/y_train.npy")

X_val = np.load("data/X_val.npy")
Y_val = np.load("data/y_val.npy")

X_test = np.load("data/X_test.npy")
Y_test = np.load("data/y_test.npy")

print("=== DATA ===")
print("X_train:", X_train.shape)
print("Y_train:",Y_train.shape)

print("X_val:", X_val.shape)
print("Y_val:", Y_val.shape)

print("X_test:", X_test.shape)
print("Y_test:", Y_test.shape)

#Create model
model = MultinomialNaiveBayesFromScratch(alpha=1.0)

#Train model
model.fit(X_train, Y_train)
print("Train model thanh cong!")

#predict
y_val_pred = model.predict(X_val)
y_test_pred = model.predict(X_test)

evaluation = ModelEvaluation(Y_test, y_test_pred)
evaluation.print_result("TEST")

val_evaluation = ModelEvaluation(Y_val, y_val_pred)
val_evaluation.print_result("VALIDATION")


