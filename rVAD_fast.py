from __future__ import division
import numpy 
import pickle
import os
import sys
import math
import code
from scipy.signal import lfilter
import speechproc
from copy import deepcopy

# Refs:
#  [1] Z.-H. Tan, A.k. Sarkara and N. Dehak, "rVAD: an unsupervised segment-based robust voice activity detection method," Computer Speech and Language, 2019. 
#  [2] Z.-H. Tan and B. Lindberg, "Low-complexity variable frame rate analysis for speech recognition and voice activity detection." 
#  IEEE Journal of Selected Topics in Signal Processing, vol. 4, no. 5, pp. 798-807, 2010.

# 2017-12-02, Achintya Kumar Sarkar and Zheng-Hua Tan

# Usage: python rVAD_fast_2.0.py inWaveFile  outputVadLabel


winlen, ovrlen, pre_coef, nfilter, nftt = 0.025, 0.01, 0.97, 20, 512
ftThres=0.5; vadThres=0.4
opts=1

finwav=str(sys.argv[1])
fn = finwav.split("/")[-1].replace(".wav","")
print("fn : ",fn)
fvad=fn+"_vad.txt"

fs, data = speechproc.speech_wave(finwav)   
print("len(data) : ",len(data))

ft, flen, fsh10, nfr10 =speechproc.sflux(data, fs, winlen, ovrlen, nftt)



# --spectral flatness --
pv01=numpy.zeros(nfr10)
pv01[numpy.less_equal(ft, ftThres)]=1 
pitch=deepcopy(ft)

pvblk=speechproc.pitchblockdetect(pv01, pitch, nfr10, opts)


# --filtering--
ENERGYFLOOR = numpy.exp(-50)
b=numpy.array([0.9770,   -0.9770])
a=numpy.array([1.0000,   -0.9540])
fdata=lfilter(b, a, data, axis=0)


print("len(fdata) : ",len(fdata))
#--pass 1--
noise_samp, noise_seg, n_noise_samp=speechproc.snre_highenergy(fdata, nfr10, flen, fsh10, ENERGYFLOOR, pv01, pvblk)

print("len(noise_samp) : ",len(noise_samp))
print("noise_seg : ",len(noise_seg))
#sets noisy segments to zero

for j in range(n_noise_samp):
    fdata[range(int(noise_samp[j,0]),  int(noise_samp[j,1]) +1)] = 0 

print("len(fdata) : ",len(fdata))
print("pv01 : ",len(pv01))
print("pvblk : ",len(pvblk))

vad_seg=speechproc.snre_vad(fdata,  nfr10, flen, fsh10, ENERGYFLOOR, pv01, pvblk, vadThres)

print("len(vad_seg) : ",len(vad_seg))
# print("vad_seg.astype(int) : ",vad_seg.astype(int))
numpy.savetxt(fvad, vad_seg.astype(int),  fmt='%i')
print("%s --> %s " %(finwav, fvad))

idx = 1
zero_count = 0 
one_count = 0
time_tracker = 0

op = open(fn+"_labels.txt","w")
op2 = open(fn+"_segments.txt","w")

for x in vad_seg.astype(int):
	if x == 0:
		if one_count > 0:
			t1 = one_count * 0.01
			st = time_tracker
			time_tracker += t1
			print("voice : ",t1)
			print(st," : ",time_tracker)
			op.write(str(st)+"\t"+str(time_tracker)+"\tvoice\n")
			op2.write(fn+"-"+str(st).replace(".","")+"-"+str(time_tracker).replace(".","")+" "+fn+" "+str(st)+" "+str(time_tracker)+"\n")
		one_count = 0
		zero_count += 1
	else:
		if zero_count > 0:
			t2 = zero_count * 0.01
			st = time_tracker
			time_tracker += t2
			print("unvoice : ",t2)
			print(st," : ",time_tracker)
			op.write(str(st)+"\t"+str(time_tracker)+"\tunvoice\n")
			op2.write(fn+"-"+str(st).replace(".","")+"-"+str(time_tracker).replace(".","")+" "+fn+" "+str(st)+" "+str(time_tracker)+"\n")
		zero_count = 0
		one_count += 1

data=None; pv01=None; pitch=None; fdata=None; pvblk=None; vad_seg=n_noise_samp
