import re


def equal(string1, string2):
    # 确保输入是字符串
    str1 = str(string1)
    str2 = str(string2)

    pattern = r'[^\w\s]'
    # 使用正则表达式对字符串进行处理
    content1 = re.sub(pattern, '', str1)
    content2 = re.sub(pattern, '', str2)

    return content1 == content2
