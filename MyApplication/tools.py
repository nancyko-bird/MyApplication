import re
import shutil
from datetime import datetime
import os
from decimal import Decimal, InvalidOperation


def check_string(s):
    # 字符串可以包含字母、数字和下划线，但是不能以数字开头，也不能是纯数字
    # 此外，也不能包含某些特殊字符，如“-”和“@”
    if not s:  # 检查空字符串
        return False
    if s[0].isdigit():  # 检查是否以数字开头
        return False
    if s.isdigit():  # 检查是否是纯数字
        return False
    if '-' in s or '@' in s:  # 检查是否包含特殊字符“-”和“@”
        return False
        # if not re.match(r'^[a-zA-Z0-9_]+$', s):  # 检查是否只包含字母、数字和下划线
    #     return False
    return True


def backup_data(src, dst):
    # src: 源文件路径
    # dst: 目标文件路径
    shutil.copy(src, dst)  # 使用shutil的copy方法复制文件


# 使用函数
# copy_file('source.txt', 'destination.txt')

def get_now_time():
    # 获取当前时间
    now = datetime.now()
    # 格式化为字符串，精确到秒
    now_time = now.strftime('%Y-%m-%d-%H:%M:%S')
    return now_time


def get_now_time1():
    # 获取当前时间
    now = datetime.now()
    # 格式化为字符串，精确到秒
    now_time = now.strftime('%Y%m%d%H%M%S')
    return now_time


def split_path_and_filename(filepath):
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    return directory, filename


def print_line(s):
    print("\n============= " + str(s) + " ==================")


def parse_tags(tag_string):
    """
    接受一个以分号分隔的标签字符串，并返回一个包含这些标签的列表。

    :param tag_string: 以分号分隔的标签字符串
    :return: 包含标签的列表
    """
    # 使用split()方法根据分号分割字符串，得到一个列表
    tags = re.split(r'[;；]', tag_string)

    # 去除列表中的空字符串元素（如果有的话）
    tags = [tag.strip() for tag in tags if tag.strip()]

    return tags


def format_decimal_string(num_str):
    # 分割整数部分和小数部分
    parts = num_str.split('.')
    integer_part = parts[0]

    # 检查小数部分
    if len(parts) > 1:
        fractional_part = parts[1]

        # 判断小数位数是否超过两位
        if len(fractional_part) > 2:
            raise ValueError("Decimal part must not exceed two digits.")
        elif len(fractional_part) < 2:
            # 如果小数部分少于两位，则补零
            fractional_part += '0' * (2 - len(fractional_part))
    else:
        # 如果没有小数部分，则补上.00
        fractional_part = '00'

        # 合并整数部分和小数部分
    formatted_num_str = f"{integer_part}.{fractional_part}"

    try:
        # 将字符串转换为Decimal类型
        decimal_value = Decimal(formatted_num_str)
    except InvalidOperation:
        raise ValueError("Invalid input. Cannot convert to Decimal.")

    return decimal_value
    # # 示例用法
    # try:
    #     print(format_decimal_string("123"))  # 输出: 123.00
    #     print(format_decimal_string("123.4"))  # 输出: 123.40
    #     print(format_decimal_string("123.456"))  # 报错：小数点后超过两位
    #     print(format_decimal_string("-123.4"))  # 输出: -123.40
    #     print(format_decimal_string("0.4"))  # 输出: 0.40
    #     print(format_decimal_string("123.0000"))  # 输出: 123.00（注意：按照您的要求，我们仅检查并限制小数点后两位）
    # except ValueError as e:
    #     print(f"Error: {e}")
