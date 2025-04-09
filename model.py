# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Load the Dataset
df = pd.read_excel("drop out data.xlsx")

# Handle Missing Values
print(df.isnull().sum())

# Filling missing numerical values with mean
df.fillna(df.mean(numeric_only=True), inplace=True)

# Filling missing categorical values with mode
for column in df.select_dtypes(include='object').columns:
    df[column].fillna(df[column].mode()[0], inplace=True)

# Encoding Categorical Variables
encoder = LabelEncoder()
for column in df.select_dtypes(include='object').columns:
    df[column] = encoder.fit_transform(df[column])

# Feature Scaling
scaler = StandardScaler()
numerical_columns = df.select_dtypes(include=np.number).columns.tolist()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# Splitting Data
X = df.drop("dropout", axis=1)
y = df["dropout"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
model = RandomForestClassifier()
model.fit(X_train, y_train)

# GUI using Tkinter
def predict_dropout():
    try:
        inputs = [float(entry.get()) for entry in entries]
        inputs = np.array(inputs).reshape(1, -1)
        inputs = scaler.transform(inputs)
        prediction = model.predict(inputs)[0]
        result = "Likely to Dropout" if prediction == 1 else "Unlikely to Dropout"
        messagebox.showinfo("Prediction", result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create GUI
root = tk.Tk()
root.title("Dropout Prediction")

labels = X.columns.tolist()
entries = []

for idx, label in enumerate(labels):
    lbl = ttk.Label(root, text=label)
    lbl.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
    entry = ttk.Entry(root)
    entry.grid(row=idx, column=1, padx=10, pady=5)
    entries.append(entry)

btn = ttk.Button(root, text="Predict", command=predict_dropout)
btn.grid(row=len(labels), column=0, columnspan=2, pady=20)

root.mainloop()
