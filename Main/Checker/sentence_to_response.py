from Hull.pipeline.Utils.generate import generate_response

# SPO还原为句子
sentence_to_response_PROMPT = \
    """这里有主题C，以及一部分原子事实，请按照主题的背景信息，将原子事实拼接成一个完整的答复

    以下是一些上下文示例：


    ### title:
    欧洲冠军联赛（UEFA Champions League）的冠军球队所属国家

    ### sentences:
    欧洲冠军联赛自1955年创立以来，冠军球队来自多个欧洲国家。
    没有一个特定国家的俱乐部每年都赢得冠军。
    不同年份的冠军球队来自不同的国家，反映了欧洲足球实力的分布和变化。
    要获取每个赛季冠军球队及其所属国家的详细信息，建议查阅欧洲足联（UEFA）的官方网站或其他权威体育新闻资源。
    
    ### 候选答案:
    欧洲冠军联赛（UEFA Champions League）自1955年创立至今，吸引了来自多个欧洲国家的顶级足球俱乐部参与竞争。这项赛事没有一个特定国家的俱乐部能够每年都赢得冠军，冠军球队的所属国家随着每个赛季都有所变化，这种现象反映了欧洲各国足球实力的分布和周期性变化。
    为了了解每个赛季的冠军球队及其所属国家的详细信息，可以查阅欧洲足联（UEFA）的官方网站或参考其他权威的体育新闻资源。
    
    
    现在根据提供的title和sentences，请生成候选答案：

    ### title:
    {title}

    ### sentences:
    {sentences}

    ### 候选答案:

    """


def sentence_to_response(title, sentences):
    prompt = sentence_to_response_PROMPT.format(title=title, sentences=sentences)
    gpt4_sentence = generate_response(prompt)
    return gpt4_sentence


