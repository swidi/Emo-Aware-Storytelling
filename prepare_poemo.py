import sys
from sklearn.model_selection import train_test_split

train_ratio = 0.80
validation_ratio = 0.10
test_ratio = 0.10
data_folder = "data/"

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
    if(emo in ["Beauty / Joy", "Humor", "Vitality"]):
        emo = "Joy"
    if(emo == "Annoyance"):
        emo = "Anger"
    if(emo == "Uneasiness"):
        emo = "Fear"
    if(emo in ["Nostalgia", "Awe / Sublime", "Suspense"]):
        emo = "Neutral"


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
  doPrint=False
  #print(len(poems))
  distStanza = {}
  distPoem = {}
  stats0 = {}
  stats1 = {}
  fourline=0
  """
  for poem in poems:
    n = len(poem)
    distPoem[n] = distPoem.get(n,0)+1
    if n==7 and doPrint: printpoem(poem)
    for stanza in poem:
      m = len(stanza)
      if m==2 and doPrint: printpoem(poem,flag=">>>")
      distStanza[m] = distStanza.get(m,0)+1
      if m==4: 
        printpoem([stanza],">>")
        fourline+=1
        emo1,emo2 = set(),set()
        for verse in stanza: 
          a0,a1 = verse[1],verse[2]
          for e in a0.split(" --- "): emo1.add(e)
          for e in a1.split(" --- "): emo2.add(e)
        e1 = len(emo1)
        e2 = len(emo2)
        stats0[e1] = stats0.get(e1,0)+1
        stats1[e2] = stats1.get(e2,0)+1 

  print(fourline)
  for e in sorted(stats0):
    print(e,stats0[e]/(sum(stats0.values())),stats1[e]/(sum(stats1.values())))

  print("=== Poems with n stanzas")
  for n in sorted(distPoem):
    print("n={}".format(n),distPoem[n])
  print("=== Stanzas with m lines")
  for m in sorted(distStanza):
    print("m={}".format(m),distStanza[m]) 
  """

  titles = [] 
  titles_file = open("titles.txt", "w")
  stories = [] 
  stories_file = open("stories.txt", "w")
  emotion_arcs = []
  emotion_arcs_file = open("emotion_arcs.txt", "w")

  title_train = open(data_folder + "train_x1.txt", "w")
  title_dev = open(data_folder + "dev_x1.txt", "w")
  title_test = open(data_folder + "test_x1.txt", "w")

  poem_train = open(data_folder + "train_x4.txt", "w")
  poem_dev = open(data_folder + "dev_x4.txt", "w")
  poem_test = open(data_folder + "test_x4.txt", "w")

  emotion_train = open(data_folder + "train_mapped.txt", "w")
  emotion_dev = open(data_folder + "dev_mapped.txt", "w")
  emotion_test = open(data_folder + "test_mapped.txt", "w")

  for poem in poems:
    titles.append(poem[0][0][0])
    stanzas = []
    emotions = []

    for stanza in poem:
      if(len(stanza) != 1): # Skip the title
        emotion = dict()

        stanza_string = ""
        for line in stanza:
          emotion = accumulate(emotion, line[1])
          emotion = accumulate(emotion, line[2])
          stanza_string += line[0] + " "
        stanza_string = stanza_string[:-1] # remove the last space
        stanza_emotion = keywithmaxval(emotion)

        emotions.append(stanza_emotion)
        stanzas.append(stanza_string)


    story = ' '.join(stanzas)
    emotion_arc = ' '.join(emotions)
    stories.append(story)# + " <|endoftext|>")
    emotion_arcs.append(emotion_arc)
  
  for line in titles:
    titles_file.write(line + "\n")
  for line in stories:
    stories_file.write(line + "\n")
  for line in emotion_arcs:
    emotion_arcs_file.write(line + "\n")


#  title_train_list, title_test_list, poem_train_list, poem_test_list, emotion_train_list, emotion_test_list = train_test_split(titles, stories, emotion_arcs, test_size=1 - train_ratio)
#  title_dev_list, title_test_list, poem_dev_list, poem_test_list, emotion_dev_list, emotion_test_list, = train_test_split(title_test_list, poem_test_list, emotion_test_list, test_size=test_ratio / (test_ratio + validation_ratio))

#  print("Split:")
#  print(len(title_train_list), len(title_test_list), len(title_dev_list))
#  title_train.write("\n".join(title_train_list))
#  title_train.close()
#  title_dev.write("\n".join(title_dev_list))
#  title_dev.close()
#  title_test.write("\n".join(title_test_list))
#  title_test.close()

#  poem_train.write("\n".join(poem_train_list))
#  poem_train.close()
#  poem_dev.write("\n".join(poem_dev_list))
#  poem_dev.close()
#  poem_test.write("\n".join(poem_test_list))
#  poem_test.close()
#
#  emotion_train.write("\n".join(emotion_train_list))
#  emotion_train.close()
#  emotion_dev.write("\n".join(emotion_dev_list))
#  emotion_dev.close()
#  emotion_test.write("\n".join(emotion_test_list))
#  emotion_test.close()
#  #stories.close()
#  #titles.close()
#  #emotion_arcs.close()


