from fpdf import FPDF
from datetime import datetime
from constants import order_options_dict
from constants import pdf_direction_dict
from constants import dictation_dict
from constants import OrderOption
from constants import PDFDirection
from constants import DictationOption
import os


class PDF(FPDF):
    def footer(self):
        self.set_font('MSYH', '', 12)
        self.set_y(-15)
        self.cell(0, 10, f"{self.page_no()}", 0, 0, "C")


def select_pdf_direction():
    print("请输出导出PDF时的页面方向（输入数字即可，仅支持单选）：")
    for key, value in pdf_direction_dict.items():
        print(f"   [{key.value}]. {value}")
    while True:
        direction_choice = input("您的选择是：")
        if direction_choice in (PDFDirection.LONGITUDINAL.value, PDFDirection.HORIZONTAL.value,
                                PDFDirection.COMPACT.value):
            break
        print("输入错误，请重试。")
        for key, value in pdf_direction_dict.items():
            print(f"   [{key.value}]. {value}")
    return direction_choice


def select_dictation_mode():
    print("请输出导出PDF时是否开启默写模式（输入数字即可，仅支持单选）：")
    for key, value in dictation_dict.items():
        print(f"   [{key.value}]. {value}")
    while True:
        direction_choice = input("您的选择是：")
        if direction_choice in (DictationOption.DICTATION_OFF.value, DictationOption.DICTATION_EN.value,
                                DictationOption.DICTATION_CH.value):
            break
        print("输入错误，请重试。")
        for key, value in dictation_dict.items():
            print(f"   [{key.value}]. {value}")
    return direction_choice


def wrap_text(pdf, text, max_width) -> tuple:
    lines_takeup = 1
    text_width = pdf.get_string_width(text)
    margin = 2
    if text_width <= max_width - margin:
        return lines_takeup, text
    wrapped_text = ""
    each_line = ""
    for char in text:
        if pdf.get_string_width(each_line + char) < max_width - margin:
            each_line += char
        else:
            wrapped_text += each_line + '\n'
            lines_takeup += 1
            each_line = char
    wrapped_text += each_line
    return lines_takeup, wrapped_text


def pdf_compact_mode(pdf, all_words, order_choice, direction):
    pdf.add_page()
    font_path = os.path.join(os.getcwd(), 'dependencies/MSYH.TTC')
    pdf.add_font('MSYH', '', font_path)
    pdf.set_font('MSYH', '', 7)

    left_margin = 10
    top_margin = 10
    right_margin = 10
    page_width = pdf.w - left_margin - right_margin
    gap = 5
    col_width = (page_width - gap) / 2
    line_height = 4
    current_column = 0 
    x_positions = [left_margin, left_margin + col_width + gap]
    y_position = top_margin
    pdf.set_auto_page_break(False)
    max_y = pdf.h - 20

    def split_text_to_lines(text, width):
        lines = []
        current_line = ""
        for char in text:
            test_line = current_line + char
            if pdf.get_string_width(test_line) <= width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char
        if current_line:
            lines.append(current_line)
        return lines
    
    for word, interpret in all_words.items():
        text = f"{word} - {interpret}"
        indent_offset = pdf.get_string_width(f"{word} - ")
        first_line_width = col_width
        wrapped_line_width = col_width - indent_offset
        first_line = ""
        remaining_text = text
        for char in text:
            test_line = first_line + char
            if pdf.get_string_width(test_line) <= first_line_width:
                first_line += char
                remaining_text = remaining_text[1:]
            else:
                break
        
        wrapped_lines = split_text_to_lines(remaining_text, wrapped_line_width)
        total_height = line_height
        if wrapped_lines:
            total_height += len(wrapped_lines) * line_height
        if y_position + total_height > max_y:
            if current_column == 0:
                current_column = 1
                y_position = top_margin
            else:
                pdf.add_page()
                current_column = 0
                y_position = top_margin
        pdf.set_xy(x_positions[current_column], y_position)
        pdf.cell(col_width, line_height, first_line, ln=1)
        y_position += line_height
        for line in wrapped_lines:
            pdf.set_xy(x_positions[current_column] + indent_offset, y_position)
            pdf.cell(wrapped_line_width, line_height, line, ln=1)
            y_position += line_height
    current_date = datetime.now().strftime('%Y_%m_%d')
    file_name = f"words-{current_date}-{order_options_dict[OrderOption(order_choice)]}-{pdf_direction_dict[PDFDirection(direction)]}.pdf"
    pdf.output(file_name)



def save_as_pdf(all_words, order_choice):
    direction = select_pdf_direction()
    dictation_mode = DictationOption.DICTATION_OFF.value
    if direction != PDFDirection.COMPACT.value:
        dictation_mode = select_dictation_mode()
    if direction == PDFDirection.HORIZONTAL.value:
        col_widths = [20, 50, 200]
        pdf = PDF(orientation='L')
    elif direction == PDFDirection.LONGITUDINAL.value:
        col_widths = [20, 50, 120]
        pdf = PDF()
    elif direction == PDFDirection.COMPACT.value:
        pdf = PDF()
        pdf_compact_mode(pdf, all_words, order_choice, direction)
        return
    else:
        return
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
        lines_takeup, wrapped_interpret = wrap_text(pdf, interpret, col_widths[2])
        pdf.cell(col_widths[0], line_height * lines_takeup, str(idx + 1), border=1, align="C", fill=fill)
        if dictation_mode == DictationOption.DICTATION_EN.value:
            pdf.cell(col_widths[1], line_height * lines_takeup, "", border=1, align="C", fill=fill)
        else:
            pdf.cell(col_widths[1], line_height * lines_takeup, word, border=1, align="C", fill=fill)
        x = pdf.get_x()
        y = pdf.get_y()
        if dictation_mode == DictationOption.DICTATION_CH.value:
            pdf.cell(col_widths[2], line_height * lines_takeup, "", border=1, align="L", fill=fill)
        else:
            pdf.multi_cell(col_widths[2], line_height, wrapped_interpret, border=1, align="L", fill=fill)
        pdf.set_xy(x + col_widths[2], y)
        pdf.ln(line_height * lines_takeup)

    current_date = datetime.now().strftime('%Y_%m_%d')
    file_name = f"words-{current_date}-{order_options_dict[OrderOption(order_choice)]}-{pdf_direction_dict[PDFDirection(direction)]}-{dictation_dict[DictationOption(dictation_mode)]}.pdf"
    pdf.output(file_name)
