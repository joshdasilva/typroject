#Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import CuDNNLSTM   #nvidia cudnn
from keras.layers import Dropout
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import requests

def getStockdata(stock):
    data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stock+'&outputsize=full&apikey=ZCXPM8FMBJXNOE3J&datatype=csv')
    with open('csvFiles/'+stock+'.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        reader = csv.reader(data.text.splitlines())
        for row in reader:
            writer.writerow(row)
            
stock = ["AAPL" , "MSFT" , "AMZN" , "FB" , "BRK.B" , "GOOG" , "XOM" , "JPM" , "V" , "BAC" , "INTC" , "CSCO" , "VZ" , "PFE" , "T" , "MA" , "BA" , "DIS" , "KO" , "PEP" , "NFLX" , "MCD" , "WMT" , "ORCL" , "IBM" , "PYPL" , "MMM" , "NVDA" , "NKE" , "COST" , "QCOM" ]

for i in range(len(stock)):
    getStockdata(stock[i]),
			
#stock = ["FB" ,  "GOOG" , "PYPL" ] #smaller than 980
#stock = ["AAPL" , "MSFT" , "AMZN" , "BRK.B" , "XOM" , "JPM" , "V" , "BAC" , "INTC" , "CSCO" , "VZ" , "PFE" , "T" , "MA" , "BA" , "DIS" , "KO" , "PEP" , "NFLX" , "MCD" , "WMT" , "ORCL" , "IBM" , "MMM" , "NVDA" , "NKE" , "COST" , "QCOM" ] #without goog, fb and pypl

for x in range(len(stock)):
    # Reading the csv file using pandas library
    data_val = pd.read_csv('csvFiles/'+stock[x]+'.csv') 
    pre_process_data = data_val.loc['0':'2731']
    dataset_train = pre_process_data.sort_index(ascending=False)
	#get the training set from the close column
    training_set = dataset_train.iloc[:, 4:5].values
	#test set 
    dataset_test = dataset_train.tail(15)

    # Feature Scaling
    from sklearn.preprocessing import MinMaxScaler
    sc = MinMaxScaler(feature_range = (0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # Creation of a data structure with 1 output and 60 timesteps
    xtrain = []
    ytrain = []
    for i in range(60, 2035):
        xtrain.append(training_set_scaled[i-60:i, 0])   #60 time steps
        ytrain.append(training_set_scaled[i, 0])
    xtrain, ytrain = np.array(xtrain), np.array(ytrain)

    # Reshaping the array 
    i=0
    xtrain = np.reshape(xtrain, (xtrain.shape[0], xtrain.shape[1], 1))

    # Building and initialising the RNN
    LSTMregressor = Sequential()

    # Add 1st LSTM layer and some Dropout regularisation
    LSTMregressor.add(CuDNNLSTM(units = 50, return_sequences = True, input_shape = (xtrain.shape[1], 1)))
    LSTMregressor.add(Dropout(0.2))

    # Adding 3nd LSTM layer with dropout regularisation
    LSTMregressor.add(CuDNNLSTM(units = 50, return_sequences = True))
    LSTMregressor.add(Dropout(0.2))

    # Adding 3rd LSTM layer and some Dropout regularisation
    LSTMregressor.add(CuDNNLSTM(units = 50, return_sequences = True))
    LSTMregressor.add(Dropout(0.2))

    # Adding 4th LSTM layer with dropout regularisation
    LSTMregressor.add(CuDNNLSTM(units = 50))
    LSTMregressor.add(Dropout(0.2))

    # Add the output layer
    LSTMregressor.add(Dense(units = 1))

    # Compile the RNN using adam optimizer
    LSTMregressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

    # Fitting the RNN to the Training set
    LSTMregressor.fit(xtrain, ytrain, epochs = 100, batch_size = 32)

    # Making the predictions and exporting to csv file 
    real_stock_price = dataset_test.iloc[:, 4:5].values
    # Getting the predicted stock price
    dataset_total = pd.concat((dataset_train['close'], dataset_test['close']), axis = 0)
    inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(60, 76): #size 16
        X_test.append(inputs[i-60:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price = LSTMregressor.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)    
    #pandas export
    i=0
    np.savetxt('csvFilesPrediction/'+stock[x]+'.csv',predicted_stock_price, delimiter=',',  header='pp', comments='')

