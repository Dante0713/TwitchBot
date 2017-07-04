# The only import you need!
import socket, requests, re, random, time


class TwitchBot:
    def __init__(self):
        # Options (Don't edit)
        self.SERVER = "irc.twitch.tv"  # server
        self.PORT = 6667  # port
        # Options (Edit this)
        self.PASS = "oauth:Your oauth passwords"  # bot password can be found on https://twitchapps.com/tmi/
        self.BOT = "dante0713"  # Bot's name [NO CAPITALS]
        self.CHANNEL = "dante0713"  # Channal name [NO CAPITALS]
        self.OWNER = "dante0713"  # Owner's name [NO CAPITALS]
        self.QUIT = True
        self.SOCKET = socket.socket()
        self.read_buffer = ""
        self.NickNameFile = 'F:/TwitchBot-master/NickNameList.txt'
        self.NickList = []
        self.AudienceList = {}

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
                line = line.strip('\n')
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
        self.AudienceList = self.keep_viewer()
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

    def set_nick_name_from_lines(self, user, message):
        Sentence = message.split(' ')
        if len(Sentence) == 2:
            Sentence = Sentence[1]
            if len(Sentence) <= 10:
                self.set_nick_name(user=user, NickName=re.sub('\r|\n|\t', '', Sentence))
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

    def get_nick_name(self, user):
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
                words = words + self.NickList[i][0] + ", " + re.sub('\n', '', self.NickList[i][1]) + "\n"
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
        self.read_buffer = ""

    def set_lake_stuff_from_lines(self, message, user):
        Sentence = message.split(' ')
        if len(Sentence) == 2:
            Sentence = Sentence[1]
            if len(Sentence) <= 10:
                return Sentence
            else:
                return 1
        else:
            return 2
        pass

    def get_stuff(self):
        number = random.randint(0,999)
        if number <= 15:
            return 0
        elif number <= 35:
            return 1
        elif number <= 470:
            return 2
        else:
            return 3
    # 爬聊天室觀眾 準備計算 point 未完成
    def keep_viewer(self):
        audience_list = {}
        res = requests.get('http://tmi.twitch.tv/group/user/dante0713/chatters')
        words = re.sub('\r|\n|\t|', '', res.text)
        viewers = words.split('"viewers": [')[1].split(']')[0]
        mods = words.split('"moderators": [')[1].split(']')[0]
        viewers = re.sub(",      " + r'"' + "streamelements" + r'"' + "", "",
                         viewers + ",      " + mods)  # 去除 streamelements, kimikobot
        viewers = re.sub(",      " + r'"' + "kimikobot" + r'"' + "", "", viewers)
        viewer_list = re.sub(r'"', "", re.sub(" ", "", viewers)).split(',')
        for viewer in viewer_list:
            audience_list[viewer] = 0
        return audience_list

    def compare_set(self):
        flag = False
        audience_list = self.keep_viewer()
        for key in audience_list:
            if key in self.AudienceList:
                self.AudienceList[key] = self.AudienceList[key] + 1
            else:
                self.AudienceList[key] = 0

    def count_loyalty(self, time_keep_flag, first_time):
        # 問題: 不知道不講話的觀眾會不會被算進去
        if time_keep_flag == False:
            next_time = time.time()
            time_count = next_time - first_time
            if time_count >= 60:
                self.compare_set()
            else:
                return False

    def show_audience_list(self):
        words = ""
        print(self.AudienceList)
        for key in self.AudienceList:
            words = words + key + ": " + str(self.AudienceList[key])+ ", "
        return words

    def run(self):
        line = ""
        thisNickName = ""
        thisUser = ""
        first_time = 0
        time_keep_flag = True
        lady_was_die_in_user_hands = ""
        lady_of_lake_flag = True
        while self.QUIT:
            try:
                if time_keep_flag == True:
                    first_time = time.time()
                time_keep_flag = self.count_loyalty(time_keep_flag, first_time)
                self.read_buffer = self.SOCKET.recv(1024)
                self.read_buffer = self.read_buffer.decode('utf8')
                temp = self.read_buffer.split("\n")
                self.read_buffer = self.read_buffer.encode('utf8')
                self.read_buffer = temp.pop()
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
                    if "!丹堤bot指令集" in message:
                        self.send_message(self.SOCKET, "親愛的 " + nick_name + " ~ 所有指令在 https://goo.gl/etv8rT 中可以查詢")
                        break
                    elif "大家晚安" in message or "quit" in message:
                        #self.send_message(self.SOCKET, "謝謝今天的各位的參與，喜歡我的朋友可以加入我的臉書粉專 https://www."
                        #                               "facebook.com/dante0713 ,台裡的最新資訊都在臉書粉專裡，祝各位有個美"
                        #                               "麗的夜晚，大家晚安囉~ 88")
                        self.send_message(self.SOCKET, "丹堤bot 下線中...")
                        self.send_message(self.SOCKET, "丹堤bot 已離線")
                        self.send_message(self.SOCKET, "Points: " + self.show_audience_list())
                        self.store_nick_list()
                        self.QUIT = False
                        break
                    elif "!myGit" in message:
                        self.send_message(self.SOCKET, "Here's my Twitch Bot link. https://github.com/Dante0713/TwitchBot/blob/master/README.md")
                        break
                    elif "!我的Git" in message:
                        self.send_message(self.SOCKET, "這是我寫的聊天室機器人，歡迎觀看及使用 https://github.com/Dante0713/TwitchBot/blob/master/README_CH.md")
                        break
                    elif "滋滋卡滋滋，湖中女神~ 神力復甦!!" in message:
                        lady_of_lake_flag = True
                        lady_was_die_in_user_hands = ""
                        self.send_message(self.SOCKET, "在台主施以神奇的魔法後，湖中女神意外的復活了!!!")
                        break
                if "!湖中女神 " in message or "!drop " in message:
                    if lady_of_lake_flag == True:
                        stuff = self.set_lake_stuff_from_lines(message, user)
                        if stuff == 1:
                            self.send_message(self.SOCKET, "很抱歉，由於您的物品名稱太長，導致掉下去湖中的過程，刺死了湖中女神，請您訂閱台主、斗內台主或使用小奇點以喚回湖中女神") # 中文版 防呆
                            lady_was_die_in_user_hands = user
                            lady_of_lake_flag = False
                            break
                        elif stuff == 2:
                            self.send_message(self.SOCKET, "很抱歉，由於您丟入湖裡的物品長得太奇怪，湖中女神認不出來，請您再丟一次，不知道怎麼丟可以問台主 :) ")
                            break
                        else:
                            value = self.get_stuff()
                            if value == 0:
                                self.send_message(self.SOCKET, "恭喜你, 成功用愛情擄獲了湖中女神的心, 湖中女神決定不只給你 金" + stuff + " 作為回報，也獻上了他的肉體 <3 (恭喜您獲得 500 丹丹幣，請聊天室的朋友提醒台主給錢)")
                                break
                            elif value == 1:
                                self.send_message(self.SOCKET, "恭喜你, 成功用十塊錢擄獲了湖中女神的心, 湖中女神決定用 銀" + stuff + " 回報你的斗內 <3 (恭喜您獲得 300 丹丹幣，請聊天室的朋友提醒台主給錢)")
                                break
                            elif value == 2:
                                self.send_message(self.SOCKET, "很抱歉,湖中女神聽不到你說甚麼,於是你的" +stuff + "就這樣默默的沉入湖底...")
                                break
                            elif value == 3:
                                self.send_message(self.SOCKET, "湖中女神覺得你很誠實,所以決定把"+ stuff +"物歸原主")
                                break
                    else:
                        self.send_message(self.SOCKET,
                                          "湖中女神已經被" + lady_was_die_in_user_hands + "殺死，只有訂閱、斗內或小奇點，才有辦法讓台主使湖中女神死亡復甦! ")  # 中文版 防呆
                        break
                if "!認人 " in message or "!set_nick_name " in message:
                    case = self.set_nick_name_from_lines(message=message, user=user)
                    if case == 1:
                        self.send_message(self.SOCKET, "恭喜你輸入成功")
                        break
                    elif case == 2:
                        self.send_message(self.SOCKET, '親愛的' + nick_name + '，您設定的暱稱酷炫屌炸天，而且超過十個字，導致我的腦容量爆表拉!!!  NotLikeThis')
                        break
                    elif case == 3:
                        self.send_message(self.SOCKET, '小淘氣，不要鬧在下了~ 您的暱稱不可包含空格 提示: (!認人 <您的暱稱>)')
                        break
                if "月月" in message or "丹丹" in message or "提哥" in message or "堤哥" in message or "月子" in message or "月提" in message or "月堤" in message or "丹提" in message or "丹堤" in message or "台主" in message:
                    if "安安" in message or "ㄤㄤ" in message or "你好" in message or "KonCha" in message or "Hi" in message or "hi" in message:
                        self.send_message(self.SOCKET, "你好啊~" + nick_name + " ! 歡迎來到丹堤實況台~ 希望你會喜歡今天的實況內容~ ")
                        break
                    if "早" in message:
                        self.send_message(self.SOCKET, "早啊~" + nick_name + " ! 早起精神好! ")
                        break
                    if '好久不見' in message:
                        self.send_message(self.SOCKET, "真的是好久不見了~ " + nick_name + ", 我給您留了個位置, 趕快拉張椅子坐下來看台吧 <3")
                        break
                    if '姊姊' in message or '姐姐' in message or '解解' in message:
                        if len(message) < 6:
                            self.send_message(self.SOCKET, nick_name + "妹妹早阿~ 小朋友們今天有沒有都乖乖的呀? ")
                            break
                if 'Hi' in message or 'hi' in message:
                    if 'FlipThis' in message or 'TheThing' in message or 'VoHiYo' in message or 'DoritosChip' in message or 'copyThis' in message or 'MorphinTime' in message or 'BigPhish' in message or 'NotLikeThis' in message:
                        break
                    elif 'Dante' in message or 'dante' in message:
                        self.send_message(self.SOCKET, "Hello, " + nick_name + "!")
                        break
                    else:
                        self.send_message(self.SOCKET, "Hi there! Nice to meet you")
                        break
                if "歐吼" in message:
                    if user == "n75830" or user == "ss87414" or user == "winnie0810":
                        self.send_message(self.SOCKET, "歐~~~ 齁~~~~~" + nick_name + "早安呀")
                        break
                if "丹寶貝" in message or '丹寶寶' in message:
                    if user == 'morgn__':
                        self.send_message(self.SOCKET, "摩根寶貝你來啦~  TwitchUnity  TwitchUnity")
                        break
                if "InuyoFace" in message:
                    self.send_message(self.SOCKET, "你想幹嘛? ScaredyCat ")
                    break
                if "KappaPride" in message:
                    if "阿" in message and "月" in message and "仔" in message:
                        split_nick_name = ""
                        if user == "ninomiyalena":
                            split_nick_name = "LENA"
                        elif user == "tiaolowan":
                            split_nick_name = "樓王"
                        else:
                            split_nick_name = nick_name
                        self.send_message(self.SOCKET, " FailFish ".join(split_nick_name))
                        break
                else:
                    break
############################################################################
if __name__ == '__main__':
    Dante0713 = TwitchBot()
    Dante0713.__init__()
    Dante0713.setting()
    Dante0713.run()
