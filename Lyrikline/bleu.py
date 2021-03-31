import nltk
import os

english = []
trans = []
    
with os.scandir("lyrikline") as it:
    for entry in it:
        if "EN" in entry.name and entry.is_file():
            english.append(entry.path)
        elif entry.name.endswith("trans") and entry.is_file():
            trans.append(entry.path)
if(len(english) != len(trans)):
    print("Not all files translated!")
english.sort()
trans.sort()

eng_corpus = []
trans_corpus = []
for i in range(len(english)):
    eng_file = open(english[i], "r")
    trans_file = open(trans[i], "r")

    eng_words = eng_file.read().split()
    trans_words = trans_file.read().split()
    
    eng_corpus.append([eng_words])
    trans_corpus.append(trans_words)
    print(english[i])
    bleu = nltk.translate.bleu_score.sentence_bleu([eng_words], trans_words)
    print(bleu)

    eng_file.close()
    trans_file.close()
    print("====================")


print(nltk.translate.bleu_score.corpus_bleu(eng_corpus, trans_corpus, weights=(1, 0, 0, 0)))
print(nltk.translate.bleu_score.corpus_bleu(eng_corpus, trans_corpus, weights=(1/2., 1/2., 0, 0)))
print(nltk.translate.bleu_score.corpus_bleu(eng_corpus, trans_corpus, weights=(1/3., 1/3., 1/3., 0)))
print(nltk.translate.bleu_score.corpus_bleu(eng_corpus, trans_corpus, weights=(1/4., 1/4., 1/4., 1/4.)))
