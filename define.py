import re
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
word_nomean=['ạ','đi','em','thầy','ơi','e',"cô","vậy","và","tôi"]
#Hàm xóa các từ trong word_nomen
def delete_word(s):
    s = s.lower()
    s= s.split()
    for i in range(len(s)):
        if s[i] in word_nomean:
            s[i]=""
    return " ".join(s)

#Hàm để thay thế các từ gõ sai và có dấu thành chữ không dấu
def no_accent_vietnamese(s):
    s = delete_word(s)
    s = alias(s)
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[đ]', 'd', s)
    return s
#hàm thay thế các từ viết tắt thành từ có nghĩa
def alias(s):
    s = s.replace('cntt','cong nghe thong tin')
    s = s.replace('bn','bao nhieu')
    s = s.replace('ko','khong')
    s = s.replace('ntn','nhu the nao')
    s = s.replace('ktx','ky tuc xa')
    s = s.replace('nhiu','nhieu')
    s = s.replace('hc','hoc')
    s = s.replace('dc','duoc')
    s = s.replace('nghanh','nganh')
    s = s.replace('khmt','khoa hoc may tinh')
    s = s.replace('httt','he thong thong tin')
    s = s.replace('ktpm','ki thuat phan mem')
    s = s.replace('clc','chat luong cao')
    s = s.replace('nckh','nghien cuu khoa hoc')
    s = s.replace('sv','sinh vien')
    s = s.replace('ktdl','ky thuat du lieu')
    s = s.replace('attt','an toan thong tin')
    return s
#Hàm chuẩn hóa một câu văn bản đầu vào
def clean_up_sentence(sentence):
    sentence_words=no_accent_vietnamese(sentence)
    sentence_words = nltk.word_tokenize(sentence_words)
    sentence_words = [word.lower() for word in sentence_words]
    return sentence_words
