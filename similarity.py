import numpy as np
from gensim.models import KeyedVectors
import sys
import re
from deep_translator import GoogleTranslator

print("wait for loading word2vec model")
model = KeyedVectors.load("models/fast_model.kv", mmap = 'r')
print("load sucess")

SECURITY_WORD_DICTIONARY = {
    "mde": "microsoft defender endpoint",
    "waf": "web application firewall",
    "edr": "endpoint detection response",
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

word1 = sys.argv[1]
word2 = sys.argv[2]
similarity_score = get_similarity(word1, word2, model)
print(similarity_score)