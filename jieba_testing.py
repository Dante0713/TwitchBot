#encoding=utf-8
import jieba

sentence = "我的比哩巴喜喜歡吃麥當勞"
print("Input：", sentence)
words = jieba.cut(sentence, cut_all=True)



seg_list = jieba.cut(sentence, cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.cut_for_search(sentence)  # 搜索引擎模式
print(", ".join(seg_list))
# cut_all=False 全模式關閉

import jieba.posseg as pseg
sssss = pseg.cut(sentence)
for w in sssss:
    print('%s %s' % (w.word, w.flag))