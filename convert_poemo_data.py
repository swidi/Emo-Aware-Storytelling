f = open("poemo_dataset/tsv/emotion.german.tsv")

title = f.readline().strip()
f.readline()
print(title)

line = f.readline()
while(line.strip()!=""):
    (stanza, ano1, ano2) = line.split('\t')
    stanza = stanza.strip()
    ano1 = ano1.strip()
    ano2 = ano2.strip()

    print(stanza)
    print(ano1)
    print(ano2)
    line = f.readline()