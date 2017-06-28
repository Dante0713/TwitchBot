# The only import you need!
import socket,re


class TwitchBot:
    def __init__(self):
        # Options (Don't edit)
        self.SERVER = "irc.twitch.tv"  # server
        self.PORT = 6667  # port
        # Options (Edit this)
        self.PASS = "oauth:pcd4qyfqd5t6we1sykcwzm657rc1vy"  # bot password can be found on https://twitchapps.com/tmi/
        self.BOT = "dante0713"  # Bot's name [NO CAPITALS]
        self.CHANNEL = "dante0713"  # Channal name [NO CAPITALS]
        self.OWNER = "dante0713"  # Owner's name [NO CAPITALS]
        self.QUIT = True
        self.SOCKET = socket.socket()
        self.readbuffer = ""
        self.NickNameFile = 'C:/Users/USER/Desktop/TwitchBot/NickNameList.txt'
        self.NickList = []

    # Functions
    def read_nick_name_file(self):
        nick_list = []
        read_nick_file = ""
        try:
            read_nick_file = open(self.NickNameFile, 'r')
            # do stuff with ReadNickFile
            for line in read_nick_file.readlines():
                if line == "":
                    break
                line.replace("\n","")
                line = line[:len(line)].split(", ")
                nick_list.append(line)
        finally:
            if read_nick_file is not None:
                read_nick_file.close()
            return nick_list

    def send_message(self, s, line):
        message_temp = "PRIVMSG #" + self.CHANNEL + " :" + line
        s.send((message_temp + "\r\n").encode('utf8'))

    def get_user(self, line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    def get_message(self, line):
        global message
        try:
            message = (line.split(":", 2))[2]
        except:
            message = ""
        return message

    def join_chat(self):
        readbuffer_join = "".encode('utf8')
        Loading = True
        self.NickList = self.read_nick_name_file()
        while Loading:
            readbuffer_join = self.SOCKET.recv(1024)
            readbuffer_join = readbuffer_join.decode('utf8')
            temp = readbuffer_join.split("\n")
            readbuffer_join = readbuffer_join.encode('utf8')
            readbuffer_join = temp.pop()
            for line in temp:
                Loading = self.loading_completed(line)
        self.send_message(self.SOCKET, "各位好啊~ 現在已經開台囉~ 歡迎來到丹堤實況台~ 希望今天的主題你們會喜歡! ")
        print("Bot has joined " + self.CHANNEL + " Channel!")

    def loading_completed(self, line):
        if ("End of /NAMES list" in line):
            return False
        else:
            return True

    def set_nick_name_from_lines(self,  user, message):
        Sentence = message.split(' ')
        if len(Sentence) == 2:
            Sentence = Sentence[1]
            if len(Sentence) <= 10:
                self.set_nick_name(user= user, NickName= re.sub('\r|\n|\t','',Sentence))
                print(self.NickList)
                return 1
            else:
                return 2
        else:
            return 3

    def set_nick_name(self, user, NickName):
        flag = True
        for line in self.NickList:
            if user == line[0]:
                line[1] = NickName
                flag = False
        if flag:
            self.NickList.append([user, NickName])

    def get_nick_name(self,  user):
        for line in self.NickList:
            if user == line[0]:
                return line[1]
        return user

    def Console(self, line):
        # gets if it is a user or twitch server
        if "PRIVMSG" in line:
            return False
        else:
            return True

    def store_nick_list(self):
        WriteNickFile = open(self.NickNameFile, 'w')
        words = ""
        try:
            for i in range(len(self.NickList)):
                print(type(self.NickList[i][0]))
                words = words + self.NickList[i][0] + ", " + re.sub('\n','',self.NickList[i][1]) + "\n"
            # do stuff with WriteNickFile
            WriteNickFile.write(words)
        finally:
            if WriteNickFile is not None:
                WriteNickFile.close()

# Code runs
    def setting(self):
        s_prep = socket.socket()
        s_prep.connect((self.SERVER, self.PORT))
        s_prep.send(("PASS " + self.PASS + "\r\n").encode('utf8'))
        s_prep.send(("NICK " + self.BOT + "\r\n").encode('utf8'))
        s_prep.send(("JOIN #" + self.CHANNEL + "\r\n").encode('utf8'))
        self.SOCKET = s_prep
        self.join_chat()
        self.readbuffer = ""

    def run(self):
        line = ""
        thisNickName = ""
        thisUser = ""
        while self.QUIT:
            try:
                self.readbuffer = self.SOCKET.recv(1024)
                self.readbuffer = self.readbuffer.decode('utf8')
                temp = self.readbuffer.split("\n")
                self.readbuffer = self.readbuffer.encode('utf8')
                self.readbuffer = temp.pop()
            except:
                temp = ""
            for line in temp:
                if line == "":
                    break
                # So twitch doesn't timeout the bot.
                if "PING" in line and self.Console(line):
                    self.SOCKET.send("PONG tmi.twitch.tv\r\n".encode('utf8'))
                    break
                # get user
                user = self.get_user(line)
                # get user's nick name
                nick_name = self.get_nick_name(user)
                # get message send by user
                message = self.get_message(line)
                # for you to see the chat from CMD
                print(user + " > " + message)

                # commands
                if user == self.OWNER:
                    if "!command" in message:
                        self.send_message(self.SOCKET, "親愛的 " + nick_name + " ~ 所有指令在 https://goo.gl/etv8rT 中可以查詢"
                                                                       "唷~")
                        break
                    elif "大家晚安" in message:
                        self.send_message(self.SOCKET, "謝謝今天的各位的參與，喜歡我的朋友可以加入我的臉書粉專 https://www."
                                                       "facebook.com/dante0713 ,台裡的最新資訊都在臉書粉專裡，祝各位有個美"
                                                       "麗的夜晚，大家晚安囉~ 88")
                        self.store_nick_list()
                        self.QUIT = False
                        break
                if "老楊" in message:
                    if "安安" in message or "ㄤㄤ" in message:
                        self.send_message(self.SOCKET, "滾! ")
                        break
                if "月月" in message or "丹丹" in message or "提哥" in message or "堤哥" in message or "月子" in message or "月提" in message \
                        or "月堤" in message or "丹提" in message or "丹堤" in message or "台主" in message:
                    if "安安" in message or "ㄤㄤ" in message or "你好" in message or "KonCha" in message or "Hi" in message:
                        self.send_message(self.SOCKET, "你好啊~" + nick_name + " ! 歡迎來到丹堤實況台~ 希望你會喜歡今天的實況內容~ ")
                        break
                    if "早" in message:
                        self.send_message(self.SOCKET, "早啊~" + nick_name + " ! 早起精神好! ")
                        break
                    if '好久不見' in message:
                        self.send_message(self.SOCKET, "真的是好久不見了~ " + nick_name + ", 我給您留了個位置, 趕快拉張椅子坐下來看台吧 <3")
                        break
                if "歐吼" in message:
                    if user == "n75830" or user == "ss87414" or user == "winnie0810":
                        self.send_message(self.SOCKET, "歐~~~ 齁~~~~~" + nick_name + "早安呀")
                if "!認人 " in message:
                    case = self.set_nick_name_from_lines(message=message, user=user)
                    if case == 1:
                        self.send_message(self.SOCKET, "輸入成功 (測試中)")
                    elif case == 2:
                        self.send_message(self.SOCKET, '親愛的' + nick_name + '，您設定的暱稱酷炫屌炸天，而且超過十個字，導致我的腦容量爆表拉!!!  NotLikeThis')
                    elif case == 3:
                        self.send_message(self.SOCKET, '小淘氣，不要鬧在下了~ 您的暱稱不可包含空格 提示: (!認人 <您的暱稱>)')
                if "InuyoFace" in message:
                    self.send_message(self.SOCKET, "你想幹嘛?")
                if "KappaPride" in message:
                    if "阿" in message and "月" in message and "仔" in message:
                        split_nick_name = ""
                        if user == "ninomiyalena":
                            split_nick_name = "LENA"
                        elif user == "tiaolowan":
                            split_nick_name = "樓王"
                        self.send_message(self.SOCKET, " FailFish ".join(split_nick_name))

############################################################################
if __name__ == '__main__':
    Dante0713 = TwitchBot()
    Dante0713.__init__()
    Dante0713.setting()
    Dante0713.run()
