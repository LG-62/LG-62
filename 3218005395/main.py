import re
import gensim
import jieba


# 用正则表达式清理数据，过滤完只剩下中文
def clear(l):
    r = re.compile(u"[^\u4e00-\u9fa5]")
    l = r.sub('', l)
    return l


# 原文的读取，过滤
#orig_path = 'D:/学习资料/软工/pythonProject/test/orig.txt'
orig_path = input("输入论文原文的文件的绝对路径:\t")
test_path = input("输入抄袭版论文的文件的绝对路径:\t")

# 异常处理
if not os.path.exists(orig_path):
    print("论文源文件不存在！")
    exit()
if not os.path.exists(test_path):
    print("抄袭论文文件不存在！")
    exit()
    
# print('%s' % orig_path)
orig_file = open(orig_path, 'r', encoding='utf-8')  # 打开文本
text1 = orig_file.read()
orig_file.close()  # 关闭文本
text1 = clear(text1)  # 对文本进行清理

# 查重文本的读取和清理
# test_path = 'D:/学习资料/软工/pythonProject/test/orig_0.8_add.txt'
test_file = open(test_path, 'r', encoding='utf-8')
text2 = test_file.read()
test_file.close()
text2 = clear(text2)

# 结果保存文件的路径
# result_path = 'D:/学习资料/软工/pythonProject/test/result.txt'
result_path = input("输入输出的答案文件的绝对路径:\t")

# 分别对原文和查重文本的jieba分词
text11 = jieba.lcut(text1)
text22 = jieba.lcut(text2)

# 检验jieba分词后的结果
# print(text11)
# print(text22)

# 把jieba分词后的值通过similarity求相似度
texts = [text11, text22]
# 将文本的词语进行建立词典
dictionary = gensim.corpora.Dictionary(texts)
# 处理词典
corpus = [dictionary.doc2bow(text) for text in texts]
features_num = len(dictionary)
similarity = gensim.similarities.Similarity('-similarity-index', corpus, num_features=features_num)
# 将查重文本转化为稀疏向量
test_corpus_1 = dictionary.doc2bow(text11)
# 得到相似结果
cosine_sim = similarity[test_corpus_1][1]
# 答案保留小数点后两位
print("文本相似度：%.2f" % cosine_sim)

# 将相似度结果写入指定文件
f = open(result_path, 'w', encoding='utf-8')
f.write("文章相似度：%.2f" % cosine_sim)
f.close()
