import json
import os
import logging
from New.Checker.ad_triplet import get_ad_triplet
from New.Checker.check_triplet import check_triplet, correct_triplet
from New.Checker.equal import equal
from New.Checker.response_to_title_and_sentence import response_to_sentence
from New.Checker.select_sentence import get_Correctness_and_revise_sentence
from New.Checker.sentence_to_response import sentence_to_response
from New.Checker.sentence_to_triple import extract_triplet
from New.Checker.triple_to_sentence import triplet_to_sentence
from tqdm import tqdm
import chardet

current_directory = os.path.dirname(__file__)
input_path = os.path.join(current_directory, '../', 'Data/MainTestSet', 'test.json')
output_path = os.path.join(current_directory, '../', 'Data/MainTestSet', 'Checking_test_01.json')
logging.basicConfig(filename='checking.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def extract_sentence():
    QC_index = []
    print('loading MainTestdata.text')
    with open(input_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    with open(input_path, 'r', encoding=encoding) as fp:
        data = json.load(fp)
    # extract triplets
    hull_num = 0
    print('Extracting and Checking')
    output_data = []
    for item in tqdm(data):
        local_Hull_num = 0
        assert "response" in item, "response field is required"
        final_sentences = []
        response = item["response"]
        # question = item.get("topic.txt", None)
        # 模型回答转换为句子对
        sentences = response_to_sentence(response)
        # 提取模型回答的主题
        # title = response_to_title(question, response)
        title = item.get("prompt", None)
        item['sentences'] = sentences
        # 遍历句子对
        for index, sentence in enumerate(sentences):
            # 测试倒装句子，查看模型是否认同倒装句，不认同的话判定为发生幻觉，采用新回答替代原句子
            # reverse_sentence = get_reverse_sentence(sentence)
            hull, revise_sentence = sentence_check(item, title, sentence)
            local_Hull_num += hull
            if revise_sentence is not None:
                final_sentences.append(revise_sentence)
            else:
                print("revise_sentence is None")
            if hull == 1:
                QC_index.append(index)
        # 累加幻觉次数
        hull_num += local_Hull_num
        Checking_response = sentence_to_response(title, final_sentences)
        item["final_sentences"] = final_sentences
        item["Checking_response"] = Checking_response
        # 写入
        item["local_Hull_num"] = local_Hull_num
        item["QC_index"] = QC_index
        # 写入
        output_data.append(item)
        with open(output_path, "w", encoding='utf-8') as fp:
            json.dump(output_data, fp, indent=2, ensure_ascii=False)
    print('Extraction completed and output saved.')
    print(hull_num)


def sentence_check(item, title, sentence):
    hull = 0
    corr, revise_sentence = get_Correctness_and_revise_sentence(sentence)
    print("sentence" + sentence)
    print("revise_sentence" + revise_sentence)
    print(corr)
    if corr == "False":  # 如果原句子是假的
        pre_sentence = sentence
        sentence = revise_sentence
        item['ad_revise_sentence'] = sentence
        pre_four_triplet = extract_triplet(title, pre_sentence)
        four_triplet = extract_triplet(title, sentence)
        sentence, num, ad_four_triplets = check(corr, hull, sentence, title, four_triplet, pre_four_triplet)
    else:
        four_triplet = extract_triplet(title, sentence)
        sentence, num, ad_four_triplets = check(corr, hull, sentence, title, four_triplet)
    hull = max(num, hull)
    item[f"{four_triplet}_hull_num"] = hull
    item[f"{four_triplet}_ads"] = ad_four_triplets
    item[f"{four_triplet}_select_sentence"] = sentence
    return hull, sentence


# 检查四元组是否正确
def check(corr, hull, sentence, title, four_triplet, pre_four_triplet=None):
    ad_four_triplets = get_ad_triplet(title, four_triplet)  # 生成对抗性四元组
    ad_four_triplets.append(four_triplet)  # 添加四元组

    if corr == "False":  # 原句子为错误的情况
        ad_four_triplets.append(pre_four_triplet)  # 添加原句子四元组
    four_triplet_temp = check_triplet(ad_four_triplets)  # 筛选候选四元组

    if equal(four_triplet, four_triplet_temp):  # 如果候选四元组是四元组返回原句子、判断幻觉数量为0、对抗性四元组
        return sentence, hull, ad_four_triplets

    # 修改四元组
    if corr == "False":  # 原句子为错误的情况
        triplet_final = correct_triplet(title, pre_four_triplet, four_triplet_temp)
    else:
        triplet_final = correct_triplet(title, four_triplet, four_triplet_temp)
    hull = 1  # 判断幻觉数量为1

    if not triplet_final:
        sentence = None  # 矛盾无法缓解，删除原句子
    else:
        sentence = triplet_to_sentence(title, triplet_final)  # 四元组还原为句子
    return sentence, hull, ad_four_triplets


def main():
    extract_sentence()


if __name__ == "__main__":
    main()
