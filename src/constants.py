from enum import Enum


class OrderOption(Enum):
    DEFAULT_ORDER = '0'
    SHUFFLE_ORDER = '1'
    ALPHABETICAL_ORDER = '2'
    NO_EXPORT = '3'


order_options_dict = {
    OrderOption.DEFAULT_ORDER: "默认顺序",
    OrderOption.SHUFFLE_ORDER: "打乱顺序",
    OrderOption.ALPHABETICAL_ORDER: "字典顺序",
    OrderOption.NO_EXPORT: "不导出至文件",
}


class FormatOption(Enum):
    CSV = '0'
    PDF = '1'


class PDFDirection(Enum):
    LONGITUDINAL = '0'
    HORIZONTAL = '1'
    COMPACT = '2'
    DICTATION_EN = '3'
    DICTATION_CH = '4'


pdf_direction_dict = {
    PDFDirection.LONGITUDINAL: "纵向",
    PDFDirection.HORIZONTAL: "横向",
    PDFDirection.COMPACT: "紧凑",
    PDFDirection.DICTATION_EN: "默写单词",
    PDFDirection.DICTATION_CH: "默写释义",
}
