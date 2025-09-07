import openpyxl
from datetime import datetime
from constants import order_options_dict
from constants import OrderOption
from openpyxl.styles import Alignment, Font


def save_as_xlsx(all_words, order_choice) -> str:
    current_date = datetime.now().strftime("%Y_%m_%d")
    file_name = f"words-{current_date}-{order_options_dict[OrderOption(order_choice)]}.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # 设置标题和表头
    sheet.title = "Words"
    sheet.append(["Index", "Word", "Interpretation"])
    for cell in sheet[1]:  # 第一行是表头
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center")
    for index, (word, interpret) in enumerate(all_words.items(), start=1):
        sheet.append([index, word, interpret])

    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            val = "" if cell.value is None else str(cell.value)
            length = max((len(line) for line in val.splitlines()), default=0)
            if length > max_length:
                max_length = length
        sheet.column_dimensions[column].width = min(max_length + 2, 80)

    workbook.save(file_name)
    return file_name
