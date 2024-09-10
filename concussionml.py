import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from autosklearn.classification import AutoSklearnClassifier

# Load the dataset and skip the first row
dataset = pd.read_csv('C:/Users/kapad/Downloads/concussion.csv', skiprows=[0])

# Drop rows with missing values
dataset = dataset.dropna()

# Data preprocessing
X = dataset.iloc[:, 1:-1]  # Features (all columns except the first and last ones)
y = dataset.iloc[:, -1]   # Target variable (last column)

# Map unique values to expected range
label_mapping = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
y = y.map(label_mapping)

# Data encoding
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)  # Encode target variable to numerical values

# Convert features and target to numpy arrays
X = X.values
y = np.array(y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=None)

# AutoML model training
automl = AutoSklearnClassifier(time_left_for_this_task=3600)  # Adjust time limit as needed
automl.fit(X_train, y_train)

# Model evaluation
y_pred = automl.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')
f1 = f1_score(y_test, y_pred, average='macro')

print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1 Score:', f1)
