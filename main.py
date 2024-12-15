import requests
import time
import random


def get_cookie_and_last_word():
    cookie = input("请输入您的不背单词的cookie，然后按回车键继续...\n")
    last_word = input("请输入您上次导出的最后一个单词，然后按回车键继续，第一次使用请输入任意数字...\n")
    return cookie, last_word


def fetch_all_words(headers):
    all_words = {}
    response = requests.get(
        'https://www.bbdc.cn/api/user-new-word?page=0', headers=headers)
    data = response.json()
    for words_info in data["data_body"]["wordList"]:
        if '\n' in words_info["interpret"]:
            words_info["interpret"] = words_info["interpret"].replace(
                '\n', ' ')
        all_words[words_info["word"]] = words_info["interpret"]
    total_pages = int(data["data_body"]["pageInfo"]['totalPage'])

    for i in range(total_pages):
        print(f"\r进度：{'#' * (i + 1)} {(i + 1) / total_pages * 100:.2f}%", end="")
        response = requests.get(
            f'https://www.bbdc.cn/api/user-new-word?page={i}', headers=headers)
        data = response.json()
        for words_info in data["data_body"]["wordList"]:
            if '\n' in words_info["interpret"]:
                words_info["interpret"] = words_info["interpret"].replace(
                    '\n', ' ')
            all_words[words_info["word"]] = words_info["interpret"]
        time.sleep(3)
    return all_words


def save_words(all_words, last_word):
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
    cookie, last_word = get_cookie_and_last_word()
    headers = {'cookie': cookie}
    all_words = fetch_all_words(headers)

    if input("\n是否打乱顺序？(y/n): ").lower() == 'y':
        all_words = dict(random.sample(
            list(all_words.items()), len(all_words)))

    if input("是否按照字典顺序排序？(y/n): ").lower() == 'y':
        all_words = dict(sorted(all_words.items(), key=lambda x: x[0]))

    save_words(all_words, last_word)


if __name__ == "__main__":
    main()
