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
words=[]
classes=[]
documents=[]
ignore_words=['?','!','.',',','a','v','xét']
data_file=open('data.json',encoding='utf-8').read()
#Load file json 
intents=json.loads(data_file)
#Thu thập từ vựng và các lớp (thẻ)
total=0
for intent in intents['intents']:
    for pattern in intent['patterns']:
        pattern=define.no_accent_vietnamese(pattern).strip()
        w=nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
words=[w for w in words if w not in ignore_words]
words=sorted(list(set(words)))
classes=sorted(list(set(classes)))

pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))
#Chuẩn bị dữ liệu huấn luyện
training=[]
output_empty=[0]*len(classes)
for doc in documents:
    bag=[]

    pattern_words=doc[0]
    pattern_words=[word.lower() for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row=list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag,output_row])
    
training=np.array(training,dtype=object)
train_x=list(training[:,0])
train_y=list(training[:,1])
#Hàm tạo model
def create_model():
    model = Sequential()
    model.add(Dense(128, input_dim=len(train_x[0]), activation='tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))
    sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model

train_x=np.array(train_x)
train_y=np.array(train_y)
#Hàm chia tập dữ liệu train test
from sklearn.model_selection import train_test_split
train_data, test_data, train_labels, test_labels = train_test_split(train_x, train_y, test_size=0.2, random_state=42)
model = create_model()
history = model.fit(np.array(train_data), np.array(train_labels), epochs=90, batch_size=8, verbose=1)
model.save('chatbot_model.h5')
score = model.evaluate(np.array(test_data), np.array(test_labels), verbose=1)
# print('Test loss:', score[0])
# print('Test accuracy:', score[1])