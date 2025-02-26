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


GREEN_OUTPUT = '\033[32m'
COLOUR_END = '\033[0m'