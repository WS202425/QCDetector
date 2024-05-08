import ast
import re

from Hull.pipeline.Utils.generate import generate_response, generate_responses
from Hull.pipeline.Utils.parse_evdience import parse_claim_triplets

check_triplet_PROMPT = \
    """
    给定主题C作为背景提供信息，请从4个四元组中，挑选出你认为正确的四元组并返回
    以下是一些上下文示例：
    ### triplets:
    （在欧洲冠军联赛中取得显著成就的西班牙俱乐部，包括利物浦、曼联、切尔西等）
    （英格兰的俱乐部，没有重大成就，欧冠，包括利物浦、曼联、切尔西等）
    （在英超联赛中取得显著成绩的英格兰俱乐部，包括利物浦、曼联、切尔西等）
    （在欧洲冠军联赛中取得显著成绩的英格兰俱乐部，但不包括利物浦、曼联、切尔西等）
    （在欧洲冠军联赛中取得显着成就的英格兰俱乐部，包括利物浦、曼联、切尔西等）
    ### triplet:
    （在欧洲冠军联赛中取得显着成就的英格兰俱乐部，包括利物浦、曼联、切尔西等）
    
    现在根据提供的title和triplets，请返回你认为正确的triplet：


    ### triplets:
    {triplets}

    ### triplet:

        
    
"""

correct_triplet_PROMPT = \
    """
    针对给定的背景主题，面对两个含有冲突元素的四元组，你的目标是通过删除冲突元素，而不是融合冲突元素，来创造一个无冲突的新四元组，如果两个四元组之间的矛盾无法通过删除冲突信息来解决，则返回空四元组。
    
    ### title:
    《林海雪原》中的人物设置和模式
    ### triplet1:
    《林海雪原》，承袭了，传统文学作品中的“英雄/美人”模式，人物设置
    ### triplet2:
    《林海雪原》，承袭了，传统文学作品中的“文武双全”模式，人物设置'
    ### correct_triplet:
    《林海雪原》，融合了，传统文学作品中的模式，人物设置

    现在根据提供的title和triplets，请帮我返回修改后的correct_triplet：

    ### title:
    {title}

    ### triplet1:
    {triplet1}
    
    ### triplet2:
    {triplet2}
    
    ### correct_triplet:



"""




def parse_correct_triple(text):
    pattern_list = r"(?:### correct_triplet:\n)?(\[.*?\])"
    match_list = re.search(pattern_list, text)
    if match_list:
        # 提取列表字符串
        list_str = match_list.group(1)

        # 将字符串表示的列表转换成Python列表
        try:
            list_obj = ast.literal_eval(list_str)
            for item in list_obj:
                # 对列表中的每个元素（四元组字符串）进行进一步处理
                return item
        except ValueError as e:
            print("列表字符串解析错误:", e)


def check_triplet(triplets):
    prompt = check_triplet_PROMPT.format(triplets=triplets)
    gpt4_sentence = generate_response(prompt, temperature=0.1)
    return gpt4_sentence


def correct_triplet(title, triplet1, triplet2):
    prompt = correct_triplet_PROMPT.format(title=title, triplet1=triplet1, triplet2=triplet2)
    gpt4_sentence = generate_response(prompt, temperature=0.1)
    gpt4_sentence = parse_correct_triple(gpt4_sentence)
    return gpt4_sentence


