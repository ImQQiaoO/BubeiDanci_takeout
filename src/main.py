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
import sys
import subprocess


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
        all_words[words_info["word"]] = None
    for i in range(1, total_pages):
        time.sleep(random.uniform(2, 5))
        print("进度：",
              f'|{"#" * ((i + 1) * 50 // total_pages):50}|',
              f'{(i + 1) * 100 // total_pages}%', end='\r')
        page_data = fetch_page_data(base_url.format(page=i), headers)
        if not page_data:
            break
        for words_info in page_data["data_body"]["wordList"]:
            all_words[words_info["word"]] = None
    print()
    return all_words


def save_as_csv(all_words, order_choice) -> str:
    if os.name == 'nt':
        encoding = 'mbcs'
    else:
        encoding = 'utf-8'
    current_date = datetime.now().strftime('%Y_%m_%d')
    file_name = f"words-{current_date}-{order_options_dict[OrderOption(order_choice)]}.csv"
    with open(file_name, 'w', encoding=encoding, errors='replace', newline='') as f:
        if len(all_words) == 0:
            return None
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        index = 0
        for word, interpret in all_words.items():
            index += 1
            writer.writerow([index, word, interpret])
    return file_name


def select_output_word_order(all_words, reverse_flag) -> tuple:
    print("请输出导出至文件时的单词顺序（输入数字即可，仅支持单选）：")
    for key, value in order_options_dict.items():
        print(f"   [{key.value}]. {value}")
    while True:
        order_choice = input("您的选择是：")
        if order_choice in (OrderOption.DEFAULT_ORDER.value, OrderOption.NO_EXPORT.value):
            if reverse_flag:
                all_words = dict(reversed(list(all_words.items())))
                reverse_flag = False
            break
        if order_choice == OrderOption.REVERSE_ORDER.value:
            if not reverse_flag:
                all_words = dict(reversed(list(all_words.items())))
                reverse_flag = True
            break
        if order_choice == OrderOption.SHUFFLE_ORDER.value:
            all_words = dict(random.sample(list(all_words.items()), len(all_words)))
            break
        if order_choice == OrderOption.ALPHABETICAL_ORDER.value:
            all_words = dict(sorted(all_words.items(), key=lambda x: x[0]))
            break
        print("输入错误，请重试。")
        for key, value in order_options_dict.items():
            print(f"   [{key.value}]. {value}")
    return all_words, order_choice, reverse_flag


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


def load_dictionary() -> dict:
    dict_path = os.path.join(os.getcwd(), 'dependencies/ultimate.csv')
    if not os.path.exists(dict_path):
        raise FileNotFoundError("未找到字典文件！可能是由于未将字典文件 `ultimate.csv` 放在 `dependencies` 目录下。")
    dictionary = {}
    with open(dict_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            dictionary[row[0]] = row[3]
    return dictionary


def consult_dictionary(all_words) -> None:
    print("正在查询字典...")
    dictionary = load_dictionary()
    for word in all_words:
        if word in dictionary:
            all_words[word] = dictionary[word].replace('\\n', ' ')
        else:
            all_words[word] = "-"
    print("查询完毕！")
    
    
def reveal_in_file_manager(file_path):
    abs_path = os.path.abspath(file_path)
    if sys.platform == 'win32':  # Windows
        subprocess.Popen(f'explorer /select,"{abs_path}"')
    elif sys.platform == 'darwin':  # macOS
        subprocess.Popen(['open', '-R', abs_path])  # 在 Finder 中揭示文件
    elif sys.platform.startswith('linux'):  # Linux
        dirname = os.path.dirname(abs_path)
        managers = [
            ['nautilus', '--select', abs_path],      # GNOME
            ['dolphin', '--select', abs_path],       # KDE
            ['thunar', abs_path],                    # XFCE
            ['pcmanfm', abs_path],                   # LXDE
            ['xdg-open', dirname]                    # 通用回退
        ]
        for manager in managers:
            try:
                subprocess.Popen(manager)
                break
            except FileNotFoundError:
                continue
        else:
            raise NotImplementedError("Unsupported platform")


def main() -> None:
    print("欢迎使用不背单词导出工具！")
    while True:
        cookie = input("请输入您的不背单词的cookie，然后按回车键继续...\n")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36",
            "cookie": cookie,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        try:
            all_words = fetch_all_words(headers)
            print(f"单词获取成功，共 {len(all_words)} 个单词。")
            consult_dictionary(all_words)
            break
        except requests.exceptions.RequestException as e:
            print(f"本次请求出错，请重新尝试获取：{e}")
        except FileNotFoundError as e:
            print(f"字典文件错误：{e}")
            input("程序将在您按下回车键后退出...")
            return
        except Exception as e:
            print(f"本次获取单词失败，请检查Cookie是否正确：{e}")

    reverse_flag = False
    while True:
        all_words, order_choice, reverse_flag = select_output_word_order(all_words, reverse_flag)
        for word, interpret in all_words.items():
            print(word, interpret)

        output_file = None
        if order_choice != OrderOption.NO_EXPORT.value:
            select_choice = select_format()
            if select_choice == FormatOption.CSV.value:
                output_file = save_as_csv(all_words, order_choice)
            elif select_choice == FormatOption.PDF.value:
                output_file = save_as_pdf(all_words, order_choice)
            
            if output_file is not None:
                print("此次保存成功！是否需要打开文件所在目录？（y/n）", end="")
                if input().lower() == "y":
                    reveal_in_file_manager(".\\" + output_file)
                else:
                    print("已取消打开文件所在目录。")
            else:
                print("保存失败：没有单词可以导出或文件生成失败。")
        if input("输入[q]退出程序，输入其他任意内容按回车键继续保存：").lower() == "q":
            break


if __name__ == "__main__":
    main()
