import os
from gensim.models.fasttext import load_facebook_model

# 取得目前檔案所在的目錄，確保路徑在不同電腦都能跑
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "models", "cc.zh.300.bin")
model = load_facebook_model(model_path)

def get_relation_score(word1, word2):
    try:
        # 計算餘弦相似度 (Cosine Similarity)，範圍通常在 0 ~ 1 之間
        # 這代表了兩詞在語義空間的關聯機率
        score = model.wv.similarity(word1, word2)
        return score
    except KeyError:
        # 如果詞不在字典裡，返回 0
        return 0

# 測試
print(f"半導體 vs 晶圓: {get_relation_score('半導體', '晶圓')}") 
print(f"半導體 vs 珍珠奶茶: {get_relation_score('半導體', '珍珠奶茶')}")