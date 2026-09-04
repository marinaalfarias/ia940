freqa2=110
freqa5=880
freqb2=freqa2*(2**(1/12))
freqb5=freqa5*(2**(1/12))
delta1=freqb2-freqa2
delta2=freqb5-freqa5

print("a#2: ", freqb2)
print("delta1: ", delta1)
print("a#5: ", freqb5)
print("delta2: ", delta2)