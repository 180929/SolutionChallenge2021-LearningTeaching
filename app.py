# -*- coding: utf-8 -*-
import shutil
from flask import Flask, render_template, request, redirect, url_for, jsonify,session,send_from_directory
from parameters import firebaseConfig
import pyrebase
from firebase import firebase as fb
import requests
import os


app = Flask(__name__)
app.config['SECRET_KEY']='Billy'

def findUser(db,mail):
    user = None
    users = db.child("Students").get()
    for user1 in users.each():
        if user1.val()['EMAIL'] == mail:
            user = user1
            break
    return user

def verification(Email):
    Inscription=True
    firebase = pyrebase.initialize_app(firebaseConfig)
    # firebase = firebase.FirebaseApplication("https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app/", None)
    # result = firebase.post('/Students/',data2)
    db = firebase.database()
    user = findUser(db, Email)
    if user:
        Inscription=False
    return Inscription

def verificationPassword(Email, Password):
    Inscription = False
    firebaseConfig = {
        'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
        'authDomain': "pythonprojectfpms.firebaseapp.com",
        'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
        'projectId': "pythonprojectfpms",
        'storageBucket': "pythonprojectfpms.appspot.com",
        'messagingSenderId': "436048843972",
        'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
        'measurementId': "G-S7DXXKCN7R"
    }
    from flask import Flask, render_template, request, session, redirect, url_for
    import pyrebase
    from firebase import firebase
    from passlib.hash import sha256_crypt
    firebase = pyrebase.initialize_app(firebaseConfig)
    # firebase = firebase.FirebaseApplication("https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app/", None)
    # result = firebase.post('/Students/',data2)
    db = firebase.database()
    users = db.child("Students").get()
    for user1 in users.each():
        if user1.val()['EMAIL'] == Email:
            if sha256_crypt.verify(Password, user1.val()['Password']) == True:
                Inscription = True
                break;
            else:
                Inscription = False
                break;

        else:
            Inscription = False

    return Inscription


class DATACLASS:
    def __init__(self):
        self.data={}
        self.typeD=""
        self.table=""

    def AddType(self,type):
        self.typeD=type

    def AddType(self,table):
        self.table=table
    def Adddata(self,name,firstname,password,email,study):
        self.data={
        "EMAIL":email,
        "Password": password,
        "Firstname": firstname,
        "Study": study,
        "Name": name,
        }
    def Adcourse(self,title, theme, region, description, prereq, langue, email):
        self.data={
        "Title":title,
        "Subject": theme,
        "Subsubject": region,
        "Description": description,
        "Prerequis": prereq,
        "Language": langue,
        "Autor" : email,
        "Pdf":[""],
        "Videos":[""],
        }
    def Adfollowedcourse(self,clef):
        self.data={
        "KeyCourse":clef,
        }
    def AdDiscussion(self,course_title,subject,message):
        self.data={
            "course_title":course_title,
            "subject":subject,
            "message":message,
        }
        #rajouter un champ pour le mail de l'utilisateur
        #rajouter un champ pour gérer les différentes réponses à la discussion (liste d'objets --> objet = {emailUtilisateur : ... , réponse :... , date : ...}
        #rajouter un champ pour la data à laquelle la discussion a été envoyée
        #rajouter un id ?
    def GetDATA(self):
        return self.data,self.typeD,self.table


def getDiscussions(db):
    discussions = db.child("Discussions").get()
    headings = ["Discussion", ]
    keys=[]
    data=[]
    for discussion in discussions.each():
        keys.append("/discussion/"+str(discussion.key()))
        data.append((discussion.val()["course_title"]+"-"+discussion.val()["subject"],))
    return headings, data, keys

def findDiscussion(db,discussion_id):
    discussion=None
    check=False
    discussions = db.child("Discussions").get()
    for discussion in discussions.each():
        if discussion.key() == discussion_id:
            check=True
            discussion=discussion
            break
    return check,discussion




def getFileName(filePath):
    fileName = ""
    pos = None
    for i in range(len(filePath) - 1, 0, -1):
        if filePath[i] == "/":
            pos = i + 1
            break

    for i in range(pos, len(filePath)):
        fileName += filePath[i]
    fileName_v2 = ""
    for i in range(len(fileName)):
        if i == len(fileName) - 4:
            break
        fileName_v2 += fileName[i]

    return (fileName_v2)


def uploadFile(storage,course,filename,type,file):
    path="Authors/"+course["Autor"]+"/Languages/"+course["Language"]+"/Courses/"+course["Title"]+"/files/"+type+"/"
    storage.child(path+filename).put(file)

    return path+filename

def findCourse(db,course_id):
    c=None
    courses = db.child("Courses").get()
    for course in courses.each():

        if course.key() == course_id:

            c=course
            break

    return c



def checkAuthor(db,session,course_id):
    check=False
    course=findCourse(db,course_id)
    if course.val()["Autor"]==session["mail"]:
        check=True
    return check


def checkFollowedCourses(db, session, course_id):
    check = False
    user=findUser(db,session["mail"])
    followedCourses = db.child("Students").child(user.key()).child("listFollowedCourses").get()
    for course in followedCourses.each():
        if course.val()["KeyCourse"] == course_id:
            check = True
            break

    return check





@app.route('/sign_out')
def sign_out():
    if "mail" in session:
        session.pop('mail')
    return redirect(url_for("connexion"))

@app.route('/home')
def home():
    from flask import Flask, render_template, request, session, redirect, url_for
    if "mail" in session:
        print("Mail : "+session["mail"])
        print("hello")
        return  render_template('home.html')
    else:
        return redirect(url_for("connexion"))

@app.route('/all_courses')
def all_courses():
    from flask import Flask, render_template, request, session, redirect, url_for
    if "mail" in session:
        import pyrebase
        from firebase import firebase
        firebaseConfig = {
            'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
            'authDomain': "pythonprojectfpms.firebaseapp.com",
            'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
            'projectId': "pythonprojectfpms",
            'storageBucket': "pythonprojectfpms.appspot.com",
            'messagingSenderId': "436048843972",
            'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
            'measurementId': "G-S7DXXKCN7R"
        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        courses = db.child("Courses").get()
        mycourses = []

        students = db.child("Students").get()
        stud = []
        sub = []
        for mycourse in courses.each():
            mycourses.append(mycourse)
            if mycourse.val()['Subject'].split()[0] != "Tourism,":
                sub.append(mycourse.val()['Subject'].split()[0])
            else:
                sub.append("Tourism")
            print(mycourse.val()['Subject'].split()[0])
            for etud in students.each():
                if mycourse.val()["Autor"] == etud.val()["EMAIL"]:
                    stud.append(etud)
        #courses = db.child("Students").get()
        vari = zip(mycourses, stud, sub)

        themes = db.child("Topics").get()

        return  render_template('all_courses.html', cours=vari, topics=themes)
    else:
        return redirect(url_for("connexion"))

@app.route('/research', methods=["get", "post"])
def research():
    from flask import Flask, render_template, request, session, redirect, url_for
    if request.method == 'POST':
        k = request.form['keyword'].lower()
        if "mail" in session:
            import pyrebase
            from firebase import firebase
            firebaseConfig = {
                'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
                'authDomain': "pythonprojectfpms.firebaseapp.com",
                'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
                'projectId': "pythonprojectfpms",
                'storageBucket': "pythonprojectfpms.appspot.com",
                'messagingSenderId': "436048843972",
                'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
                'measurementId': "G-S7DXXKCN7R"
            }
            firebase = pyrebase.initialize_app(firebaseConfig)
            db = firebase.database()
            courses = db.child("Courses").get()
            mycourses = []
            students = db.child("Students").get()
            stud = []
            sub = []
            for mycourse in courses.each():
                if k in mycourse.val()["Title"].lower() or k in mycourse.val()["Description"].lower() or k in mycourse.val()["Subject"].lower() or k in mycourse.val()["Subsubject"].lower():
                    mycourses.append(mycourse)
                    if mycourse.val()['Subject'].split()[0] != "Tourism,":
                        sub.append(mycourse.val()['Subject'].split()[0])
                    else:
                        sub.append("Tourism")
                    for etud in students.each():
                        if mycourse.val()["Autor"] == etud.val()["EMAIL"]:
                            stud.append(etud)
            #courses = db.child("Students").get()
            vari = zip(mycourses, stud, sub)
            themes = db.child("Topics").get()
            return  render_template('all_courses.html', cours=vari, topics=themes)
        else:
            return redirect(url_for("connexion"))


@app.route('/research2', methods=["get", "post"])
def research2():
    from flask import Flask, render_template, request, session, redirect, url_for
    if request.method == 'POST':
        k = request.form['keyword'].lower()
        subj = request.form['theme']
        subsub = request.form['region']
        if "mail" in session:
            import pyrebase
            from firebase import firebase
            firebaseConfig = {
                'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
                'authDomain': "pythonprojectfpms.firebaseapp.com",
                'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
                'projectId': "pythonprojectfpms",
                'storageBucket': "pythonprojectfpms.appspot.com",
                'messagingSenderId': "436048843972",
                'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
                'measurementId': "G-S7DXXKCN7R"
            }
            firebase = pyrebase.initialize_app(firebaseConfig)
            db = firebase.database()
            courses = db.child("Courses").get()
            mycourses = []
            students = db.child("Students").get()
            stud = []
            sub = []
            for mycourse in courses.each():
                if k in mycourse.val()["Title"].lower() or k in mycourse.val()["Description"].lower() or k in mycourse.val()["Subject"].lower() or k in mycourse.val()["Subsubject"].lower():
                    if (mycourse.val()["Subject"] == subj and mycourse.val()["Subsubject"] == subsub) or (mycourse.val()["Subject"] == subj and subsub == "...") or subj == "...":
                        mycourses.append(mycourse)
                        if mycourse.val()['Subject'].split()[0] != "Tourism,":
                            sub.append(mycourse.val()['Subject'].split()[0])
                        else:
                            sub.append("Tourism")
                        for etud in students.each():
                            if mycourse.val()["Autor"] == etud.val()["EMAIL"]:
                                stud.append(etud)
            #courses = db.child("Students").get()
            vari = zip(mycourses, stud, sub)
            themes = db.child("Topics").get()
            return  render_template('all_courses.html', cours=vari, topics=themes)
        else:
            return redirect(url_for("connexion"))



@app.route('/delete_course', methods=["get","post"])
def delete_course():
    from flask import Flask, render_template, request, session, redirect, url_for
    if request.method == 'POST':
        if "mail" in session:
            clef = request.form['key']
            print(clef)


            import pyrebase
            from firebase import firebase
            firebaseConfig = {
                'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
                'authDomain': "pythonprojectfpms.firebaseapp.com",
                'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
                'projectId': "pythonprojectfpms",
                'storageBucket': "pythonprojectfpms.appspot.com",
                'messagingSenderId': "436048843972",
                'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
                'measurementId': "G-S7DXXKCN7R"
            }
            firebase = pyrebase.initialize_app(firebaseConfig)
            db = firebase.database()
            #db.child("Courses").child(clef).delete()
            print(db.child("Courses").child(clef).remove())




            return  redirect(url_for("teach"))
        else:
            return redirect(url_for("connexion"))



@app.route('/details', methods=["get","post"])
def details():
    from flask import Flask, render_template, request, session, redirect, url_for
    if request.method == 'POST':
        if "mail" in session:
            import ast
            course = request.form['x']
            clef = request.form['key']
            print(course)
            print(clef)
            course = ast.literal_eval(course) 


            import pyrebase
            from firebase import firebase
            firebaseConfig = {
                'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
                'authDomain': "pythonprojectfpms.firebaseapp.com",
                'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
                'projectId': "pythonprojectfpms",
                'storageBucket': "pythonprojectfpms.appspot.com",
                'messagingSenderId': "436048843972",
                'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
                'measurementId': "G-S7DXXKCN7R"
            }
            firebase = pyrebase.initialize_app(firebaseConfig)
            db = firebase.database()
            students = db.child("Students").get()
            liste = []
            print(students)
            for i in students.each():
                if i.val()['EMAIL'] == session["mail"]:
                    if 'listFollowedCourses' in i.val():
                        liste = i.val()['listFollowedCourses']
                if i.val()['EMAIL'] == course["Autor"]:
                    stud = i.val()

            status = "Follow" #valeur qu'on affichera sur le bouton
            if len(liste) > 0:
                for c, v in liste.items():
                    #print(clef, v['KeyCourse'])
                    if v['KeyCourse'] == clef:
                        status = "Unfollow"
            #################### PARTIE D'OLI ###############################

            firebase = pyrebase.initialize_app(firebaseConfig)
            storage = firebase.storage()
            #key_db = course_d.key()

            #course = course_d.val()
            if "Pdf" and "Videos" not in course:
                db.child("Courses").child(clef).update({"Pdf": [""], "Videos": [""]})
            course = db.child("Courses").child(clef).get().val()
            pathsPDF = course["Pdf"][:]
            pathsVideos = course["Videos"][:]

            if pathsPDF[0] == "":
                del pathsPDF[0]
            if pathsVideos[0] == "":
                del pathsVideos[0]
            # linksPDF = []
            fileNamesPdf = []

            for path in pathsPDF:
                # link = constructLink(storage, path, token=session["idToken"])
                # linksPDF.append(link)

                fileNamesPdf.append(getFileName(path))

            # linksVideos = []
            fileNamesVideos = []

            for path in pathsVideos:
                # linksVideos.append(constructLink(storage, path,token=session["idToken"]))
                fileNamesVideos.append(getFileName(path))

            author=False
            if session['mail']==stud['EMAIL']:
                author=True

            return  render_template('details.html', cours=course, stud=stud, key=clef, status=status,ListPdf=fileNamesPdf,ListVideos=fileNamesVideos,author=author)
        else:
            return redirect(url_for("connexion"))

@app.route('/details2', methods=["get","post"])
def details2():
    from flask import Flask, render_template, request, session, redirect, url_for
    if request.method == 'POST':
        if "mail" in session:
            if request.form['status'] == "Follow":
                import pyrebase
                from firebase import firebase
                firebaseConfig = {
                    'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
                    'authDomain': "pythonprojectfpms.firebaseapp.com",
                    'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
                    'projectId': "pythonprojectfpms",
                    'storageBucket': "pythonprojectfpms.appspot.com",
                    'messagingSenderId': "436048843972",
                    'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
                    'measurementId': "G-S7DXXKCN7R"
                }
                firebase = pyrebase.initialize_app(firebaseConfig)
                db = firebase.database()
                students = db.child("Students").get()
                for i in students.each():
                    if i.val()["EMAIL"] == session['mail']:
                        clefEtud = i.key()
                        stud = i.val()
                        if 'listFollowedCourses' in i.val():
                            liste = i.val()['listFollowedCourses']


                import ast
                clef = request.form['key']
                course = request.form['cours']
                #course = ast.literal_eval(course)
                data = DATACLASS()
                data.Adfollowedcourse(clef)
                data2, type, table = data.GetDATA()
                from firebase import firebase
                firebase = firebase.FirebaseApplication(
                    "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app/", None)
                result = firebase.post('/Students/'+clefEtud+'/listFollowedCourses', data2)
                config = {
                    "apiKey": "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
                    "authDomain": "pythonprojectfpms.firebaseapp.com",
                    "databaseURL": "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
                    "projectId": "pythonprojectfpms",
                    "storageBucket": "pythonprojectfpms.appspot.com",
                    "messagingSenderId": "436048843972",
                    "appId": "1:436048843972:web:f67ac5f04b5ee26e5b2591",
                    "measurementId": "G-S7DXXKCN7R",

                }
                
                course = db.child("Courses").child(clef).get()
                students = db.child("Students").get()
                for i in students.each():
                    if i.val()["EMAIL"] == course.val()["Autor"]:
                        stud = i
                course = course.val()
                        
                #################### PARTIE D'OLI ###############################

                firebase = pyrebase.initialize_app(firebaseConfig)
                storage = firebase.storage()
                #key_db = course_d.key()
    
                #course = course_d.val()
                
                if "Pdf" and "Videos" not in course:
                    db.child("Courses").child(clef).update({"Pdf": [""], "Videos": [""]})
                course = db.child("Courses").child(clef).get().val()
                pathsPDF = course["Pdf"][:]
                pathsVideos = course["Videos"][:]
    
                if pathsPDF[0] == "":
                    del pathsPDF[0]
                if pathsVideos[0] == "":
                    del pathsVideos[0]
                # linksPDF = []
                fileNamesPdf = []
    
                for path in pathsPDF:
                    # link = constructLink(storage, path, token=session["idToken"])
                    # linksPDF.append(link)
    
                    fileNamesPdf.append(getFileName(path))
    
                # linksVideos = []
                fileNamesVideos = []
    
                for path in pathsVideos:
                    # linksVideos.append(constructLink(storage, path,token=session["idToken"]))
                    fileNamesVideos.append(getFileName(path))
    
                author=False
                if session['mail']==stud.val()['EMAIL']:
                    author=True
                course = db.child("Courses").child(clef).get()
                students = db.child("Students").get()
                for i in students.each():
                    if i.val()["EMAIL"] == course.val()["Autor"]:
                        stud = i
    
                return  render_template('details.html', cours=course.val(), stud=stud.val(), key=clef, status="Unfollow",ListPdf=fileNamesPdf,ListVideos=fileNamesVideos,author=author)
            
            else:
                import pyrebase
                from firebase import firebase
                firebaseConfig = {
                    'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
                    'authDomain': "pythonprojectfpms.firebaseapp.com",
                    'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
                    'projectId': "pythonprojectfpms",
                    'storageBucket': "pythonprojectfpms.appspot.com",
                    'messagingSenderId': "436048843972",
                    'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
                    'measurementId': "G-S7DXXKCN7R"
                }
                firebase = pyrebase.initialize_app(firebaseConfig)
                db = firebase.database()
                students = db.child("Students").get()
                for i in students.each():
                    if i.val()["EMAIL"] == session['mail']:
                        clefEtud = i.key()
                        stud = i.val()
                        

                import ast
                clef = request.form['key']
                course = request.form['cours']
                #course = ast.literal_eval(course)

                for i in students.each():
                    if i.val()['EMAIL'] == session["mail"]:
                        print(i.val()['listFollowedCourses'])
                        for c, v in i.val()['listFollowedCourses'].items():
                            print(v['KeyCourse'])
                            if v['KeyCourse'] == clef:
                                clefetud = i.key()
                                temp = db.child("Students").child(i.key()).get().val()
                                liste = temp['listFollowedCourses']


                for c, v in liste.items():
                    if v['KeyCourse'] == clef:
                        clefsup = c
                del liste[clefsup]
                temp['listFollowedCourses'] = liste
                db.child("Students").child(clefetud).update(temp)
                
                
                course = db.child("Courses").child(clef).get()
                students = db.child("Students").get()
                for i in students.each():
                    if i.val()["EMAIL"] == course.val()["Autor"]:
                        stud = i
                course = course.val()
                
                #################### PARTIE D'OLI ###############################

                firebase = pyrebase.initialize_app(firebaseConfig)
                storage = firebase.storage()
                #key_db = course_d.key()
    
                #course = course_d.val()
                if "Pdf" and "Videos" not in course:
                    db.child("Courses").child(clef).update({"Pdf": [""], "Videos": [""]})
                course = db.child("Courses").child(clef).get().val()
                pathsPDF = course["Pdf"][:]
                pathsVideos = course["Videos"][:]
    
                if pathsPDF[0] == "":
                    del pathsPDF[0]
                if pathsVideos[0] == "":
                    del pathsVideos[0]
                # linksPDF = []
                fileNamesPdf = []
    
                for path in pathsPDF:
                    # link = constructLink(storage, path, token=session["idToken"])
                    # linksPDF.append(link)
    
                    fileNamesPdf.append(getFileName(path))
    
                # linksVideos = []
                fileNamesVideos = []
    
                for path in pathsVideos:
                    # linksVideos.append(constructLink(storage, path,token=session["idToken"]))
                    fileNamesVideos.append(getFileName(path))
    
                author=False
                if session['mail']==stud.val()['EMAIL']:
                    author=True
                course = db.child("Courses").child(clef).get()
                students = db.child("Students").get()
                for i in students.each():
                    if i.val()["EMAIL"] == course.val()["Autor"]:
                        stud = i

                return  render_template('details.html', cours=course.val(), stud=stud.val(), key=clef, status="Follow",ListPdf=fileNamesPdf,ListVideos=fileNamesVideos,author=author)
        else:
            return redirect(url_for("connexion"))


@app.route('/teached_courses')
def teach():
    from flask import Flask, render_template, request, session, redirect, url_for
    if "mail" in session:
        import pyrebase
        from firebase import firebase
        firebaseConfig = {
            'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
            'authDomain': "pythonprojectfpms.firebaseapp.com",
            'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
            'projectId': "pythonprojectfpms",
            'storageBucket': "pythonprojectfpms.appspot.com",
            'messagingSenderId': "436048843972",
            'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
            'measurementId': "G-S7DXXKCN7R"
        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        courses = db.child("Courses").get()
        mycourses = []
        sub = []
        for mycourse in courses.each():
            if mycourse.val()['Autor'] == session["mail"]:
                mycourses.append(mycourse)
                if mycourse.val()['Subject'].split()[0] != "Tourism,":
                    sub.append(mycourse.val()['Subject'].split()[0])
                else:
                    sub.append("Tourism")
        vari = zip(mycourses, sub)
        return  render_template('teached.html', cours=vari)
    else:
        return redirect(url_for("connexion"))

@app.route('/followed_courses')
def followed_courses():
    import ast
    from flask import Flask, render_template, request, session, redirect, url_for
    if "mail" in session:
        import pyrebase
        from firebase import firebase
        firebaseConfig = {
            'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
            'authDomain': "pythonprojectfpms.firebaseapp.com",
            'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
            'projectId': "pythonprojectfpms",
            'storageBucket': "pythonprojectfpms.appspot.com",
            'messagingSenderId': "436048843972",
            'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
            'measurementId': "G-S7DXXKCN7R"
        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        students = db.child("Students").get()
        liste = []
        print(students)
        for i in students.each():
            if i.val()['EMAIL'] == session["mail"]:
                if 'listFollowedCourses' in i.val():
                    liste = i.val()['listFollowedCourses']

        courses = db.child("Courses").get()
        etud = db.child("Students").get()
        mycourses = []
        listekeys = []
        sub = []
        stud = []
        notif = ""
        if len(liste) > 0:
            for i in liste.items():
                listekeys.append(i[1]["KeyCourse"])

            for mycourse in courses.each():
                if mycourse.key() in listekeys:
                    mycourses.append(mycourse)
                    if mycourse.val()['Subject'].split()[0] != "Tourism,":
                        sub.append(mycourse.val()['Subject'].split()[0])
                    else:
                        sub.append("Tourism")
                    for etud in students.each():
                        if mycourse.val()["Autor"] == etud.val()["EMAIL"]:
                            stud.append(etud)
            mycourses=zip(mycourses, stud, sub)
        else:
            mycourses = "null"
            notif = "You're not following any course at the moment"


        return  render_template('followed.html', cours=mycourses, notif=notif)
    else:
        return redirect(url_for("connexion"))

@app.route('/profile')
def profile():
    if "mail" in session:

        return render_template('profile.html')
    else:
        return redirect(url_for("connexion"))

@app.route('/Confirmation', methods=["get","post"])
def Code():
    from flask import Flask, render_template, request, session, redirect, url_for
    import pyrebase
    from firebase import firebase
    if request.method == 'POST':
        Code = request.form["Code"]
        if Code==session["Code"]:
            Lastname = session["Lastname"]
            Surname = session["Surname"]
            Etude = session["Etude"]
            Email = session["Email"]
            password = session["password"]
            data = DATACLASS()
            data.Adddata(Lastname, Surname, password, Email, Etude)
            data2, type, table = data.GetDATA()
            print(data2)
            from firebase import firebase
            firebase = firebase.FirebaseApplication(
                "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app/", None)
            result = firebase.post('/Students/', data2)
            config = {
                "apiKey": "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
                "authDomain": "pythonprojectfpms.firebaseapp.com",
                "databaseURL": "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
                "projectId": "pythonprojectfpms",
                "storageBucket": "pythonprojectfpms.appspot.com",
                "messagingSenderId": "436048843972",
                "appId": "1:436048843972:web:f67ac5f04b5ee26e5b2591",
                "measurementId": "G-S7DXXKCN7R",

            }
            firebase = pyrebase.initialize_app(config)
            auth = firebase.auth()
            user = auth.create_user_with_email_and_password(Email, password)
            return  render_template('login.html',notification="You are registered")
        else:
            return render_template('register.html', notification="Your code is not correct")
    else:
        return render_template('CODE.html')

@app.route('/form_course', methods=["get","post"])
def form_course():
    from flask import Flask, render_template, request, session, redirect, url_for
    import pyrebase
    from firebase import firebase
    import pyrebase
    from firebase import firebase
    firebaseConfig = {
        'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
        'authDomain': "pythonprojectfpms.firebaseapp.com",
        'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
        'projectId': "pythonprojectfpms",
        'storageBucket': "pythonprojectfpms.appspot.com",
        'messagingSenderId': "436048843972",
        'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
        'measurementId': "G-S7DXXKCN7R"
    }
    if 'mail' in session:
        if request.method == 'POST':

            Title= request.form["title"]
            Subject = request.form["theme"]
            Subsubject = request.form["region"]
            Description = request.form["description"]
            Prerequis = request.form["prerequis"]
            Language = request.form["langue"]
            print("vérif champs")

            #Inscription=verification(Email)

            if not Title:
                return render_template("form_course.html", notification="Veuillez remplir tous les champs")
            elif not Subject:
                return render_template("form_course.html", notification="Veuillez remplir tous les champs")
            elif not Description:
                return render_template("form_course.html", notification="Veuillez remplir tous les champs")
            elif not Prerequis:
                return render_template("form_course.html", notification="Veuillez remplir tous les champs")
            elif not Language:
                return render_template("form_course.html", notification="Veuillez remplir tous les champs")
            
            else:
                data = DATACLASS()
                data.Adcourse(Title, Subject, Subsubject, Description, Prerequis, Language, session["mail"])
                data2, type, table = data.GetDATA()
                from firebase import firebase
                firebase = firebase.FirebaseApplication(
                    "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app/", None)
                result = firebase.post('/Courses/', data2)
                config = {
                    "apiKey": "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
                    "authDomain": "pythonprojectfpms.firebaseapp.com",
                    "databaseURL": "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
                    "projectId": "pythonprojectfpms",
                    "storageBucket": "pythonprojectfpms.appspot.com",
                    "messagingSenderId": "436048843972",
                    "appId": "1:436048843972:web:f67ac5f04b5ee26e5b2591",
                    "measurementId": "G-S7DXXKCN7R",

                }
                #firebase = pyrebase.initialize_app(config)
                #auth = firebase.auth()
                #user = auth.create_user_with_email_and_password(Email, password)
                return render_template("home.html", notification="Course created !")
        elif request.method == 'GET':
            firebase = pyrebase.initialize_app(firebaseConfig)
            db = firebase.database()
            languages = db.child("Languages").get()
            themes = db.child("Topics").get()
            return render_template("form_course.html", langues=languages, topics=themes)
        else:
            print("lol ?")
    else:
        return redirect(url_for("connexion"))

@app.route('/',methods=["get","post"])
def initial():
     return  render_template('login.html')

@app.route('/connexion', methods=["get","post"])
def connexion():
    from flask import Flask, render_template, request, session, redirect, url_for
    import pyrebase
    from firebase import firebase
    config = {
        "apiKey": "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
        "authDomain": "pythonprojectfpms.firebaseapp.com",
        "databaseURL": "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
        "projectId": "pythonprojectfpms",
        "storageBucket": "pythonprojectfpms.appspot.com",
        "messagingSenderId": "436048843972",
        "appId": "1:436048843972:web:f67ac5f04b5ee26e5b2591",
        "measurementId": "G-S7DXXKCN7R",

    }
    firebase=pyrebase.initialize_app(config)
    auth=firebase.auth()
    if request.method == 'POST':
        Email=request.form["Email"]
        PassWord=request.form["PassWord"]
        EmailNotexist = verification(Email)
        if  EmailNotexist==False:
            Login=verificationPassword(Email,PassWord)
            if Login==True:

                session["mail"]=Email
                return render_template("home.html")
            else:
                return render_template("login.html", notification="Password or Email incorrect")
        else:
            return render_template("login.html", notification="Password or Email incorrect")

    else:
        return render_template("login.html")

@app.route('/inscription', methods=["get","post"])
def inscription():
    from flask import Flask, render_template, request, session, redirect, url_for
    import pyrebase
    from firebase import firebase
    if request.method == 'POST':

        Lastname= request.form["Lastname"]
        Surname = request.form["Surname"]
        Birthdate = request.form["BirthDate"]
        Etude = request.form["BillingAdress"]
        Email = request.form["Email"]
        password = request.form["PassWord"]


        Inscription=verification(Email)

        if not Surname:
            return render_template("register.html", notification="Veuillez remplir tous les champs")
        elif not Lastname:
            return render_template("register.html", notification="Veuillez remplir tous les champs")
        elif not Birthdate:
            return render_template("register.html", notification="Veuillez remplir tous les champs")
        elif not Etude:
            return render_template("register.html", notification="Veuillez remplir tous les champs")
        elif not Email:
            return render_template("register.html", notification="Veuillez remplir tous les champs")
        elif not password:
            return render_template("register.html", notification="Veuillez remplir tous les champs")
        elif Inscription==False:
            return render_template("register.html", notification="Cette adresse email existe déjà")

        else:

            import random
            import smtplib
            from email.mime.text import MIMEText
            from passlib.hash import sha256_crypt
            sender_email = str("learningteachingbyfpms@gmail.com")

            smtp_ssl_host = "smtp.gmail.com"  # smtp.mail.yahoo.com
            recever=str(request.form["Email"])
            password = str("OlivierM123")
            secret = random.randint(1000, 9999)
            String_SEcret = str(secret)
            msg = "your code to connect is: " + String_SEcret
            server = smtplib.SMTP(smtp_ssl_host, 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recever, "your code to connect is    " + String_SEcret)
            session["Code"]=String_SEcret
            session["Email"]=Email
            session["password"]=sha256_crypt.encrypt(request.form["PassWord"])
            session["Lastname"]=Lastname
            session["Surname"]=Surname
            session["Etude"]=Etude

            return render_template("CODE.html", notification="Verify your email to create your account!")

    elif request.method == 'GET':
        return render_template("register.html")
    else:
        print("lol ?")





@app.route('/forum',methods=["GET","POST"])
def forum():

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    headings,data,keys=getDiscussions(db)
    return  render_template('forum.html',headings=headings,zipList=zip(keys,data))




@app.route('/form_discussion',methods=["GET","POST"])
def form_discussion():

    if request.method == 'POST':

        Title = request.form["title"]
        Subject = request.form["subject"]
        Message = request.form["message"]


        # Inscription=verification(Email)

        if not Title:
            return render_template("form_discussion.html", notification="Veuillez remplir tous les champs")
        elif not Subject:
            return render_template("form_discussion.html", notification="Veuillez remplir tous les champs")
        elif not Message:
            return render_template("form_discussion.html", notification="Veuillez remplir tous les champs")


        else:

            data = DATACLASS()
            data.AdDiscussion(Title, Subject, Message)
            data2, type, table = data.GetDATA()
            print(data2)
            firebase = fb.FirebaseApplication(
                "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app/", None)
            result = firebase.post('/Discussions/', data2)

            return redirect(url_for("forum"))

    elif request.method == 'GET':
        return render_template("form_discussion.html")

    else:
        print("lol ?")


@app.route('/discussion/<discussion_id>',methods=["GET"])
def discussion(discussion_id):

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    check,discussion=findDiscussion(db,discussion_id)
    if check:
        return render_template("discussion.html",discussion_id=discussion_id,course_title=discussion.val()["course_title"],subject=discussion.val()["subject"],message=discussion.val()["message"])





@app.route('/double_liste',methods=["GET","POST"])
def double_liste(): #verif de la session?
    from flask import Flask, render_template, request, session, redirect, url_for
    import pyrebase
    from firebase import firebase
    if request.method == 'POST':
    
        print("Enter file")
        
        resultat= "<label>Sub-subject</label> <br><select class='form-control' id='region'  name='region'> <option>...</option>"
        resultat1= "" 
        resultat2="</select>"
        
        region = request.values['a']
        
        firebaseConfig = {
            'apiKey': "AIzaSyCaUjayB4miLFeDcOfSgsYpjiT4XODaSkI",
            'authDomain': "pythonprojectfpms.firebaseapp.com",
            'databaseURL': "https://pythonprojectfpms-default-rtdb.europe-west1.firebasedatabase.app",
            'projectId': "pythonprojectfpms",
            'storageBucket': "pythonprojectfpms.appspot.com",
            'messagingSenderId': "436048843972",
            'appId': "1:436048843972:web:f67ac5f04b5ee26e5b2591",
            'measurementId': "G-S7DXXKCN7R"
        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        topics = db.child("Topics").get()

        
        
        for topic in topics.each():
            #print(topic)
            #print(topic.val()['id'])
            if topic.val()['name'] == region:
                listtopics = topic.val()['sous-themes']
        
        print(listtopics)
 
        for i in listtopics:
            if i != None:
                resultat1 += ("<option value=\"" + i['namesub'] + "\">" + i['namesub'] + "</option>")

        return jsonify(result=resultat + resultat1 + resultat2)





@app.route('/form_upload/<course_id>',methods=["POST","GET"])

def form_upload(course_id):

    if 'mail' in session:

        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        stud = findUser(db,session['mail'])
        course_d = findCourse(db, course_id)

        if course_d:

            if checkAuthor(db, session, course_id):



                if request.method == 'POST':

                    filename = request.form["name"]
                    type = request.form["type"]
                    file = request.files["upFile"]

                    # Inscription=verification(Email)
                    print(file)
                    if not filename:
                        return render_template("form_upload.html", course_id=course_id,
                                               notification="Veuillez remplir tous les champs")
                    elif not type:
                        return render_template("form_upload.html", course_id=course_id,
                                               notification="Veuillez remplir tous les champs")
                    elif not file:
                        return render_template("form_upload.html", course_id=course_id,
                                               notification="Veuillez remplir tous les champs")

                    else:
                        storage = firebase.storage()
                        course_d = findCourse(db, course_id)
                        course = course_d.val()

                        if type == "pdf":
                            filepath = uploadFile(storage, course, filename + ".pdf", type, file)
                            newList = course["Pdf"][:]
                            newList.append(filepath)
                            db.child("Courses").child(course_id).update({"Pdf": newList})

                        if type == "video":
                            filepath = uploadFile(storage, course, filename + ".mp4", type,
                                                  file)  # .mp4 ; .avi avoir des types prédéf ?
                            newList = course["Videos"][:]
                            newList.append(filepath)
                            db.child("Courses").child(course_id).update({"Videos": newList})

                        # course = course_d.val()
                        if "Pdf" and "Videos" not in course:
                            db.child("Courses").child(course_id).update({"Pdf": [""], "Videos": [""]})
                        course = db.child("Courses").child(course_id).get().val()
                        pathsPDF = course["Pdf"][:]
                        pathsVideos = course["Videos"][:]

                        if pathsPDF[0] == "":
                            del pathsPDF[0]
                        if pathsVideos[0] == "":
                            del pathsVideos[0]
                        # linksPDF = []
                        fileNamesPdf = []

                        for path in pathsPDF:
                            # link = constructLink(storage, path, token=session["idToken"])
                            # linksPDF.append(link)

                            fileNamesPdf.append(getFileName(path))

                        # linksVideos = []
                        fileNamesVideos = []

                        for path in pathsVideos:
                            # linksVideos.append(constructLink(storage, path,token=session["idToken"]))
                            fileNamesVideos.append(getFileName(path))

                        return render_template('details.html', cours=course, stud=stud, key=course_id, status="",ListPdf=fileNamesPdf,ListVideos=fileNamesVideos,author=True)

                elif request.method == 'GET':

                    return render_template("form_upload.html", course_id=course_id)

                else:
                    print("lol ?")
            else:
                print("tu ne peux pas faire de formulaire pour ce cours, ce n'est pas le tien")
                return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("connexion"))




@app.route('/streaming/<course_id>/Authors/<mail>/Languages/<language>/Courses/<course>/files/video/<filename>',methods=["GET", "POST"])
def watchVideo(course_id,mail, language, course, filename):

    if 'mail' in session:
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        course_d = findCourse(db, course_id)

        if course_d:


                storagePath = "/Authors/" + mail + "/Languages/" + language + "/Courses/" + course + "/files/video/" + filename
                firebase = pyrebase.initialize_app(firebaseConfig)
                storage = firebase.storage()

                workingdir = os.path.abspath(os.getcwd())

                filepath = workingdir + '/temporary/video/'
                ##TELECHARGEMENT DU FICHIER
                storage.child(storagePath).download(filename=filename, path=storagePath)

                # DEPLACEMENT DU FICHIER (pas obligatoire car on le supprime)
                shutil.move(workingdir + "/" + filename, filepath + filename)

                # SUPPRESSION DU FICHIER
                # os.remove(filepath + filename)
                return send_from_directory(filepath, filename)

        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("connexion"))


@app.route('/viewPdf_file/<course_id>/Authors/<mail>/Languages/<language>/Courses/<course>/files/pdf/<filename>',methods=["GET","POST"])
def watchPdf_file(course_id,mail,language,course,filename):

    if 'mail' in session :


        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        course_d = findCourse(db, course_id)

        if course_d:

                storagePath="/Authors/"+mail+"/Languages/"+language+"/Courses/"+course+"/files/pdf/"+filename
                firebase = pyrebase.initialize_app(firebaseConfig)
                storage = firebase.storage()

                workingdir = os.path.abspath(os.getcwd())

                filepath = workingdir + '/temporary/pdf/'
                ##TELECHARGEMENT DU FICHIER
                storage.child(storagePath).download(filename=filename,path=storagePath)

                #DEPLACEMENT DU FICHIER (pas obligatoire car on le supprime)
                shutil.move(workingdir+"/"+filename,filepath+filename)

                #SUPPRESSION DU FICHIER
                #os.remove(filepath + filename)
                return send_from_directory(filepath, filename)

        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("connexion"))



if __name__ == "__main__":
    app.debug=True
    app.run()