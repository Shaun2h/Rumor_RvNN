import os
import json
import csv
from datetime import datetime
if __name__=="__main__":
    homedir = "all-rnr-annotated-threads"
    topicalname = os.listdir(homedir)
    convenient_dictionary = {"charliehebdo":(0,1,2,3),
            "ebola-essien":(0,1,2,3),
            "ferguson":(4,5,6,7),
            "germanwings-crash":(8,9,10,11),
            "gurlitt":(12,13,14,15),
            "ottawashooting":(16,17,18,19),
            "prince-toronto":(20,21,22,23),
            "putinmissing":(24,25,26,27),
            "sydneysiege":(28,29,30,31)}
            
            
            
    dumpdir = "fake_tree"
    if not os.path.exists(dumpdir):
        os.mkdir(dumpdir)
    labelfile_txtlist = []        
    texts = {}
    access_list = [("tweetid","id"), ("userid",["user","id"]), ("user_display_name",["user","name"]), ("user_screen_name",["user","screen_name"]), ("user_reported_location",["user","location"]), ("user_profile_description",["user","description"]), ("user_profile_url",["user","url"]), ("follower_count",["user","followers_count"]), ("following_count",["user","friends_count"]), ("account_creation_date",["user","created_at"]), ("account_language",["user","lang"]), ("tweet_language",["user","id"]), ("tweet_text","text"), ("tweet_time","created_at"), ("tweet_client_name","source"), ("in_reply_to_userid","in_reply_to_user_id"), ("in_reply_to_tweetid","in_reply_to_status_id"), ("quoted_tweet_tweetid",""), ("is_retweet","retweeted"), ("retweet_userid",""), ("retweet_tweetid",""), ("latitude",""), ("longitude",""), ("quote_count",""), ("reply_count",""), ("like_count","favorite_count"), ("retweet_count","retweet_count"), ("hashtags",["entities","hashtags"]), ("urls",["entities","urls"]), ("user_mentions",["entities","user_mentions"]), ("poll_choices","")]
    def pheme_accessor(access_list,targetjson):
        # return a list of whatever to write in that row for daniel's CSV
        outlist = []
        # print(access_list)
        # print(targetjson)
        for i in access_list:
            if type(i[1])==str:
                if i[1]=="":
                    outlist.append("")
                else:
                    outlist.append(targetjson[i[1]])
                    
            elif type(i[1])==list:
                if i[0]=="user_mentions":
                    holderlist = []
                    for usermention in targetjson[i[1][0]][i[1][1]]:
                        holderlist.append(usermention["id"])
                    outlist.append(holderlist)
                else:
                    outlist.append(targetjson[i[1][0]][i[1][1]])
                    
                    
        return outlist
                
                
    threadeddict = {"rumour":[],"non-rumour":[],"unverified":[]}
    csvlist = [["tweetid","userid","user_display_name","user_screen_name","user_reported_location","user_profile_description","user_profile_url","follower_count","following_count","account_creation_date","account_language","tweet_language","tweet_text","tweet_time","tweet_client_name","in_reply_to_userid","in_reply_to_tweetid","quoted_tweet_tweetid","is_retweet","retweet_userid","retweet_tweetid","latitude","longitude","quote_count","reply_count","like_count","retweet_count","hashtags","urls","user_mentions","poll_choices"]]
    for filetarget in topicalname:
        topicalname = filetarget.replace("-all-rnr-threads","")
        nonrumourfiles = os.listdir(os.path.join(homedir,topicalname+"-all-rnr-threads","non-rumours"))
        rumourfiles = os.listdir(os.path.join(homedir,topicalname+"-all-rnr-threads","rumours"))
        indexes = convenient_dictionary[topicalname]
        rumourindex = indexes[0]
        nonrumourindex = indexes[1]
        unverifiedindex = indexes[2]
        reactionindex = indexes[3]
        for labeltype in [("rumours",rumourfiles),("non-rumours",nonrumourfiles)]:
            for threadidx in labeltype[1]:
                newthread = {"reactions":[]}
                if threadidx[0]==".":
                    continue # is a mac storage thingy.
                threadpath = os.path.join(homedir,topicalname+"-all-rnr-threads",labeltype[0],threadidx)
                annotation = os.path.join(threadpath,"annotation.json")
                structure = os.path.join(threadpath,"structure.json")
                source_tweets_dir = os.path.join(threadpath,"source-tweets")
                reaction_tweets_dir = os.path.join(threadpath,"reactions")
                unverified_flag = False
                nonrumour_flag = False
                rumour_flag = False
                for sourcetweet in os.listdir(source_tweets_dir):
                    if "." ==sourcetweet[0]:
                        continue
                    with open(os.path.join(source_tweets_dir,sourcetweet),"r",encoding="utf-8") as sourcetweetfile:
                        sourcetweet_json = json.load(sourcetweetfile)
                        outlist = pheme_accessor(access_list,sourcetweet_json)
                        rootname = outlist[0]
                        texts[outlist[0]] = outlist[12]
                    with open(annotation,"r",encoding="utf-8") as annotations_file:
                        annotation_json = json.load(annotations_file)
                        try:
                            z = annotation_json["misinformation"]
                            if z==1:
                                outlist.append(rumourindex)
                            else:
                                try: 
                                    z = annotation_json["true"]
                                    if z==0:
                                        outlist.append(unverifiedindex) # no true 
                                        unverified_flag = True
                                    else:
                                        outlist.append(nonrumourindex) # no true 
                                        nonrumour_flag = True
                                except KeyError:
                                    outlist.append(rumourindex) # no true, no misinformation
                                    rumour_flag = True
                        except KeyError:
                            try:
                                z = annotation_json["true"]
                                if z==1:
                                    outlist.append(nonrumourindex)
                                    nonrumour_flag = True
                                else:
                                    outlist.append(rumourindex)
                                    rumour_flag = True
                            except KeyError:
                                outlist.append(unverifiedindex) # doesn't have both true or misinformation
                                unverified_flag = True
                                
                    csvlist.append(outlist)
                    newthread["source"] = outlist[:-1]
                    newthread["topic"] = labeltype[0]
                for reactiontweet in os.listdir(reaction_tweets_dir):
                    if "."==reactiontweet[0]:
                        continue
                    with open(os.path.join(reaction_tweets_dir,reactiontweet),"r",encoding="utf-8") as reactiontweetfile:
                        reactiontweet_json = json.load(reactiontweetfile)
                        outlist = pheme_accessor(access_list,reactiontweet_json)
                        outlist.append(reactionindex)
                    csvlist.append(outlist)
                    newthread["reactions"].append(outlist[:-1])
                    newthread["root"] = str(rootname)
                if len(newthread["reactions"])==0: # no reactions...
                    continue
                if rumour_flag:
                    threadeddict["rumour"].append(newthread)
                    labelfile_txtlist.append("false"+":"+str(rootname))
                elif nonrumour_flag:
                    threadeddict["non-rumour"].append(newthread)
                    labelfile_txtlist.append("true"+":"+str(rootname))
                elif unverified_flag:
                    threadeddict["unverified"].append(newthread)
                    labelfile_txtlist.append("unverified"+":"+str(rootname))
    with open("transposed_label.txt","w", encoding ="utf-8") as threadfile:
        for item in labelfile_txtlist:
            threadfile.write(str(item)+"\n")
        
    with open("transposed_source_tweets.txt","w",encoding="utf-8") as textfile:
        for item in texts:
            textfile.write(str(item)+"\t"+texts[item].replace("\n"," ")+"\n")
    
    
    for silenced_label in ["rumour","non-rumour","unverified"]:
        for tree in threadeddict[silenced_label]:
            tweettimedict = {}
            banlist = []
            with open(os.path.join(dumpdir,tree["root"]+".txt"), "w", encoding="utf-8") as treefile:

                source_tweetid = tree["source"][0]
                source_userid = tree["source"][1]
                source_tweet_time = tree["source"][13]
                replyuserid = tree["source"][15]
                replytweetid  = tree["source"][16]
                treefile.write(str(["ROOT","ROOT","0.0"])+"->"+str([str(source_userid),str(source_tweetid),"0.0"])+"\n")
                source_datetime = datetime.strptime(tree["source"][13],'%a %b %d %H:%M:%S +0000 %Y')

                
                for reaction in tree["reactions"]:
                    selftweetid = reaction[0]
                    selfuserid = reaction[1]
                    selftweet_time = reaction[13]
                    tweettimedict[str(selftweetid)] = [selftweet_time,selfuserid]
                    
                    
                for reaction in tree["reactions"]:
                    
                    selftweetid = reaction[0]
                    selfuserid = reaction[1]
                    selftweet_time = reaction[13]
                    replyuserid = reaction[15]
                    replytweetid  = reaction[16]
                    # print(selftweetid,selfuserid,selftweet_time,replyuserid,replytweetid)
                    selfdatetime = datetime.strptime(selftweet_time,'%a %b %d %H:%M:%S +0000 %Y')
                    if replytweetid==None: # not responding to tweet... but related to event.
                        print("related but not in tree for root.")
                        print(reaction)
                        continue
                    # if not str(replytweetid) in tweettimedict and str(replytweetid)!=:
                        # print(replytweetid)
                        # print(tweettimedict.keys())
                        # banlist.append(replytweetid)
                        # banlist.append(selftweetid)
                        # continue
                    # if replytweetid in banlist:
                        # banlist.append(selftweetid)
                        # continue
                    
                    if not str(replytweetid) in tweettimedict and str(replytweetid)!=str(source_tweetid):
                        replytweetid = source_tweetid
                        continue                    
                        
                    
                    if replytweetid==source_tweetid:
                        # print("replied to source..")
                        treefile.write(str([source_userid, source_tweetid, "0.0"])+"->"+str([str(replyuserid),str(selftweetid),"0.0"])+"\n")
                    else:
                        replydatetime = datetime.strptime(tweettimedict[str(replytweetid)][0],'%a %b %d %H:%M:%S +0000 %Y')
                        firstdiff = source_datetime - replydatetime
                        seconddiff = replydatetime - selfdatetime
                        treefile.write(str([tweettimedict[str(replytweetid)][1], replytweetid, firstdiff.total_seconds()])+"->"+str([str(replyuserid),str(selftweetid),seconddiff.total_seconds()])+"\n")