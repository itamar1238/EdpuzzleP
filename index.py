from flask import Flask, request, render_template, url_for, redirect

import json, requests

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def my_form_post():

    global pclases, cookies_dict, length_clases, clases, status

    token = request.form['text']

    cookies_dict = {
        "token": token
    }

    response2 = requests.get("https://edpuzzle.com/api/v3/classrooms/active", cookies=cookies_dict)

    status = response2.status_code

    if status == 200:

        clases = json.loads(response2.content)

        pclases = []

        length_clases = len(clases)

        for i in range(len(clases)):

            pclases.append(clases[i]['_id'])

        return redirect("/clases")
    
    else: 

        return redirect("/")

@app.route('/clases')
def home2():

    if status == 200:

        return render_template("home2.html", clases=clases, length_clases=length_clases)
    
    else:

        return redirect("/")

@app.route("/clases/<int:id>")
def my_other_form_post(id):

    global examen, length2_examenes

    numClassId = id

    classId = str(pclases[int(numClassId)-1])

    url = "https://edpuzzle.com/api/v3/assignments/classrooms/" + classId + "/students?needle="

    response = requests.get(url, cookies=cookies_dict)

    examen = json.loads(response.content)
    
    length2_examenes = len(examen['medias'])
    
    return redirect("/examenes")

@app.route('/examenes')
def home3():

    if status == 200:

        return render_template("home3.html", length2_examenes=length2_examenes, examen=examen)
    
    else:

        return redirect("/")

@app.route('/examenes/<int:id2>')
def my_other_other_form(id2):
    
    num = id2

    num = int(num) - 1

    length3_examenes = len(examen['medias'][num]['questions'])

    return render_template("home4.html", num=num, examen=examen, length3_examenes=length3_examenes, id2=id2)

status = None

if __name__ == "__main__":

    app.run(threaded=True)