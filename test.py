user = "test001"
NickName = "nickname_Update"
user2 = "test002"
NickName2 = "安喜延"
NickNameFile = 'C:/Users/USER/Desktop/TwitchBot/NickNameList.txt'

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

following_word(" fail ", "apple")
NickList = readNickNameFile()
print(type(NickList))
NickList = setNickName(NickList, user, NickName)
NickList = setNickName(NickList, user2, NickName2)
print(NickList)
saveNickList(NickList)