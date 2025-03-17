from fpdf import FPDF
from datetime import datetime
from constants import order_options_dict
from constants import pdf_direction_dict
from constants import OrderOption
from constants import PDFDirection
import os


class PDF(FPDF):
    def footer(self):
        self.set_font('MSYH', '', 12)
        self.set_y(-15)
        self.cell(0, 10, f"{self.page_no()}", 0, 0, "C")


def select_pdf_direction():
    print("请输出导出PDF时的页面方向（输入数字即可，仅支持单选）：")
    print("选择横向时，会展示较为完整的单词释义")
    for key, value in pdf_direction_dict.items():
        print(f"   [{key.value}]. {value}")
    while True:
        direction_choice = input("您的选择是：")
        if direction_choice in (PDFDirection.LONGITUDINAL.value, PDFDirection.HORIZONTAL.value):
            break
        else:
            print("输入错误，请重试。")
            for key, value in pdf_direction_dict.items():
                print(f"   [{key.value}]. {value}")
    return direction_choice


def warp_text(pdf, text, max_width) -> tuple:
    lines_takeup = 1
    text_width = pdf.get_string_width(text)
    margin = 2
    if text_width <= max_width - margin:
        return lines_takeup, text
    warped_text = ""
    each_line = ""
    for char in text:
        if pdf.get_string_width(each_line + char) < max_width - margin:
            each_line += char
        else:
            each_line += '\n'
            warped_text += each_line
            lines_takeup +=1
            each_line = char
    warped_text += each_line
    return lines_takeup, warped_text


def save_as_pdf(all_words, order_choice):
    direction = select_pdf_direction()
    if direction == PDFDirection.HORIZONTAL.value:
        col_widths = [20, 50, 200]
        pdf = PDF(orientation='L')
    else:
        col_widths = [20, 50, 120]
        pdf = PDF()
    pdf.add_page()
    font_path = os.path.join(os.getcwd(), 'dependencies/MSYH.TTC')
    pdf.add_font('MSYH', '', font_path)
    pdf.set_font('MSYH', '', 12)
    line_height = pdf.font_size * 2.5
    table_width = sum(col_widths)

    start_x = (pdf.w - table_width) / 2
    start_y = pdf.get_y()

    pdf.set_xy(start_x, start_y)
    pdf.set_fill_color(240, 240, 240)

    for idx, (word, interpret) in enumerate(all_words.items()):
        pdf.set_x(start_x)
        fill = idx % 2 == 0
        lines_takeup, warped_interpret = warp_text(pdf, interpret, col_widths[2])
        pdf.cell(col_widths[0], line_height * lines_takeup, str(idx + 1), border=1, align="C", fill=fill)
        pdf.cell(col_widths[1], line_height * lines_takeup, word, border=1, align="C", fill=fill)
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(col_widths[2], line_height, warped_interpret, border=1, align="L", fill=fill)
        pdf.set_xy(x + col_widths[2], y)
        pdf.ln(line_height * lines_takeup)

    current_date = datetime.now().strftime('%Y_%m_%d')
    file_name = f"words-{current_date}-{order_options_dict[OrderOption(order_choice)]}-{pdf_direction_dict[PDFDirection(direction)]}.pdf"
    pdf.output(file_name)
