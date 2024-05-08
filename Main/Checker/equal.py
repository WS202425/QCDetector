import re


# def equal(string1, string2):
#     # 清理两个字符串中的特殊字符（全角和半角括号）
#     pattern = r'[^\w\s]'
#     content1 = re.sub(pattern, '', string1)
#     content2 = re.sub(pattern, '', string2)
#     # 比较清理后的字符串
#     return content1 == content2


t = """(姚明，出生在，上海)
(姚明，身高，2.29米)
(姚明，身高，7英尺6英寸)
(姚明，是，中国篮球领袖、商人和政治人物的传奇生涯和公益事业)"""
s = "['(姚明，出生在，上海)\n(姚明，身高，2.29米)\n(姚明，身高，7英尺6英寸)\n(姚明，是，中国篮球领袖、商人和政治人物的传奇生涯和公益事业)']"


def equal(string1, string2):
    # 确保输入是字符串
    str1 = str(string1)
    str2 = str(string2)

    pattern = r'[^\w\s]'
    # 使用正则表达式对字符串进行处理
    content1 = re.sub(pattern, '', str1)
    content2 = re.sub(pattern, '', str2)

    return content1 == content2


# print(equal(t,s))