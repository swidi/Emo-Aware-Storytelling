import sys
from sklearn.model_selection import train_test_split

train_ratio = 0.80
validation_ratio = 0.10
test_ratio = 0.10
data_folder = "data/"
insert_end_of_line = True

def readPoems(fn):
    poems = []
    poem = []
    stanza = []
    prev_line = None
    for line in open(fn):
        line = line.strip()
        if line=="":
            if prev_line=="":
                if poem!=[]:
                    poems.append(poem)
                    poem=[]
            else:
                if stanza!=[]: poem.append(stanza)
                stanza = []
        else:
            stanza.append(line.split("\t"))
        prev_line = line
    if poem!=[]: poems.append(poem)
    return poems

def printpoem(poem,flag=""):
    for s in poem:
        for line in s:
            print(flag,line)
        print()

def accumulate(dict, string):
    for emo in string.split(" --- "):
        if(emo in ["Beauty / Joy"]): #"Humor", "Vitality"]):
            emo = "Joy"
        #if(emo == "Annoyance"):
        #    emo = "Anger"
        #if(emo == "Uneasiness"):
        #    emo = "Fear"
        #if(emo in ["Nostalgia", "Awe / Sublime", "Suspense"]):
        #    emo = "Neutral"
        if(emo == "Awe / Sublime"):
            emo = "Awe"


        if (emo in dict):
            dict[emo] += 1
        else:
            dict[emo] = 1
    return dict

def keywithmaxval(d):
    """ a) create a list of the dict's keys and values;
        b) return the key with the max value"""
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]

if __name__ == "__main__":
    poems = readPoems(sys.argv[1])

    titles = []
    titles_file = open("titles.txt", "w")
    stanzas = []
    stanzas_file = open("stanzas.txt", "w")
    emotion_arcs = []
    emotion_arcs_file = open("emotion_arcs.txt", "w")

    for poem in poems:
        title = poem[0][0][0]
        stanzas = []
        emotions = []

        for stanza in poem:
            print(stanza)
            if(len(stanza) != 1): # Skip the title
                emotion = dict()

                stanza_string = ""

                for line in stanza:
                    emotion = accumulate(emotion, line[1])
                    if len(line) == 3:
                        emotion = accumulate(emotion, line[2])
                    stanza_string += line[0] + " "
                print(emotion)
                emotion = keywithmaxval(emotion)
                print(emotion)

                emotion_arcs_file.write(emotion + "\n")
                titles_file.write(title + "\n")
                stanzas_file.write(stanza_string + "\n")

        stanza = ' '.join(stanzas)
        emotion_arc = ' '.join(emotions)
        stanzas.append(stanza)# + " <|endoftext|>")
