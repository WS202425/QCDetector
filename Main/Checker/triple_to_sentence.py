import re
from Hull.pipeline.Utils.generate import generate_response

triplet_to_sentence_PROMKPT = \
    """给定一个主题背景和一个原子事实四元组（主，谓，宾，附加信息）请你将他还原为原子事实。
    以下是一些上下文示例：

    ### 主题:
    欧洲冠军联赛（UEFA Champions League）的冠军球队所属国家

    ### triplets:
    （AC米兰，赢得，欧洲冠军联赛冠军，曾多次，所属国家是意大利）
    
    ### 原子事实:
    AC米兰，一支来自意大利的足球俱乐部，曾多次赢得欧洲冠军联赛冠军。

    现在根据提供的主题背景，生成三元组和附加条件生成原子事实

    ### 主题:
    {title}
    
    ### triplet:
    {triplet}

    ### 原子事实:

    """


def triplet_to_sentence(title, triplet):
    prompt = triplet_to_sentence_PROMKPT.format(title=title, triplet=triplet)
    gpt4_response = generate_response(prompt)
    return gpt4_response


# print(extract_triplet("（AC米兰，赢得，欧洲冠军联赛冠军，意大利的俱乐部）",
#                       "意大利的俱乐部，如AC米兰和尤文图斯等，也曾多次赢得欧洲冠军联赛冠军。"))

