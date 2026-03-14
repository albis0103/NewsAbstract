from gensim.models import KeyedVectors
print("loading the original .vec file (will wait about 10 sec~)")
model = KeyedVectors.load_word2vec_format("models/cc.en.300.vec", binary=False, limit=100000)
print("transform to .bin that can support mmap")
model.save("models/fast_model.kv")#會自動產生gensim專屬.kv and .npy支援mmap