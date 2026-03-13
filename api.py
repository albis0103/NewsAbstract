import numpy as np
from gensim.models import KeyedVectors
print("wait for loading word2vec model")
model = KeyedVectors.load_word2vec_format("models/cc.en.300.vec", binary=False, limit=100000)
print("load sucess")
# 1. 擴充你的資安字典 (涵蓋縮寫與中文對應)
SECURITY_ALIASES = {
    "mde": "microsoft defender endpoint",
    "waf": "web application firewall",
    "edr": "endpoint detection response",
}

def get_word2vec(text, model):
    text = text.lower().strip()
    search_text = SECURITY_ALIASES.get(text, text)
    words = search_text.split()
    
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

# --- 測試執行 ---
# 假設你的 model 已經載入成功 (KeyedVectors.load_word2vec_format)
print(f"MDE vs Firewall: {get_similarity('MDE', 'firewall', model)}")
# print(f"防火牆 vs Firewall: {get_similarity('防火牆', 'firewall', model)}")