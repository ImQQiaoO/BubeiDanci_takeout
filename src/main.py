import requests
import time
import random
import os
import csv
from constants import order_options_dict
from constants import OrderOption
from constants import FormatOption
from datetime import datetime
from pdf_formatter import save_as_pdf


def fetch_page_data(url, headers, retries=3):
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            time.sleep(random.uniform(2, 5))
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
        print("进度：",
              f'|{"#" * ((i + 1) * 50 // total_pages):50}|',
              f'{(i + 1) * 100 // total_pages}%', end='\r')
        page_data = fetch_page_data(base_url.format(page=i), headers)
        if not page_data:
            break
        for words_info in page_data["data_body"]["wordList"]:
            interpret = words_info["interpret"].replace('\n', ' ')
            all_words[words_info["word"]] = interpret
    print()
    return all_words


def save_as_csv(all_words, order_choice) -> None:
    if os.name == 'nt':
        encoding = 'mbcs'
    else:
        encoding = 'utf-8'
    current_date = datetime.now().strftime('%Y_%m_%d')
    file_name = f"words-{current_date}-{order_options_dict[OrderOption(order_choice)]}.csv"
    with open(file_name, 'a', encoding=encoding, newline='') as f:
        if len(all_words) == 0:
            return
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        index = 0
        for word, interpret in all_words.items():
            index += 1
            writer.writerow([index, word, interpret])


def select_output_word_order(all_words) -> tuple:
    print("请输出导出至文件时的单词顺序（输入数字即可，仅支持单选）：")
    for key, value in order_options_dict.items():
        print(f"   [{key.value}]. {value}")
    while True:
        order_choice = input("您的选择是：")
        if order_choice in (OrderOption.DEFAULT_ORDER.value, OrderOption.NO_EXPORT.value):
            break
        elif order_choice == OrderOption.SHUFFLE_ORDER.value:
            all_words = dict(random.sample(list(all_words.items()), len(all_words)))
            break
        elif order_choice == OrderOption.ALPHABETICAL_ORDER.value:
            all_words = dict(sorted(all_words.items(), key=lambda x: x[0]))
            break
        else:
            print("输入错误，请重试。")
            for key, value in order_options_dict.items():
                print(f"   [{key.value}]. {value}")
    return all_words, order_choice


def select_format():
    print("请输出导出至文件时的文件形式（输入数字即可，仅支持单选）：")
    for option in FormatOption:
        print(f"   [{option.value}]. {option.name}")
    while True:
        format_choice = input("您的选择是：")
        if format_choice in (FormatOption.CSV.value, FormatOption.PDF.value):
            break
        else:
            print("输入错误，请重试。")
            for option in FormatOption:
                print(f"   [{option.value}]. {option.name}")
    return format_choice


def main() -> None:
    print("欢迎使用不背单词导出工具！")
    cookie = input("请输入您的不背单词的cookie，然后按回车键继续...\n")
    headers = {'cookie': cookie}
    all_words = fetch_all_words(headers)
    while True:
        all_words, order_choice = select_output_word_order(all_words)
        for word, interpret in all_words.items():
            print(word, interpret)

        if order_choice != OrderOption.NO_EXPORT.value:
            select_choice = select_format()
            if select_choice == FormatOption.CSV.value:
                save_as_csv(all_words, order_choice)
            elif select_choice == FormatOption.PDF.value:
                save_as_pdf(all_words, order_choice)
            print("此次保存成功！", end="")
        if input("输入[q]退出程序，输入其他任意内容按回车键继续保存：").lower() == "q":
            break


if __name__ == "__main__":
    main()
