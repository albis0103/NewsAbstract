import numpy as np
from gensim.models import KeyedVectors
import sys
import re
from deep_translator import GoogleTranslator
import json

print("wait for loading word2vec model")
model = KeyedVectors.load("models/fast_model.kv", mmap = 'r')
print("load sucess")

SECURITY_WORD_DICTIONARY = {
    "mde": "microsoft defender endpoint",
    "waf": "web application firewall",
    "edr": "endpoint detection response",
}
CUSTOMER_FEATURES_DB = {
    "北榮":["medical", "records", "HIS system"]
}

def is_chinese(text):
    # \u4e00-\u9fff 是 Unicode 中的中文範圍
    return bool(re.search(r'[\u4e00-\u9fff]', text))
def translate_english(text):
    try:
        translator = GoogleTranslator(source="zh-TW", target="en")
        translated_text = translator.translate(text)
        if translated_text:return translated_text
        else:return text
    except Exception as e:
        print(f"[error]翻譯服務異常:{e}")
        return text

def preprocess_text(text):
    if not text: return []
    cleaned_text = text.strip()
    if is_chinese(cleaned_text):
        cleaned_text = translate_english(cleaned_text)
    cleaned_text = cleaned_text.lower()
    search_text = SECURITY_WORD_DICTIONARY.get(cleaned_text, cleaned_text)
    words = search_text.split()
    return words



def get_word2vec(text, model):
    words = preprocess_text(text)
    #vector 紀錄words的語意分佈
    vectors = []
    for w in words:
        if w in model:
            vectors.append(model[w])
            
    if not vectors: return None
    vec_matrix = np.array(vectors)
    return np.max(vec_matrix, axis = 0)

def get_similarity(word1, word2, model):
    v1 = get_word2vec(word1, model)
    v2 = get_word2vec(word2, model)
    
    if v1 is None or v2 is None:
        return 0.0
        
    # 計算 Cosine Similarity (餘弦相似度)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    #linalg.norm() = 相量長度, 即np.linglg.norm(x) = ||x||
    if norm1 == 0 or norm2 == 0:
        return 0.0
    #similarity = cos(theta)  = A Similarity=cos(θ)= A⋅B / ||A|| ||B||
    return np.dot(v1, v2) / (norm1 * norm2)

def calculate_customer_similarity(customer_feature, news_keyword, model):
    if not customer_feature or not news_keyword: return 0.0

    probability_score = []
    for keyword in news_keyword:
        max_pi = 0.0
        for feature in customer_feature:
            similarity_score = get_similarity(feature, keyword, model)
            if similarity_score > max_pi : 
                max_pi = similarity_score
        probability_score.append(max_pi)
    final_similarity = sum(probability_score) / len(probability_score)
    return final_similarity

def main():
    try:
        news_input = sys.argv[1]
        news_keyword = [k.strip() for k in news_input.split(',')]
        
        results = {}
        for customer_name, features in CUSTOMER_FEATURES_DB.items():
            final_similarity = calculate_customer_similarity(features, news_keyword, model)
            results[customer_name] = round(float(final_similarity), 4)
        print(json.dumps(results, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error":str(e)}, ensure_ascii=False))
if __name__ == "__main__":
    main()