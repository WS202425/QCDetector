from Hull.pipeline.Utils.generate import generate_response
import re
triplet_to_sentence_PROMKPT = \
    """
   我们的任务是根据给定的主题和相关的四元组（主语，谓语，宾语，附加信息），生成三个对抗性四元组和一个经过事实修正的四元组。请遵循以下指导原则，同时确保每个修改都在逻辑上自洽且合理：

    1. 根据指定的修改原则进行操作，可以是谓语、宾语或附加信息的替换，或在其中添加否定词语。不可以修改主语。
    2. 生成的三个对抗性四元组应反映不同的视角或情境，且只在一个单元内发生改动。改动后的四元组需要存在不明显的逻辑漏洞，并与原四元组形成矛盾冲突。
    3. 请你判断原四元组是否包含隐藏的错误信息，如果包含错误，请生成一个经过事实修正的四元组。

    以下是上下文示例：
    ### title：
    李世民
    ### triplet：
    （李世民，是，唐太宗李世民与文皇后萧氏之长子，）
    ### ad_triplets：
    （李世民，不是，唐太宗李世民与文皇后萧氏之长子，）
    （李世民，是，唐太宗李世民与其他王妃之子，）
    （李世民，是，唐太宗李世民与文皇后萧氏之外甥，）
    （李世民，是，唐高祖李渊与太穆皇后窦氏之次子，）
    
    现在根据提供的主题背景和四元组，生成对抗性四元组：
    ### 主题:
    {title}
    
    ### triplet:
    {triplet}
    
    ### ad_triplets0:
    
    ### ad_triplets1:
    
    ### ad_triplets2:
    
    ### ad_triplets3:
    

    """


def get_list(input_str):
    # 根据中文括号进行分割，去除空字符串
    matches = re.findall(r"（(.*?)）", input_str)
    return matches


def get_ad_triplet(title, triplet):
    attempts = 0  # 设置尝试次数计数器
    while attempts < 5:  # 限制最大尝试次数为10次以避免无限循环
        prompt = triplet_to_sentence_PROMKPT.format(title=title, triplet=triplet)
        gpt4_response = generate_response(prompt)
        ad_triplets = get_list(gpt4_response)
        if ad_triplets:  # 检查是否获得了非空结果
            return ad_triplets
        attempts += 1
    return None
