import sys


c = 1

op1 = open("utt2spk","w")
op2 = open("wav.scp","w")

with open(sys.argv[1],"r") as f1:
    for line in f1:
        ofn = line.strip()
        ls = line.strip().split("/")
        f11 = ls[-1]
        spk = "spk_"+str(c)
        with open(f11.replace(".wav","_labels.txt"),"r") as f2:
            for line in f2:
                ls2 = line.strip().split("\t")
                if ls2[2] == "voice":
                    st = ls2[0]
                    et = ls2[1]
                    #if (float(et) - float(st)) >= 1.5 and (float(et) - float(st)) <= 2.9:
                    if (float(et) - float(st)) >= 3.0:
                        outfn = "dataset/"+spk+"_"+st.replace(".","-")+"_"+et.replace(".","-")+".wav"
                        cmd = "ffmpeg -y -i "+ofn+" -ss "+st+" -to "+et+" -ar 8000 -ac 1 "+outfn
                        print(cmd)
                        utt = spk+"_"+st.replace(".","-")+"_"+et.replace(".","-")
                        op1.write(utt+" "+spk+"\n")
                        op2.write(utt+" /home/sysadmin/sre/data/"+outfn+"\n")
        c += 1
