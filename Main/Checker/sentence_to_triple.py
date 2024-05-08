from Hull.pipeline.Utils.generate import generate_response
import re

triplet_to_sentence_PROMKPT = \
    """我们将通过一个Four_tuple（主体，谓语，宾语，附加信息）来简洁地描述一个历史事实。Four_tuple的目的是以最精确的方式传达关键信息，同时确保不丢失任何重要的事实细节，如时间、地点等，其中：
    - 主体是事实的主要主体或主角。
    - 谓语是描述主体的动作或状态。
    - 宾语是谓语作用的对象或结果。
    - 对于出生时间等特殊意义的时间、地点信息，必须保留。
    - 附加信息用于提供必要的背景信息或补充说明，但应保持简洁。
    
    ### 主题:
    李世民
    ### 原子事实:
    李世民以其卓越的政治智慧和军事才能，在中国历史上留下了不朽的功绩，被后人尊称为“贞观之治”的开创者。
    ### Four_tuple:
    （李世民，被尊称为，贞观之治的开创者，以其政治智慧和军事才能）
    
    ### 主题:
    艾伯特亲王
    ### 原子事实:
    艾伯特亲王（1819-1861）是德国王子，也是英国女王维多利亚的丈夫。
    ### Four_tuple:
    （艾伯特亲王（1819-1861），是，德国王子，同时也是英国女王维多利亚的丈夫）
    
    现在根据提供的主题背景和原子事实，生成Four_tuple：
    ### 任务：
    现在，请你根据以下主题背景和原子事实，生成相应的Four_tuple：
    ### 主题:
    {title}
    ### 原子事实:
    {sentence}
    请思考以下问题以形成四元组：
    1. 主体是谁？
    2. 谓语是什么动作或状态？
    3. 宾语是什么或者指的是什么？
    4. 附加信息是什么，如果原子事实信息不足，请使用主题背景信息来补充。
    根据上述回答，形成的Four_tuple是：
    ### Four_tuple:
    （主体，谓语，宾语，附加信息）

    """


def extract_triplet_from_text(text):
    # 定义正则表达式以匹配### triplet:后的四元组内容
    pattern = r"### Four_tuple:\s*\n*（(.*?)，(.*?)，(.*?)，(.*?)）"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # 使用.groups()来获取所有括号内的匹配组
        groups = match.groups()
        # 将匹配的组合成为一个字符串
        return "（{}，{}，{}，{}）".format(*groups)
    else:
        return None


def extract_triplet(title, sentence):
    max_attempts = 5  # 设定最大尝试次数，防止无限循环
    attempts = 0
    while attempts < max_attempts:
        prompt = triplet_to_sentence_PROMKPT.format(title=title, sentence=sentence)
        gpt4_response = generate_response(prompt)
        gpt4_response = extract_triplet_from_text(gpt4_response)
        if gpt4_response is not None:
            return gpt4_response
        attempts += 1
    return "No valid triplet found after multiple attempts"


