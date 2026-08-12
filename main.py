import numpy as np
from library.naive_bayes import MultinomialNaiveBayesFromScratch 
from Evaluation import ModelEvaluation
from Cross_validation import k_fold_cross_validation

X_train = np.load("data/X_train.npy")
Y_train= np.load("data/y_train.npy")

X_val = np.load("data/X_val.npy")
Y_val = np.load("data/y_val.npy")

X_test = np.load("data/X_test.npy")
Y_test = np.load("data/y_test.npy")

# Fold Cross Validation
cv_results = k_fold_cross_validation(
    X_train,
    Y_train,
    k=5,
    alpha=1.0,
    seed=42
)

print("\n===== DATA =====")
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

print("\n20 prediction đầu tiên của Validation:")
print(y_val_pred[:20])

print("\n20 nhãn thật của Validation:")
print(Y_val[:20])


print("\n20 prediction đầu tiên của Test:")
print(y_test_pred[:20])

print("\n20 nhãn thật của Test:")
print(Y_test[:20])

evaluation = ModelEvaluation(Y_test, y_test_pred)
evaluation.print_result("TEST")

val_evaluation = ModelEvaluation(Y_val, y_val_pred)
val_evaluation.print_result("VALIDATION")


