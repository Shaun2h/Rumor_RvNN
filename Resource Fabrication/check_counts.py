keynums = {}
with open("data.BU_RvNN.vol_5000.txt",encoding="utf-8") as tdfile:
    for line in tdfile:
        if line:
            z = line.split()[5:]
            for i in z:
                if not i.split(":")[0] in keynums:
                    keynums[i.split(":")[0]]=0
                keynums[i.split(":")[0]] = keynums[i.split(":")[0]]+int(i.split(":")[1])
print("number of tokens considered:" , len(list(keynums.keys())))
grouper = {}
for i in keynums:
    if not keynums[i] in grouper:
        grouper[keynums[i]] = []
    grouper[keynums[i]].append(i)
    
grouper = {k: v for k, v in sorted(grouper.items(), key=lambda item: item[0])}
# print(grouper)