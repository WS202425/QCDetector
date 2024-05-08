from Hull.pipeline.Utils.generate import generate_response
import re

triplet_to_sentence_PROMKPT = \
    """
    给定一个陈述。请你判断陈述的事实准确性。只有当陈述在事实上是不准确的时，才对陈述进行修改。如果陈述已经是准确的，则不需要进行任何修改，返回原陈述。
    在判断陈述时，请遵循以下原则：只有在事实上存在明显错误时进行修正，避免因表达方式不同而进行不必要的修改。
    
    以下是一些上下文示例：

    ### sentence:
    他被后人尊称为“贞观之治”的开创者。
    ### Correctness:
    True
    ### revise_sentence:
    他被后人尊称为“贞观之治”的开创者。
    
    ### sentence:
    尼尔·阿姆斯特朗是第一个登上火星的人。
    ### Correctness:
    False
    ### revise_sentence:
    尼尔·阿姆斯特朗是第一个登月的人。

    现在根据提供的 sentence，生成对应的Correctness, reverse_sentence：

    ### sentence:
    {sentence}
    
    ### Correctness:

    ### revise_sentence:


    """

Sentence_PROMPT = \
    """
    给定两个句子，你的任务是判断这两个句子是否内容一致。如果两个句子的意思相同，返回“True”，如果意思不同，返回“False”。在评估句子时，请考虑句子的整体意义，而不仅仅是文字或语法结构的相似性。
    
    ### 示例：
    revise_sentence: "佩尔修斯用美杜莎的头将他的敌人变成了石头。"
    sentence: "佩尔修斯用美杜莎的头将他的敌人变成了石像。"
    结果: True
    
    ### 任务：
    句子1: "{revise_sentence}"
    句子2: "{sentence}"
    
    ### 结果:

"""


def parse_Correctness_and_revise_sentence(text):
    # 正则表达式，用于提取Correctness值和修订后的句子
    pattern = r"(?:### Correctness:\s*)?(True|False)\s*### revise_sentence:\s*(.*)"

    # 使用re.search来查找匹配
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # 如果找到匹配，从捕获组中提取correctness和sentence
        correctness, sentence = match.groups()
        # 返回去除首尾空白的correctness和sentence
        return correctness, sentence.strip()
    else:
        # 如果没有找到匹配，返回None
        return None, None


def compare_sentences(revise_sentence, sentence):
    prompt = Sentence_PROMPT.format(revise_sentence=revise_sentence, sentence=sentence)
    gpt4_response = generate_response(prompt, temperature=0.1)
    return gpt4_response


def get_Correctness_and_revise_sentence(sentence):
    prompt = triplet_to_sentence_PROMKPT.format(sentence=sentence)
    gpt4_response = generate_response(prompt, temperature=0.1)
    Correctness, revise_sentence = parse_Correctness_and_revise_sentence(gpt4_response)
    if compare_sentences(revise_sentence, sentence) == "True":
        return compare_sentences(revise_sentence, sentence), sentence
    if revise_sentence is None:
        revise_sentence = sentence
    return Correctness, revise_sentence


# print(get_Correctness_and_revise_sentence("佩尔修斯杀死了怪物美杜莎"))
