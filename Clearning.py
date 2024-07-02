import nltk
import define
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Activation,Dropout
from keras.optimizers import SGD
import random
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping
import keras
from keras.models import load_model
words=[]
classes=[]
documents=[]
ignore_words=['?','!','.',',','a','v','xét']
data_file=open('data.json',encoding='utf-8').read()
intents=json.loads(data_file)
# print(intents)
total=0
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # total=total+1
        pattern=define.no_accent_vietnamese(pattern).strip()
        w=nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
words=[w for w in words if w not in ignore_words]
words=sorted(list(set(words)))
classes=sorted(list(set(classes)))
print(len(words))
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))
# # # #training
training=[]
output_empty=[0]*len(classes)
# print(output_empty)
for doc in documents:
    bag=[]

    pattern_words=doc[0]
    pattern_words=[word.lower() for word in pattern_words]
    # print(pattern_words)
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row=list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag,output_row])
#
training=np.array(training)
train_x=list(training[:,0])
train_y=list(training[:,1])

# print(np.array(train_y))
print(np.array(train_x).shape)
print(np.array(train_y).shape)



activation=['relu','sigmoid','tanh']

def create_model():
    model = Sequential()
    sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    return model,sgd

def get_activation_model(activation,train_x,train_y,X_test,Y_test):
    for k in activation:
        model,sgd=create_model()
        print(k)
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation=k))
        model.add(Dropout(0.5))
        model.add(Dense(128, activation=k))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        model.fit(np.array(train_x), np.array(train_y),epochs=80, batch_size=4, verbose=1)
        score=model.evaluate(np.array(X_test),np.array(Y_test))
        print("accuracy_SGD ",k,"",score[1])

print(len(words))
train_x=np.array(train_x)
train_y=np.array(train_y)
def model_test(train_x,train_y):
    model,sgd=create_model()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='tanh'))
    model.add(Dropout(0.6))
    model.add(Dense(128, activation='tanh'))
    model.add(Dropout(0.6))
    model.add(Dense(len(train_y[0]), activation='softmax'))
    # early_stopping_monitor = EarlyStopping(patience=2)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    hist=model.fit(np.array(train_x), np.array(train_y),epochs=100, batch_size=6, verbose=1)
    model.save('chatbot_model.h5', hist)
    return model
#
model = model_test(train_x,train_y)
# score=model.evaluate(np.array(X_test),np.array(Y_test))
# # print("accuracy_SGD --",i,score[1])
# model.save('chatbot_model.h5', hist)
#
from sklearn.model_selection import train_test_split

# score=model.evaluate(np.array(X_test),np.array(Y_test))
# model.save('chatbot_model.h5',hist)
score_test=[]
for i in range(0,5):
    X_train, X_test, y_train, y_test = train_test_split( train_x, train_y, test_size=1/3.0, random_state=100+i)
    # keras.backend.clear_session()
    model = model_test(X_train,y_train)
    score=model.evaluate(np.array(X_test),np.array(y_test))
    score_test.append(score[1])
    print("accuracy_SGD --",i,score[1])
#
print(score_test)














# print(classes)
# from sklearn.model_selection import ShuffleSplit
# ss = ShuffleSplit(n_splits=1, test_size=0.5,random_state=10)
# #đánh giá mô hình_ với tối ưu hóa SGD
# for train_index,test_index in ss.split(train_x):
#     keras.backend.clear_session()
# #     print("Train: ",train_index,"Test",test_index)
#     X_test,X_train=train_x[test_index],train_x[train_index]
#     Y_test,Y_train=train_y[test_index],train_y[train_index]
# #     # get_activation_model(activation,X_train,Y_train,X_test,Y_test)
# #     # plt.plot(hist.history['accuracy'])
# #     # plt.plot(hist.history['val_accuracy'])
# #     # plt.title('Model accuracy')
# #     # plt.ylabel('Accuracy')
# #     # plt.xlabel('Epoch')
# #     # plt.legend(['Train', 'Test'])
# #     # plt.show()
#     model,sgd=create_model()
#     model.add(Dense(128, input_shape=(len(train_x[0]),), activation='tanh'))
#     model.add(Dropout(0.5))
#     model.add(Dense(64, activation='tanh'))
#     model.add(Dropout(0.5))
#     model.add(Dense(len(train_y[0]), activation='softmax'))
#     # early_stopping_monitor = EarlyStopping(monitor='loss',patience=5,verbose=1)
#     model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#     hist=model.fit(np.array(X_train), np.array(Y_train),epochs=100, batch_size=4, verbose=1)
# # #     # plt.figure()
# # #
# # #
# ss1 = ShuffleSplit(n_splits=3, test_size=0.4,random_state=13)
# for train_index,test_index in ss1.split(train_x):
#     print("Train: ",train_index,"Test",test_index)
#     X_test,X_train=train_x[test_index],train_x[train_index]
#     Y_test,Y_train=train_y[test_index],train_y[train_index]
#     score=model.evaluate(np.array(X_test),np.array(Y_test),verbose=0)
#     # plt.figure()
#     print("accuracy_SGD: ",score[1])

#
# #lay tanh là tốt nhất
