import requests
import time
import random


def fetch_page_data(url, headers, retries=3):
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            time.sleep(3)
        return None


def fetch_all_words(headers) -> dict:
    all_words = {}
    base_url = 'https://www.bbdc.cn/api/user-new-word?page={page}'
    first_page_data = fetch_page_data(base_url.format(page=0), headers)
    if not first_page_data:
        return all_words
    data = first_page_data
    total_pages = int(data["data_body"]["pageInfo"]['totalPage'])
    for words_info in data["data_body"]["wordList"]:
        interpret = words_info["interpret"].replace('\n', ' ')
        all_words[words_info["word"]] = interpret
    for i in range(1, total_pages):
        print(f"\r进度：{'#' * (i + 1)} {(i + 1) / total_pages * 100:.2f}%", end="")
        page_data = fetch_page_data(base_url.format(page=i), headers)
        if not page_data:
            break
        for words_info in page_data["data_body"]["wordList"]:
            interpret = words_info["interpret"].replace('\n', ' ')
            all_words[words_info["word"]] = interpret
    print()
    return all_words


def save_words(all_words) -> None:
    index = 0
    for word, interpret in all_words.items():
        index += 1
        print(word, interpret)
        with open('words0.csv', 'a', encoding='mbcs') as f:
            f.write(f"{index}. ,{word},{interpret}\n")


def select_output_word_order(all_words):
    print("请输出导出至文件时的单词顺序（输入数字即可，仅支持单选）：")
    print("   [0]. 默认顺序")
    print("   [1]. 打乱顺序")
    print("   [2]. 字典顺序")
    while True:
        choice = input("您的选择是：")
        if choice == str(0):
            break
        elif choice == str(1):
            all_words = dict(random.sample(list(all_words.items()), len(all_words)))
            break
        elif choice == str(2):
            all_words = dict(sorted(all_words.items(), key=lambda x: x[0]))
            break
    return all_words


def main() -> None:
    print("欢迎使用不背单词导出工具！")
    cookie = input("请输入您的不背单词的cookie，然后按回车键继续...\n")
    headers = {'cookie': cookie}
    all_words = fetch_all_words(headers)
    all_words = select_output_word_order(all_words)
    save_words(all_words)


if __name__ == "__main__":
    main()
