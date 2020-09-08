
##################################################
# .//trGet?pathID=xxxx でページを遷移します。
# .//trGet?pathID=xxxx  pathID brings to a HTML page
#
#
#########################################################
from flask import  session
import pandas as pd
import random
def pathwayFromGet(request_args):
    Dict={}
    Dict["message1"]="不明なコードがみつかりました"
    Dict["message2"]=["The code is unknown","Please try another code"]
    NewDict={}
    html="error.html"
    ##################################
    #Navigation Part
    ##################################
    for i in request_args.keys():
        NewDict[i]=request_args[i]
    ##################################
    if NewDict["pathID"]=="login":
        html="HTML02_testPage.html"
        df=pd.read_excel("quiz.xlsx")
        ##何問目?
        Dict["page"]=int(NewDict["questions"])
        Dict["theme"]=NewDict["theme"]
        ##質問リスト作成
        if int(NewDict["questions"])==0:
            finddf=df[df["theme"]==NewDict["theme"]]
            questionList=finddf["INDEX"].tolist()
            random.shuffle(questionList)
            session["questionList"]=questionList[0:10]
            Dict["questionList"]=session["questionList"]
            Dict["note"]=""
            Dict["message1"]=""
            session["name"]=NewDict["UserNamae"]
            session["age"]=int(NewDict["CalendarAge"])
            session["correct"]=0
        else:
            Dict["questionList"]=session["questionList"]
            #ノート作成 全問のノート
            finddf=df[df["INDEX"]==Dict["questionList"][Dict["page"]-1]]
            Dict["note"] =(finddf["note"].values[0])
            ####答えあわせ
            if NewDict["answer"]==finddf["correct"].values[0]:
                session["correct"]=session["correct"]+1
                Dict["message1"]="◎正解:{}/10".format(session["correct"])
            else:
                Dict["message1"]="×誤り:{}/10".format(session["correct"])
        #10問で終わり
        if int(NewDict["questions"])>9:
            html="HTML03_results.html"
            Dict["message2"]=["総合点: {}点".format(int(session["correct"]/10*100)),"ホーム"]
        else:
            ##選択肢リスト
            indexNumber=session["questionList"][Dict["page"]]
            finddf=df[df["INDEX"]==indexNumber]
            session["answer"] =finddf["correct"].values[0]
            Dict["answerList"]=[finddf["correct"].values[0],finddf["wrong1"].values[0],finddf["wrong2"].values[0]]
            random.shuffle(Dict["answerList"])
            ###質問
            Dict["q"]=finddf["q"].values[0]
            Dict["UserNamae"]=NewDict["UserNamae"]
            Dict["CalendarAge"]=NewDict["CalendarAge"]
    else:
        Dict["message1"]="エラー"
        Dict["message2"]=["このページは存在しません","もどる"]
        html="error.html"
    #print (NewDict)
    #print (html)
    return Dict, html