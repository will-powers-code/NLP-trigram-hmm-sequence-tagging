import subprocess

# s = subprocess.run(f"python models.py tri dev 2 2 KBO 7 .8",shell=True, stdout=subprocess.PIPE)
# print(s.stdout[-10:])



maxZ = -1
maxTyp =  ""

for grams in range(2,8):
    for f in range(2,6):
        for d in map(lambda i:i/10, range(2,10,2)):
            process = subprocess.Popen(f"python models.py tri dev {f} 2 KBO {grams} {d}".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            z = float(out.decode("utf-8") .split()[-1])
            if z > maxZ:
                maxZ = z
                maxTyp = (f"{f},{grams},{d}")
        print(maxZ)
        print(maxTyp)

print(maxZ)
print(maxTyp)