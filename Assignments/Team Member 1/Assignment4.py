#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras_preprocessing import sequence
from keras.utils import to_categorical
from keras.models import load_model


# In[4]:


df = pd.read_csv('C:\\Users\\Rajap\\Downloads\\spam.csv',delimiter=',',encoding='latin-1')
df.head()


# In[5]:


df.drop(['Unnamed: 2','Unnamed: 3', 'Unnamed: 4'],axis=1,inplace=True) #dropping unwanted columns
df.info()


# In[6]:


#Count of Spam and Ham values
df.groupby(['v1']).size()


# In[7]:


#Label Encoding target column
X = df.v2
Y = df.v1
le = LabelEncoder()
Y = le.fit_transform(Y)
Y = Y.reshape(-1,1)


# In[8]:


# Test and train spilit 
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.15)


# In[9]:


# Tokenisation function
max_words = 1000
max_len = 150
tok = Tokenizer(num_words=max_words)
tok.fit_on_texts(X_train)
sequences = tok.texts_to_sequences(X_train)
sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)


# In[10]:


#creating LSTM model
inputs = Input(name='InputLayer',shape=[max_len])
layer = Embedding(max_words,50,input_length=max_len)(inputs)
layer = LSTM(64)(layer)
layer = Dense(256,name='FullyConnectedLayer1')(layer)
layer = Activation('relu')(layer)
layer = Dropout(0.5)(layer)
layer = Dense(1,name='OutputLayer')(layer)
layer = Activation('sigmoid')(layer)


# In[11]:


model = Model(inputs=inputs,outputs=layer)
model.summary()
model.compile(loss='binary_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])


# In[12]:


model.fit(sequences_matrix,Y_train,batch_size=128,epochs=10,
          validation_split=0.2)


# In[13]:


model.save("model_1")


# In[14]:


#test the model
test_sequences = tok.texts_to_sequences(X_test)
test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=max_len)


# In[15]:


accuracy = model.evaluate(test_sequences_matrix,Y_test)
print('Accuracy: {:0.3f}'.format(accuracy[1]))


# In[16]:


y_pred = model.predict(test_sequences_matrix)
print(y_pred[25:40].round(3))


# In[17]:


print(Y_test[25:40])

