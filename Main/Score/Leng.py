import json
import os

# current_directory = os.path.dirname(__file__)
# input_path = os.path.join(current_directory, '../', 'Data', 'topics_responses_ZH_38_100.json')
with open("topics_responses.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 初始化变量
total_sentences = 0
total_length = 0
longest_response = ""
longest_response_length = 0
longest_sentence = ""
longest_sentence_length = 0
longest_response_sentence_count = 0

# 遍历数据计算所需的值
for item in data:
    response = item["response"]
    # 清理并分割句子
    sentences = response.strip().split("。")
    num_sentences = len(sentences)
    total_sentences += num_sentences
    total_length += len(response)
    if len(response) > longest_response_length:
        longest_response = response
        len_longest_response = len(response)
        longest_response_length = len(response)
        longest_response_sentence_count = num_sentences

    # 寻找最长的句子
    for sentence in sentences:
        if len(sentence) > longest_sentence_length:
            longest_sentence = sentence
            longest_sentence_length = len(sentence)

# 计算平均值
average_sentences = total_sentences / len(data)
average_length = total_length / len(data)

print(f"平均句子数: {average_sentences}")
print(f"平均长度: {average_length} 字符")
print(f"最长的response: {longest_response}")
print(f"最长的response长度: {len_longest_response}")
print(f"最长的response句子数: {longest_response_sentence_count}")
print(f"最长的句子长度: {longest_sentence_length} 字符")
print(f"最长的句子: {longest_sentence}")
