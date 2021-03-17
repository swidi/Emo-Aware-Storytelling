import sys

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

  titles = open("titles.txt", "w")
  stories = open("stories.txt", "w")

  for poem in poems:
    titles.write(poem[0][0][0] + "\r\n")
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
        print(stanza)
        print(emotion)
        print(stanza_emotion)

        emotions.append(stanza_emotion)
        stanzas.append(stanza_string)
        print("===========")

    story = ' '.join(stanzas)
    emotion_arc = ' '.join(emotions)
    stories.write(story+"\n")# + " <|endoftext|>\r\n")
    print(story)
    print(emotion_arc)

  stories.close()
  titles.close()

  emo1 = []

