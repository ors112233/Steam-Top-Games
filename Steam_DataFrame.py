import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
import sklearn
from sklearn import linear_model, metrics, preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def DataCleaning (Df:DataFrame):
    Temp_Df = Df.copy()
    Temp_Df.dropna(inplace=True)
    Temp_Df.drop_duplicates(inplace=True)
    Temp_Df.drop(columns='Name',inplace=True)
    dateList = []
    for date in Temp_Df['Date']:
        date = date.replace('Jan','1')
        date = date.replace('Feb','2')
        date = date.replace('Mar','3')
        date = date.replace('Apr','4')
        date = date.replace('May','5')
        date = date.replace('Jun','6')
        date = date.replace('Jul','7')
        date = date.replace('Aug','8')
        date = date.replace('Sep','9')
        date = date.replace('Oct','10')
        date = date.replace('Nov','11')
        date = date.replace('Dec','12')
        date = date.replace(' ','')
        date = date.replace(',','')
        dateList.append(date)
    Temp_Df['Date'] = dateList
    Temp_Df['Date'] = Temp_Df['Date'].astype(int)
    col = ['Developer','Publisher','Genre','Langs']
    for i in col:
        Temp_Df[i] = LabelEncoder().fit_transform(Temp_Df[i])
    return Temp_Df
def split_to_train_and_test(dataset:DataFrame, label_column):
    y = dataset[label_column]
    X = dataset.drop(columns = label_column)
    X_train,X_test,y_train,y_test = train_test_split(X,y)
    return X_train, X_test, y_train, y_test
def train_1st_model(X_train, y_train):
    trained_model=linear_model.LinearRegression().fit(X_train,y_train)
    return trained_model   
def predict_1st(trained_1st_model, X_test):
    predicted_vals = trained_1st_model.predict(X_test)
    return predicted_vals
def evaluate_performance_1st(y_test,y_predicted):
    evaluate_value = r2_score(y_test,y_predicted)
    return evaluate_value

if __name__ == '__main__':
    dataset = pd.read_csv('D:\Python projects\Steam - Visual\SteamGamesDF.csv',index_col=0)
    cleaned_dataset  = DataCleaning(dataset)
    X_train, X_test, y_train, y_test = split_to_train_and_test(cleaned_dataset,'Score')
    trained_model = train_1st_model(X_train,y_train)
    y_predicted = predict_1st(trained_model,X_test)
    evaluate_value = evaluate_performance_1st(y_test,y_predicted)
    print(evaluate_value)