'''
user = "test001"
NickName = "nickname_Update"
user2 = "test002"
NickName2 = "安喜延"
NickNameFile = 'C:/Users/USER/Desktop/TwitchBot/NickNameList.txt'
import random
def readNickNameFile():
    NickList = []
    ReadNickFile = ""
    try:
        ReadNickFile = open(NickNameFile, 'r')
        # do stuff with ReadNickFile
        for line in ReadNickFile.readlines():
            if line == "":
                break
            line = line[:len(line)].split(", ")
            NickList.append(line)
    finally:
        if ReadNickFile is not None:
            ReadNickFile.close()
        return NickList

def setNickName(NickList, user, NickName):
    for line in NickList:
        if user == line[0]:
            line[1] = NickName + "\n"
        return NickList

def getNickName(NickList, user):
    for line in NickList:
        if user == line[0]:
            return line[1]
    return user

def saveNickList(NickList):
    WriteNickFile = ""
    words = ""
    try:
        for i in range(len(NickList)):
            words = words + ", ".join(NickList[i])
        WriteNickFile = open(NickNameFile, 'w')
        # do stuff with WriteNickFile
        WriteNickFile.write(words)

    finally:
        if WriteNickFile is not None:
            WriteNickFile.close()

def following_word(words, name):
    a = words.join(name)
    print(a)

def special_serve(self, user_name):
    number = hash(user_name) % 100
    if number < 10 :
        pass
    D = {0: '', 1: '', 2: '',}
    return D[number]


following_word(" fail ", "apple")
NickList = readNickNameFile()
print(type(NickList))
NickList = setNickName(NickList, user, NickName)
NickList = setNickName(NickList, user2, NickName2)
print(NickList)
saveNickList(NickList)

random.randint(0,99)


import requests, re
def keep_viewer():
    res = requests.get('http://tmi.twitch.tv/group/user/dante0713/chatters')
    words = re.sub('\r|\n|\t|', '', res.text)
    viewers = words.split('"viewers": [')[1].split(']')[0]
    mods = words.split('"moderators": [')[1].split(']')[0]
    viewers = re.sub(",      "+r'"'+"streamelements"+r'"'+"","",viewers + ",      " + mods) # 去除 streamelements, kimikobot
    viewers = re.sub(",      "+r'"'+"kimikobot"+r'"'+"","",viewers)
    viewer_list = re.sub(r'"', "", re.sub(" ", "", viewers)).split(',')
    return viewer_list

print(keep_viewer())
'''

def save_sentence_data(user, sentences, sentence_data_list, countdown):
    if countdown % 2 == 0:
        t_k_flag = True
        learn_autonomic(t_k_flag) # [throw: T, flag: F]
    else:
        learn_catch_chat()
    pass

def learn_autonomic(user, sentences, throw_keep_flag):
    if throw_keep_flag:
        throw()
    else:
        keep()
    pass

def learn_catch_chat(user, sentences, user_flag):
    keep_flag = False
    if user_flag == "@"+user:
        catch()
        keep_flag=True
    else:
        pass
    if keep_flag:
        keep()
    else:
        pass
    pass

def throw():
    pass

def catch():
    pass

def keep():
    pass
