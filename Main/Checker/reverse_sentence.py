from Hull.pipeline.Utils.generate import generate_response

get_reverse_sentence_PROMKPT = \
    """请你帮我将一个陈述句转换为倒装句。在转换过程中，请遵循以下指导原则：
    1. 识别句子成分：明确句子的主语、谓语、宾语以及时间、地点等状语。
    2. 确定主次关系：对于包含多个信息或事件的句子，需要识别主要信息或事件以及次要或补充信息。
    3. 应用倒装规则：重点对主要事件或信息进行倒装处理，确保倒装后的句子在逻辑上是清晰的，同时保持语言流畅和自然。倒装时应优先考虑语言的自然度和避免逻辑错误。
    4. 注意细节：在转换过程中，确保所有人名、地名和专有名词的准确性不受影响，保持句子原有的意义不变。
    
    请参考以下示例：

    ### sentence:
    李世民是唐朝第二任皇帝，年号贞观
    ### reverse_sentence:
    唐朝第二任皇帝是李世民，年号贞观
    
    ### sentence:
    昨天，我们在公园里看到了一只稀有的鸟
    ### reverse_sentence:
    唐朝第二任皇帝是李世民，年号贞观
    昨天，在公园里我们看到了一只稀有的鸟

    现在根据提供的sentence，生成reverse_sentence：


    ### sentence:
    {sentence}

    ### reverse_sentence:


    """


def get_reverse_sentence(sentence):
    prompt = get_reverse_sentence_PROMKPT.format(sentence=sentence)
    gpt4_response = generate_response(prompt)
    return gpt4_response


# print(get_reverse_sentence("他是唐太宗李世民与文皇后萧氏之长子"))
