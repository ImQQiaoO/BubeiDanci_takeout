import requests
import time
import random

all_words = {}


def get_cookie_and_last_word():
    cookie = input("请输入您的不背单词的cookie，然后按回车键继续...\n")
    last_word = input("请输入您上次导出的最后一个单词，然后按回车键继续，第一次使用请输入任意数字...\n")
    return cookie, last_word


def get_headers(cookie):
    return {'cookie': cookie}


def fetch_data(page, headers):
    response = requests.get(f'https://www.bbdc.cn/api/user-new-word?page={page}', headers=headers)
    return response.json()


def load_words(list_):
    for words_info in list_:
        if '\n' in words_info["interpret"]:
            words_info["interpret"] = words_info["interpret"].replace('\n', ' ')
        all_words[words_info["word"]] = words_info["interpret"]


def process_all_pages(total_pages, headers):
    for i in range(total_pages):
        print(f"\r进度：{'#' * (i + 1)} {(i + 1) / total_pages * 100:.2f}%", end="")
        data = fetch_data(i, headers)
        load_words(data["data_body"]["wordList"])
        time.sleep(3)


def shuffle_words():
    global all_words
    all_words = dict(random.sample(list(all_words.items()), len(all_words)))


def sort_words():
    global all_words
    all_words = dict(sorted(all_words.items(), key=lambda x: x[0]))


def save_words_to_file(last_word):
    index = 0
    for word, interpret in all_words.items():
        if word == last_word:
            break
        index += 1
        print(word, interpret)
        with open('words0.csv', 'a', encoding='utf-8') as f:
            f.write(f"{index}. ,{word},{interpret}\n")


def main():
    print("欢迎使用不背单词导出工具！")

    # 获取cookie和上次导出的最后一个单词
    cookie, last_word = get_cookie_and_last_word()
    headers = get_headers(cookie)

    # 获取第一页数据，计算总页数
    data = fetch_data(0, headers)
    load_words(data["data_body"]["wordList"])
    total_pages = int(data["data_body"]["pageInfo"]['totalPage'])

    # 处理所有页面数据
    process_all_pages(total_pages, headers)

    # 是否打乱顺序
    if input("\n是否打乱顺序？(y/n): ").lower() == 'y':
        shuffle_words()

    # 是否按照字典顺序排序
    if input("是否按照字典顺序排序？(y/n): ").lower() == 'y':
        sort_words()

    # 保存单词到文件
    save_words_to_file(last_word)


if __name__ == "__main__":
    main()
