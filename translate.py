import torch
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

titles_file = open("titles.txt", "r")
stories_file = open("stories.txt", "r")

titles_trans_file = open("titles_trans.txt", "w")
stories_trans_file = open("stories_trans.txt", "w")

titles = titles_file.readlines()
stories = stories_file.readlines()

for line in titles:
    print(line)
    trans = de2en.translate(line)
    print(trans)
    print("--------------------")
    titles_trans_file.write(trans + "\n")
titles_file.close()
titles_trans_file.close()

for line in stories:
    print(line)
    trans = de2en.translate(line)
    print(trans)
    print("--------------------")
    stories_trans_file.write(trans + "\n")

stories_file.close()
stories_trans_file.close()

