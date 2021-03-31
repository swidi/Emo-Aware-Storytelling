import torch
from tqdm import tqdm
de2en = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.de-en', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt', tokenizer='moses', bpe='fastbpe')

de2en.eval()  # disable dropout

# The underlying model is available under the *models* attribute
#assert isinstance(de2en.models[0], fairseq.models.transformer.TransformerModel)

# Move model to GPU for faster translation
#de2en.cuda()

# Translate a sentence
print(de2en.translate('Hello world!'))
# 'Hallo Welt!'

# Batched translation
print(de2en.translate(['Hello world!', 'The cat sat on the mat.']))
# ['Hallo Welt!', 'Die Katze saß auf der Matte.']

#titles_file = open("titles.txt", "r")
stanzas_file = open("stanzas.txt", "r")

#titles_trans_file = open("titles_trans.txt", "w")
stanzas_trans_file = open("stanzas_trans.txt", "w")

#titles = titles_file.readlines()
stanzas = stanzas_file.readlines()
"""
for line in titles:
    print(line)
    trans = de2en.translate(line)
    print(trans)
    print("--------------------")
    titles_trans_file.write(trans + "\n")
titles_file.close()
titles_trans_file.close()
"""
for line in tqdm(stanzas):
    print(line)
    trans = de2en.translate(line)
    print(trans)
    print("--------------------")
    stanzas_trans_file.write(trans + "\n")

stanzas_file.close()
stanzas_trans_file.close()

