from fpdf import FPDF
from datetime import datetime
from constants import order_options_dict
from constants import OrderOption
import os
import sys


class PDF(FPDF):
    def footer(self):
        self.set_font('MSYH', '', 12)
        self.set_y(-15)
        self.cell(0, 10, f"{self.page_no()}", 0, 0, "C")


def truncate_text(pdf, text, max_width):
    text_width = pdf.get_string_width(text)
    margin = 2
    if text_width <= max_width - margin:
        return text
    else:
        ellipsis = "..."
        ellipsis_width = pdf.get_string_width(ellipsis)
        available_width = max_width - margin - ellipsis_width

        truncated = ""
        for char in text:
            if pdf.get_string_width(truncated + char) <= available_width:
                truncated += char
            else:
                break
        return truncated + ellipsis


def save_as_pdf(all_words, order_choice):
    pdf = PDF()
    pdf.add_page()
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = "./"
    font_path = os.path.join(base_path, 'fonts/MSYH.TTC')
    pdf.add_font('MSYH', '', font_path)
    pdf.set_font('MSYH', '', 12)
    col_widths = [20, 50, 120]
    line_height = pdf.font_size * 2.5
    table_width = sum(col_widths)

    start_x = (pdf.w - table_width) / 2
    start_y = pdf.get_y()

    pdf.set_xy(start_x, start_y)
    pdf.set_fill_color(240, 240, 240)

    for idx, (word, interpret) in enumerate(all_words.items()):
        pdf.set_x(start_x)
        fill = idx % 2 == 0
        pdf.cell(col_widths[0], line_height, str(idx + 1), border=1, align="C", fill=fill)
        pdf.cell(col_widths[1], line_height, word, border=1, align="C", fill=fill)
        truncated_interpret = truncate_text(pdf, interpret, col_widths[2])
        pdf.cell(col_widths[2], line_height, truncated_interpret, border=1, align="C", fill=fill)
        pdf.ln(line_height)

    current_date = datetime.now().strftime('%Y_%m_%d')
    file_name = f"words-{current_date}-{order_options_dict[OrderOption(order_choice)]}.pdf"
    pdf.output(file_name)
