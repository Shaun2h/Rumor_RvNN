import os
import ast
keyitem = ["twitter15","twitter16"]

within_t15t16 = {}
for item in keyitem:
    for treefile in os.listdir(os.path.join(item,"tree")):
        with open(os.path.join(item,"tree",treefile),"r",encoding="utf-8") as opened_treefile:
            newset = set()
            linecounter = 0  # the line count sees how many interactions for this particular tree. it includes retweets.
            
            for line in opened_treefile:
                z = line.strip().split("->")
                for i in z:
                    newlist = ast.literal_eval(i)
                    treeitem = newlist[1]
                    newset.add(treeitem)
                linecounter+=1
            newset.remove("ROOT") # remove the root that is pointing to the original item.
            roottweet = treefile.replace(".txt","")
            # you now have a list of all unique tweet reactions.
            participant_count = len(list(newset))
            within_t15t16[roottweet] = (participant_count,linecounter)
            

hertreeids = {}
herlabelfile = "../resource/data.TD_RvNN.vol_5000.txt"
with open(herlabelfile,"r",encoding="utf-8") as reference:
    for line in reference:
        target = line.strip().split("\t")[0]
        if not target in hertreeids:
            hertreeids[target] = 0
        hertreeids[target] = hertreeids[target] + 1


hers_more = []
hers_less = []
largeovershot = []

print("Trees do not use retweets, and they are hence ignored.")
print("Total trees:",len(list(within_t15t16.keys())))
for item in within_t15t16:
    if not within_t15t16[item][0]==hertreeids[item]:
        if hertreeids[item]>within_t15t16[item][0]:
            hers_more.append(item)
            if hertreeids[item]>within_t15t16[item][1]:
                largeovershot.append(item)
        else:
            hers_less.append(item)
            
print("Total trees where she has more tweets than in dataset (retweets are ignored):",len(hers_more))
print("Total trees where she has less tweets than in dataset (retweets are ignored):",len(hers_less))
print("Total trees where she has more tweets in the tree than total lines in the file itself in the dataset:",len(largeovershot))