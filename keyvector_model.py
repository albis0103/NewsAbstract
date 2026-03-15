from gensim.models import KeyedVectors
#將模型預載入，讓news summary()以mmap讀取，加速
print("loading the original .vec file (will wait about 10 sec~)")
model = KeyedVectors.load_word2vec_format("models/cc.en.300.vec", binary=False, limit=100000)
print("transform to .kv and .npy that can support mmap")
model.save("models/fast_model.kv")#會自動產生gensim專屬.kv and .npy支援mmap