# -*- coding: utf-8 -*-
"""Perio.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19iXIZU7FDWRhBhfGPayntIxL8-uvVXMP

Linear regression for periodontitis
"""

from google.colab import drive
#Mount drive to read database
drive.mount("/content/drive")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Import database
df_csv = pd.read_csv('/content/drive/MyDrive/Regresion_Perio.csv')

#Convert to numbers
df_csv.loc[(df_csv['GÉNERO'] == 'M') , 'GÉNERO'] = 1.0
df_csv.loc[(df_csv['GÉNERO'] == 'F') , 'GÉNERO'] = 0.0
df_csv.loc[(df_csv['DIABETES'] == 'SI') , 'DIABETES'] = 1.0
df_csv.loc[(df_csv['DIABETES'] == 'NO') , 'DIABETES'] = 0.0
df_csv.loc[(df_csv['HIPERTENSION'] == 'SI') , 'HIPERTENSION'] = 1.0
df_csv.loc[(df_csv['HIPERTENSION'] == 'NO') , 'HIPERTENSION'] = 0.0

df_csv.head()
df=df_csv
df=df_csv.apply(pd.to_numeric, errors="ignore")
df.dtypes

print(df)

#Correlation for %severity
df_corr = df.corr()
print(df_corr['%Seriedad'])

#sns.pairplot(df_corr)

class LinearModel:
    def __init__(self, num_features):
        self.num_features = num_features
        self.W = np.ones(num_features).reshape(num_features,1)
        self.b = 1
    
    def fowardPropagate(self, X):
        y = self.b + np.dot(X, self.W)
        return y
    
    def meanSquaredErrorDerivative(self, predY, targetY):
        loss = np.sum(np.square(predY - targetY))
        return loss/(2*predY.shape[0])
    
    def calculateGradients(self, X, targetY, predY):
        m = predY.shape[0]
        db = np.sum(predY - targetY)/m
        dW = np.sum(np.dot(np.transpose(predY - targetY), X), axis=0)/m
        return dW, db
    
    def update_W_and_b(self, dW, db, learnRate):
        self.W = self.W - learnRate * np.reshape(dW, (self.num_features, 1))
        self.b = self.b - learnRate * db
    
    def train(self, x_train, targetY, iterations, learnRate):
        losses = []
        loss = 100
        i = 0
        while loss > 0.2:
            predY = self.fowardPropagate(x_train)
            loss = self.meanSquaredErrorDerivative(predY, targetY)
            losses.append(loss)
            dW, db = self.calculateGradients(x_train, targetY, predY)
            self.update_W_and_b(dW, db, learnRate)
            i+=1
            if i == iterations:
                break
        return losses

from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import metrics

#get the fields of interest
dataX= df[['EDAD', 'DIABETES','HIPERTENSION', '%PLACA_BACTERIANA', 'SAS%']]
dataY = df[['%Seriedad']]
dataX.head()

#split dataset
X_train, X_test, y_train, y_test = train_test_split(dataX, dataY, train_size=0.70, random_state=198)

# Setup the data
X_train = X_train.values
y_train = np.reshape(y_train.values, (y_train.shape[0], 1))
X_test = X_test.values
y_test = np.reshape(y_test.values, (y_test.shape[0], 1))

#Create new model
model = LinearModel(5)

#Train the model
train = model.train(X_train, y_train, 1000, 0.000003)
plt.plot(train)
plt.show()

y_pred = model.fowardPropagate(X_test)
m = metrics.mean_squared_error(y_test,y_pred)
print('Mean Squared Error: %.2f' % np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
#model.meanSquaredErrorDerivative(y_pred, y_test)

plt.plot(range(len(y_test)), y_test, 'g.', label='Test', alpha=.8)
plt.plot(range(len(y_test)), y_pred, 'b.', label='Predictions',alpha=.8)
plt.legend()
plt.xlabel('Instance')
plt.ylabel('Performance')
plt.show()

#################
#Inputs for by hand model
#################

#print("Género 1.yes 0.no: ")
#Genero = float(input())

print("Age: ")
Edad = float(input())

print("Diabetes 1.yes 0.no: ")
Diabetes = float(input())

print("Hypertension 1.yes 0.no: ")
Hiper = float(input())

print("Plaque Accumulation(%): ")
PB = float(input())

print("Bleeding(%): ")
SAS = float(input())

y_predict = np.array([[Edad, Diabetes, Hiper, PB, SAS]])
y_predict = model.fowardPropagate(y_predict)

print(y_predict)
if y_predict < 17 :
  print("STAGE I: incipient periodontitis")
elif y_predict < 49 :
  print("STAGE II: moderate periodontitis")
elif y_predict < 81 :
  print("STAGE III: periodontitis with potential for additional tooth loss")
else :
  print("STAGE IV: advanced periodontitis with extensive tooth loss and potential loss of dentition")