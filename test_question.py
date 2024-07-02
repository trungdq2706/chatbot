import define
import json
import define

data_file=open('data.json',encoding='utf-8').read()
intents=json.loads(data_file)
#Hàm này thu thập tất cả các thẻ (tags) từ bộ dữ liệu intents
def tag_data():
    tag=[]
    for intent in intents['intents']:
        tag.append(intent['tag'])
    return tag

def test(question):
    question=define.no_accent_vietnamese(question)
    tag=tag_data()
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if define.no_accent_vietnamese(pattern) == question:
                return 1,[]
    return 0,tag
#Hàm thêm câu hỏi cho nhãn cũ
def add_question_intotag(question,tag):
    for intent in intents['intents']:
        if intent["tag"]==tag:
            intent["patterns"].append(question)
    with open("data.json","w",encoding='utf-8') as file:
        json.dump(intents,file,ensure_ascii=False,indent=3)
    return "Đã thêm câu hỏi " + question + " vào nhãn " + tag

#Hàm thêm câu hỏi cho nhãn mới
def add_new_tag(question,tag,ans):
    dict={"tag": tag,
       "patterns" : [question],
       "responses" : [ans]
    }
    for intent in intents['intents']:
        if intent["tag"]==tag:
            return "Nhãn đã tồn tại trong cơ sở dữ liệu"
    intents['intents'].append(dict)
    with open("data.json","w",encoding='utf-8') as file:
        json.dump(intents,file,ensure_ascii=False,indent=3)
    return "Đã thêm thành công"

