@Date 2017/7/2

# 新知 (待閱)
- 召回率 = 包含率 = all - (Fp + FN)  / all 
- tf-idf (找關鍵字)
- hashtrick (解決記憶體分配)
- word2vector( 字詞之間相似程度)
- 找聊天室裡的user http://tmi.twitch.tv/group/user/dante0713/chatters

# model 學習方式

### 保留結構，但不推薦拿來訓練deep learning 

  結巴(句型結構 - 分詞) - 對方句子意義 <=> 對應的句子意義 - 挑詞 - 句型結構
  
### 適合拿來deep learning做聊天機器人學習

  1. 自行指定觀眾丟句子，收集指定觀眾回復句子
  2. 找相對應的觀眾回復
  
