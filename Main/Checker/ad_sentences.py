from Hull.pipeline.Utils.generate import generate_response
import re

triplet_to_sentence_PROMKPT = \
    """
    我们的任务是针对给定的主题和相关的句子陈述，生成一组对抗性陈述，请注意生成的对抗性陈述要与原陈述有矛盾冲突
    请按照以下指导进行，并包括一个基于逻辑认为正确的修正陈述，同时确保每个修改都在逻辑上自洽且合理：
    1.识别和修正：首先，识别原始陈述中可能存在的错误或不足之处，并考虑一个合理的修正。这个修正应该基于历史事实、逻辑推理或常识。 
    2.生成对抗性陈述：根据指定的修改原则（谓语、宾体或附加信息的替换或添加否定词语），生成三个对抗性陈述，每个四元组都应反映出不同的视角或情境。 
    3.逻辑自洽性：确保所有生成的陈述在逻辑上都是自洽的，即使它们代表了不同的观点或情况。 
    以下是上下文示例：
    ### topic：
   （中秋节）
    ### sentence：
    （中秋节，又称月圆节、团圆节、嫦娥节等，是中国传统节日之一）
    ### sentences：
    （西班牙的俱乐部，取得了显著成就，欧洲冠军联赛，包括利物浦、曼联、切尔西等）
    （英格兰的俱乐部，未取得显著成就，欧洲冠军联赛，包括利物浦、曼联、切尔西等）
    （英格兰的俱乐部，取得了显著成就，英格兰足球超级联赛，包括利物浦、曼联、切尔西等）
    （英格兰的俱乐部，取得了显著成就，欧洲冠军联赛，但不包括利物浦、曼联、切尔西等）

    现在根据提供的主题背景和四元组，生成对抗性四元组：
    ### topic:
    {topic}

    ### sentence:
    {sentence}

    ### sentences0:

    ### sentences1:

    ### sentences2:

    ### sentences3:


    """


def get_list(input_str):
    # 根据中文括号进行分割，去除空字符串
    matches = re.findall(r"（(.*?)）", input_str)
    return matches


def get_ad_triplet(topic, sentence):
    prompt = triplet_to_sentence_PROMKPT.format(topic=topic, sentence=sentence)
    gpt4_response = generate_response(prompt)
    gpt4_response = get_list(gpt4_response)
    return gpt4_response


