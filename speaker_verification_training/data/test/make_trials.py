import sys

dic1 = {}
with open("utt2spk","r") as f1:
    for line in f1:
        ls = line.split(" ")
        utt = ls[0].strip()
        spk = ls[1].strip()
        if spk not in dic1:
            lis = []
            lis.append(utt)
            dic1[spk] = lis
        else:
            lis = dic1[spk]
            lis.append(utt)
            dic1[spk] = lis

sd1 = open("trials_valid.txt","w")
k = 0
dic2 = dic1
for x in dic1:
    c = 0
    lis = dic1[x]
    for y in lis:
        sd1.write(x+" "+y+" target\n")
    for z in dic2:
        if x != z:
            lis1 = dic2[z]
            for w in lis1:
                sd1.write(x+" "+w+" nontarget\n")
        c = c + 1
    k = k + 1
    print(c,k)
