from sklearn.model_selection import train_test_split
data_folder="data_new/"
train_ratio=0.8
test_ratio=0.1
validation_ratio=0.1

titles = [] 
titles_file = open(data_folder+"titles_all.txt", "r")
titles = titles_file.read().splitlines()

stanzas = [] 
stanzas_file = open(data_folder+"stanzas_all.txt", "r")
stanzas = stanzas_file.read().splitlines()

emotion_arcs = []
emotion_arcs_file = open(data_folder+"emo_all.txt", "r")
emotion_arcs = emotion_arcs_file.read().splitlines()

title_train = open(data_folder + "train_x1.txt", "w")
title_dev = open(data_folder + "dev_x1.txt", "w")
title_test = open(data_folder + "test_x1.txt", "w")

poem_train = open(data_folder + "train_x4.txt", "w")
poem_dev = open(data_folder + "dev_x4.txt", "w")
poem_test = open(data_folder + "test_x4.txt", "w")

emotion_train = open(data_folder + "train_mapped.txt", "w")
emotion_dev = open(data_folder + "dev_mapped.txt", "w")
emotion_test = open(data_folder + "test_mapped.txt", "w")

title_train_list, title_test_list, poem_train_list, poem_test_list, emotion_train_list, emotion_test_list = train_test_split(titles, stanzas, emotion_arcs, test_size=1 - train_ratio)
title_dev_list, title_test_list, poem_dev_list, poem_test_list, emotion_dev_list, emotion_test_list, = train_test_split(title_test_list, poem_test_list, emotion_test_list, test_size=test_ratio / (test_ratio + validation_ratio))

print("Split:")
print(len(title_train_list), len(title_test_list), len(title_dev_list))
title_train.write("\n".join(title_train_list))
title_train.write("\n")
title_train.close()
title_dev.write("\n".join(title_dev_list))
title_dev.write("\n")
title_dev.close()
title_test.write("\n".join(title_test_list))
title_test.write("\n")
title_test.close()

poem_train.write(" <|endoftext|>\n".join(poem_train_list))
poem_train.write(" <|endoftext|>\n")
poem_train.close()
poem_dev.write(" <|endoftext|>\n".join(poem_dev_list))
poem_dev.write(" <|endoftext|>\n")
poem_dev.close()
poem_test.write(" <|endoftext|>\n".join(poem_test_list))
poem_test.write(" <|endoftext|>\n")
poem_test.close()

emotion_train.write("\n".join(emotion_train_list))
emotion_train.write("\n")
emotion_train.close()
emotion_dev.write("\n".join(emotion_dev_list))
emotion_dev.write("\n")
emotion_dev.close()
emotion_test.write("\n".join(emotion_test_list))
emotion_test.write("\n")
emotion_test.close()
stanzas_file.close()
titles_file.close()
emotion_arcs_file.close()

