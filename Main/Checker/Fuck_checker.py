import json
import os
import logging
from New.Checker.ad_triplet import get_ad_triplet
from New.Checker.check_triplet import check_triplet, correct_triplet
from New.Checker.equal import equal
from New.Checker.response_to_title_and_sentence import  response_to_sentence
from New.Checker.select_sentence import get_Correctness_and_revise_sentence
from New.Checker.sentence_to_response import sentence_to_response
from New.Checker.sentence_to_triple import extract_triplet
from New.Checker.triple_to_sentence import triplet_to_sentence
from tqdm import tqdm
import chardet

current_directory = os.path.dirname(__file__)
input_path = os.path.join(current_directory, '../', 'Data', 'test.json')
output_path = os.path.join(current_directory, '../', 'Data', 'Checking_test_01.json')
logging.basicConfig(filename='checking.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def extract():
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
        detected_hull_indices = []
        response = item["response"]
        # 模型回答转换为句子对
        sentences = response_to_sentence(response)
        title = item.get("prompt", None)
        item['sentences'] = sentences
        # 遍历句子对
        for index, sentence in enumerate(sentences):
            hull = 0
            corr, revise_sentence = get_Correctness_and_revise_sentence(sentence)
            print("sentence" + sentence)
            print("revise_sentence" + revise_sentence)
            print(corr)
            if corr == "False":  # 如果原句子是假的
                hull = 1
                pre_sentence = sentence
                sentence = revise_sentence
                item['ad_revise_sentence'] = sentence
                pre_four_triplet = extract_triplet(title, pre_sentence)
                four_triplet = extract_triplet(title, sentence)
                sentence, num, ad_four_triplets = check(hull, sentence, title, four_triplet, pre_four_triplet)
            else:
                four_triplet = extract_triplet(title, sentence)
                sentence, num, ad_four_triplets = check(hull, sentence, title, four_triplet)
            hull = max(num, hull)
            if hull == 1:
                detected_hull_indices.append(index)
            item[f"{four_triplet}_hull_num"] = hull
            local_Hull_num += hull
            item[f"{four_triplet}_ads"] = ad_four_triplets
            item[f"{four_triplet}_select_sentence"] = sentence
            final_sentences.append(sentence)
        # 累加幻觉次数
        hull_num += local_Hull_num
        # 最终回复
        Checking_response = sentence_to_response(title, final_sentences)
        # 正确预测的数量
        item["correct_predictions"], item["correct_predictions_num"] = correct_predict(detected_hull_indices,
                                                                                       item["hull_index"])
        item["final_sentences"] = final_sentences
        item["Checking_response"] = Checking_response
        # 写入
        item["local_Hull_num"] = local_Hull_num
        # 写入
        output_data.append(item)
        with open(output_path, "w", encoding='utf-8') as fp:
            json.dump(output_data, fp, indent=2, ensure_ascii=False)
    print('Extraction completed and output saved.')
    print(hull_num)


# 检查四元组是否正确
def check(hull, sentence, title, four_triplet, pre_four_triplet=None):
    ad_four_triplets = get_ad_triplet(title, four_triplet)
    ad_four_triplets.append(four_triplet)
    if hull == 1:  # 如果原句子发生了幻觉
        ad_four_triplets.append(pre_four_triplet)
        four_triplet_temp = check_triplet(ad_four_triplets)
        triplet_final = correct_triplet(title, pre_four_triplet, four_triplet_temp)
        if not triplet_final:
            sentence = None
        else:
            sentence = triplet_to_sentence(title, triplet_final)
    else:
        four_triplet_temp = check_triplet(ad_four_triplets)
        boolean = equal(four_triplet, four_triplet_temp)
        if boolean:
            sentence = sentence
        else:
            hull = 1
            triplet_final = correct_triplet(title, four_triplet, four_triplet_temp)
            if not triplet_final:
                sentence = None
            else:
                sentence = triplet_to_sentence(title, triplet_final)

    return sentence, hull, ad_four_triplets


def correct_predict(detected_hull_indices, hull_index):
    correct_predictions = [index for index in detected_hull_indices if index in hull_index]
    return correct_predictions, len(correct_predictions)


def main():
    extract()


if __name__ == "__main__":
    main()
