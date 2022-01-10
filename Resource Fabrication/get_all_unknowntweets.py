import os
import ast
import json

viewedlist = set()
tweetz = set()
for settype in ["twitter15","twitter16"]:
    treeitems = os.path.join(settype,"tree")
    alltreefiles = os.listdir(treeitems)
    sourcefile = os.path.join(settype,"source_tweets.txt")
    
    with open(sourcefile,"r",encoding="utf-8") as sourcedfile:
        for line in sourcedfile:
            if line:
                viewedlist.add(line.split("\t")[0])
    for treefile in alltreefiles:
        with open(os.path.join(treeitems,treefile),"r",encoding="utf-8") as latestfile:
            for line in latestfile:
                if line:
                    z = line.split("->")
                    item1 = ast.literal_eval(z[0])[1]
                    item2 = ast.literal_eval(z[1])[1]
                    for thing in [item1,item2]:
                        if thing=="ROOT":
                            tweetz.add(treefile.replace(".txt",""))
                        else:
                            tweetz.add(str(thing))
                        
unseen = []
for i in list(tweetz):
    if not i in viewedlist:
        unseen.append(i)
print("Within: ",len(tweetz))
print("Provided: ",len(viewedlist))
print("Unseen: ",len(unseen))

with open("unseentweetslist.txt","w",encoding="utf-8") as openedfile:
    json.dump(unseen,openedfile)
                    
