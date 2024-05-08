from Hull.pipeline.Utils.generate import generate_response, generate_responses
import re

from New.Checker.ad_triplet import get_list

# 判断ad_SPO三元组是否正确，如果正确，返回True，反之返回False。当返回True时，说明出现幻觉，就需要消除幻觉
response_to_title_PROMPT = \
    """
    给定一段问答文本，请分析出这段文本的主题

    以下是一些上下文示例：
    
    ### question:
    月亮上有一颗什么树？

    ### answer:
    在中国古代神话传说中，月亮上有一颗桂花树。这一设定尤其与嫦娥奔月的故事相关联。据说，嫦娥在飞升到月亮后，居住在了广寒宫，而广寒宫旁就生长着一颗桂花树。
    每到中秋时节，桂花盛开，香气四溢，因此中秋节也被称为“桂花节。

    ### title：
    中国古代神话传说中的月亮与桂花树，以及嫦娥奔月故事和中秋节的文化背景。
    

    现在根据提供的文本，请生成对应的title
    ### question:
    {question}
     ### answer:
    {answer}
    
    ### title:



"""

response_to_sentence_PROMPT = \
    """
    请根据提供的文本，细致地将其分解成原子事实。在分解过程中，请确保：
    - 每个句子都尽可能地包含一个完整的信息单位,每个句子尽可能地包含一个完整的信息单位，且在适当情况下，将因果关系或相关联的信息合并为一个原子事实。
    - 特别注意不要遗漏关键的人物、事件、时间和地点信息。
    - 尝试保持原有的逻辑结构和信息的丰富度，如有可能，以时间顺序或因果关系组织句子。
    - 如果原文中含有复杂的事件或概念，请提供简要的解释或背景信息，以保证句子的独立性和完整性。

    以下是一些上下文示例：

    ### C:在中国古代神话传说中，月亮上有一颗桂花树。这一设定尤其与嫦娥奔月的故事相关联。据说，嫦娥在飞升到月亮后，居住在了广寒宫，而广寒宫旁就生长着一颗桂花树。每到中秋时节，桂花盛开，香气四溢，因此中秋节也被称为“桂花节。

    ### Sentences：
    在中国古代神话传说中，月亮上生长有一颗桂花树。
    桂花树与嫦娥奔月的故事紧密相关。
    嫦娥飞升到月亮后，居住在广寒宫。
    广寒宫旁生长着一颗桂花树。
    每到中秋时节，桂花盛开，香气四溢。
    中秋节因桂花盛开而被称为“桂花节”。


    现在根据提供的文本，请生成对应的Sentences
    ### C:
    {C}

    ### Sentences：

"""


def response_to_title(question, answer):
    prompt = response_to_title_PROMPT.format(question=question, answer=answer)
    title = generate_response(prompt, temperature=0.5)
    return title


def response_to_sentence(C):
    prompt = response_to_sentence_PROMPT.format(C=C)
    gpt4_sentence = generate_response(prompt, temperature=0.2)
    sentences = [sentence.strip() for sentence in gpt4_sentence.strip().split("\n")]
    return sentences


# print(response_to_sentence(""""李世民（598年－649年），唐朝第二任皇帝，年号贞观（627年-649年在位），是中国历史上杰出的政治家和军事家之一。他是唐太宗李世民与文皇后萧氏之长子，因其在位期间实行改革开放，使贞观盛世成为中国历史上政治最为清明、经济最为繁荣的一个时期。\n\n李世民在位期间实行了一系列改革，包括推行科举制度、加强中央集权、推行均田制和租庸调制、减轻赋税和劳役、改革度牧制度等，进一步巩固了唐朝的统治地位。他还大力发展农业、商业和手工业，建设水利工程，修筑长城等，使得唐朝的国力得以进一步提升。\n\n在外交方面，李世民积极开展各种外交活动，加强了与邻国的关系，与突厥、吐蕃等民族进行外交联姻，巩固了唐朝的边疆安全。此外，他还率领军队进行了一系列战争，扩大了唐朝的疆土，使之达到鼎盛时期。\n\n李世民以其卓越的政治智慧和军事才能，在中国历史上留下了不朽的功绩，被后人尊称为“贞观之治”的开创者。",
#   """))

# 《林海雪原》中的人物设置和传统文学中的英雄美人模式
# ['《林海雪原》中的人物设置承袭了传统文学作品中的“英雄/美人”模式。', '少剑波是一位能文能武的“儒将”。', '白茹是一位美丽多情的女卫生员。']
