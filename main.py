import time
import random
import requests

print("欢迎使用不背单词导出工具！")
cookie = input("请输入您的不背单词的cookie，然后按回车键继续...\n")
last_word = input("请输入您上次导出的最后一个单词，然后按回车键继续，第一次使用请输入任意数字...")

headers = {
    'cookie': cookie,
}

all_words = {}


def load_words(list_):
    for words_info in list_:
        # 解析json， 获取到'wordList'，即单词列表
        if '\n' in words_info["interpret"]:
            words_info["interpret"] = words_info["interpret"].replace('\n', ' ')
        all_words[words_info["word"]] = words_info["interpret"]


response = requests.get('https://www.bbdc.cn/api/user-new-word?page=0', headers=headers)
data = response.json()

load_words(data["data_body"]["wordList"])

total_pages = int(data["data_body"]["pageInfo"]['totalPage'])  # 解析json，获取到'pageInfo'，即总页数
for i in range(total_pages):
    # 添加进度条
    print(f"\r进度：{'#' * (i + 1)} {(i + 1) / total_pages * 100:.2f}%", end="")
    response = requests.get('https://www.bbdc.cn/api/user-new-word?page=' + str(i), headers=headers)
    data = response.json()
    load_words(data["data_body"]["wordList"])
    time.sleep(3)
shuffle = input("\n是否打乱顺序？(y/n): ")
if shuffle == 'y':
    all_words = dict(random.sample(list(all_words.items()), len(all_words)))

# 将字典写入文件
index = 0
for word, interpret in all_words.items():
    if word == last_word:
        break
    index += 1
    print(word, interpret)
    with open('words0.csv', 'a', encoding='utf-8') as f:
        f.write(str(index) + '. ,' + word + ',' + interpret + '\n')
