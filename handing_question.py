import re
import define
from underthesea import sent_tokenize
key={"cong nghe thong tin" : 0,"ky thuat du lieu" : 1,"an toan thong tin":2}
def Punctuation(string):

    punctuations = '''!()-[]{};:'"\<>./?@#$%^&*_~,'''
    for x in string.lower():
        if x in punctuations:
            string = string.replace(x, "")

    # Print string without punctuation
    return string
def handing(s):
    dict={}
    s=define.no_accent_vietnamese(s)
    result=[]
    s=sent_tokenize(s)
    for k in s:
        k=Punctuation(k)
        if len(k)==0:
            continue
        k=list(k.split())
        for i in range(len(k)):
            if k[i] == ('va' or '?'):
                k[i]=','
        result=" ".join(k)
        result=result.split(',')
        # print(result)
        out_hello(result)
        result=handing_1(result)
        for j in result:
            dict[j]=-1
            for h in key:
                if h in j:
                    dict[j]=key[h]
    return dict
def handing_1(msg):
    a=[]
    for i in msg:
        s=i.strip()
        number=1
        for k in key:
            if number == 1:
                if k in s :
                    temp=s.replace(k,"")
                    a.append(temp.strip())
                    a.append(k)
                    number = 0
            else:
                break
        if number == 1:
            a.append(s)
    # print(a)
    for arr in a:
        if arr=="":
            a.remove(arr)
    results=[]
    for i in range(len(a)):
        if a[i] in key:
            for j in range(i,-1,-1):
                if a[j] not in key:
                    results.append(a[j]+" "+a[i])
                    break
        else:
            if i != len(a)-1:
                if a[i+1] not in key:
                    # print("o'")
                    results.append(a[i])
            else :
                results.append(a[i])
    if len(results)==0:
        return msg
    return results
def out_hello(res):
    hello=["chao thay","chao co","cho em hoi","cho hoi","da","thua thay","thua co",""]
    for k in hello:
        if k in res:
            res.remove(k)

# msg="ngành hệ thống thông tin"
# msg=define.no_accent_vietnamese(msg)
# print(msg)
# k=handing(msg)
# print(k)
# for i in k:
#     print(i)
