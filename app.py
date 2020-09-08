# -*- coding: utf-8 -*-
from flask import Flask, session,render_template, request
import os
import pandas as pd
#app = MyFlask(__name__)
#app.config['STATIC_FOLDER'] = 'foo'
app = Flask(__name__)
app.secret_key = "tekitouni123"
def simplePass(digitNumber):
    import random
    hiraganaList =["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    listLength=len(hiraganaList)
    password=""
    for i in range(0,digitNumber):
        w=random.randint(0,listLength-1)
        password=password+hiraganaList[w]
    return password
@app.route('/')
def main():
    Dict={}
    df=pd.read_excel("quiz.xlsx")
    Dict["theme"]=[]
    for n in (list(set(df["theme"].tolist()))):
        if len(df[df["theme"]==n])>10:
            Dict["theme"].append(n)
    if "name" not in session:
        session["name"]=simplePass(5)
        session["age"]=15
    Dict["name"]=session["name"]
    Dict["age"]=session["age"]
    return render_template("HTML01_login_HTML.html",Dict=Dict)
@app.route('/trGet', methods=['GET'])
def transit_get():
    Dict={}
    import appTranstionPathwayGet
    if request.args.get("pathID"):
        print (request.args.get)
        if "name" not in session:
            random_state="OK"
            session['absURL']=request.url
            return render_template("HTML01_login_HTML.html")
        else:
            Dict, html=appTranstionPathwayGet.pathwayFromGet(request.args)
            return render_template(html,Dict=Dict)
    else:
        html="error.html"
        Dict["message1"]="エラーです"
        Dict["message2"]=[""]
        return render_template(html,Dict=Dict)
"""
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
"""
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    # 安全のため debug=False とする
    # 特に本番稼働するファイルでは debug=True としてはいけない!
    #app.run(debug=False)
    app.run(debug=True)



