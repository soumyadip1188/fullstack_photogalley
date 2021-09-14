from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import datetime
from werkzeug.utils import secure_filename
from flask import session
import random

from flask_mail import *  #for mail



 
from flask_pymongo import PyMongo
  
app = Flask(__name__) #creating the Flask class object   
 
UPLOAD_FOLDER = 'static/uploads/'


#Flask mail configuration  
app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'picturegallary5@gmail.com'  
app.config['MAIL_PASSWORD'] = 'soumya@123'  
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True  
  
#instantiate the Mail class  
mail = Mail(app) 






app.secret_key = "secret_key" 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# mongodb+srv://rup123:<password>@cluster0.jhyqq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
# mongodb://localhost:27017/picture
mongodb_client = PyMongo(app, uri="mongodb+srv://rup123:rup123@cluster0.jhyqq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = mongodb_client.db
 

@app.route('/') #decorator defines the   
def indexpage():  
    return render_template('index.html')

# @app.route('/indexpage') #decorator defines the   
# def index():  
#     return render_template('index.html')





@app.route('/pic',methods=['GET','POST']) #decorator defines the   
def pic():    
       
        userobj = db.uploadcollection.find({}) 
        print(userobj)
        return render_template('pic.html',userdata=userobj)
        

        









@app.route('/about') #decorator defines the   
def about():  
    return render_template('about.html')

@app.route('/team') #decorator defines the   
def team():  
    return render_template('team.html')

@app.route('/gallary') #decorator defines the   
def gallery():  
    return render_template('gallaery.html')



@app.route('/userafterlogin',methods=['GET','POST']) #decorator defines the   
def userafter():    
        uname=session['uname']
        userobj = db.uploadcollection.find({}) 
        print(userobj)
        return render_template('userafterlogin.html',userdata=userobj,uname = session['uname'])
        


@app.route('/allviewimage', methods=['GET','POST'])  #userdownloadimage
def userdownloadimg(): 
    if request.method == 'GET':
        return render_template('allviewimage.html')
    else:      
        userobj = db.uploadcollection.find({'catagory': request.form['cata']})
        print(userobj)
                
        if userobj:
            return render_template('allviewimage.html', userdata = userobj,show_results=1)
        else:
            return render_template('allviewimage.html', errormsg = "INVALID CATAGORY NAME")


@app.route('/beforeallviewimg', methods=['GET','POST'])  #userdownloadimage
def userdownloadimg3(): 
    if request.method == 'GET':
        return render_template('beforeallviewimg.html')
    else:      
        userobj = db.uploadcollection.find({'catagory': request.form['cata']})
        print(userobj)
                
        if userobj:
            return render_template('beforeallviewimg.html', userdata = userobj,show_results=1)
        else:
            return render_template('beforeallviewimg.html', errormsg = "INVALID CATAGORY NAME")







@app.route('/registration', methods=["GET", "POST"])  
def userregpage():
    if request.method == 'GET':
        return render_template('registration.html')
    else:
        x=datetime.datetime.now()
        x = ''+str(x)
        #print(x)
        userobj = db.usercollection.find_one(
        {'useremail':request.form['email']})
        print(userobj)
        
        if userobj:
            return render_template('registration.html',msg='User already registered')
        else:
            uname = request.form['fullname']
        
            db.usercollection.insert_one(
            {'userfullname': uname,
            'username':request.form['username'],
            'useremail': request.form['email'],
            'usermobile': request.form['ph'],
            'userpass': request.form['userpass'],
            # 'userconpass': request.form['userconpass'],
            'regdate':x
            })
            #mail send message
            msg = Message('subject', sender = 'picturegallary5@gmail.com', recipients=[request.form['email']]) 
            s = 'Dear '+request.form['fullname'] 
            n ='your username '+request.form['username']+' and password is '+request.form['userpass']+'Do not share your credentials with anyone for sequrity and privacy purpose'
            msg.body = s+' Congratulation,You have succesfully registered our website '+n 
            mail.send(msg)

            return render_template('registration.html',msg = "REGISTRATION SUCCESSFUL")

@app.route('/login', methods=["GET", "POST"])  
def userloginpage(): 
    if request.method == 'GET': 
        return render_template('login.html')
    else:
        user = db.usercollection.find_one(
        {'username': request.form['username'],
         'userpass': request.form['userpass']
        })
        #print(user)
        
        if user:
            #print(user['username'])
            session['uemail']= user['useremail']
            session['uname'] = user['username']
            session['usertype']= 'USER'
            return redirect(url_for ('userafter'))
        else:
            return render_template('login.html', errormsg = "INVALID UID OR PASSWORD")




@app.route('/contact', methods=["GET", "POST"])  
def usercontact():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        uname = request.form['first_name']
       
        x=datetime.datetime.now()
        x = ''+str(x)

        db.usercontactcollection.insert_one(
        {'username': uname,
        'userlastname':request.form['last_name'],
        'useremail': request.form['email'],
        'usermessage':request.form['message'],
        'regdate':x,
        })
        #for contact mail send
        msg = Message('subject', sender = 'picturegallary5@gmail.com', recipients=[request.form['email']])  
        s= 'Dear '+request.form['first_name']
        msg.body =  s +' we will recived your problem,Our team will slove your problem as soon as possible'       
        mail.send(msg)

        return render_template('contact.html',msg = "Thanks! we will solve your problem soon, please check your mail")


@app.route('/admin', methods=['GET','POST'])  
def adminloginpage(): 
    if request.method == 'GET':
        return render_template('admin.html')
    else:      
        adminuid = request.form['adminuserid']
        adminpass = request.form['adminpass']

        if(adminuid == 'admin' and adminpass == 'soumya123'):
            # session['usertype'] ='ADMIN'
            return render_template('adminafterlogin.html')
        else:
            return render_template('admin.html', msg = 'INVALID UID OR PASS')

@app.route('/adminhome')  
def adminafterlogin(): 
    return render_template('adminafterlogin.html')

@app.route('/viewall')  
def viewall(): 
    userobj = db.usercollection.find({})
    print(userobj)
    return render_template('viewalluser.html', userdata = userobj)


# @app.route('/imageinfo')  
# def image(): 
#     userobj = db.uploadcollection.find({})
#     print(userobj)
#     return render_template('imageinfo.html', userdata = userobj)


@app.route('/dashboard')  
def dash():
    return render_template('dashboard.html')



        
@app.route('/logout')  
def logout():  
    if 'usertype' in session:
        utype = session['usertype']
        if utype == 'ADMIN':
            session.pop('usertype',None)
        else: 
            session.pop('usertype',None)
            session.pop('uemail',None)
            session.pop('uname',None)
        return redirect(url_for('indexpage'));    
    else:  
        return redirect(url_for('adminloginpage'));     



    







@app.route('/upload', methods=["get","post"])  
def upload():
    if request.method == 'GET':        
        return render_template('upload.html')
    # else:
    #     uname = request.form['fullname']    

       
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded')
        path = 'static/uploads/'+filename

        uname=session['uname']

        x=datetime.datetime.now()
        x = ''+str(x)
        
        n=str(random.randint(0,1000))

        db.uploadcollection.insert_one(
           {'username': uname,
             
            'pthotoid': n,
            'catagory': request.form['cata'] ,
            'image': path,
            'regdate':x,
        })
        return render_template('upload.html', filename=filename)

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
        


@app.route('/search', methods=['GET','POST'])  
def searchUser(): 
    if request.method == 'GET':
        return render_template('search.html')
    else:      
        userobj = db.usercollection.find_one({'useremail': request.form['email']})
        print(userobj)
        
        if userobj:
           
            return render_template('search.html', userdata = userobj,show_results=1)
        else:
            return render_template('search.html', errormsg = "INVALID EMAIL ID")


@app.route('/delete', methods=['GET','POST'])  
def deleteUser(): 
    if request.method == 'GET':
        return render_template('delete.html')
    else:      
        responsefrommongodb = db.usercollection.find_one_and_delete(
        {'useremail': request.form['email']})
        print(responsefrommongodb)
        if responsefrommongodb is not None:
            return render_template('delete.html', msg = "SUCCESSFULLY DETELED")
        return render_template('delete.html', msg = "INVALID EMAIL ID")




@app.route('/delete1', methods=['POST'])  
def deleteUser1():
    print(request.form['email']) 
    responsefrommongodb = db.usercollection.find_one_and_delete({'useremail': request.form['email']})
    print(responsefrommongodb)
    return redirect(url_for('viewall'))

@app.route('/delete2', methods=['POST'])  
def deleteUser2():
    print(request.form['email']) 
    responsefrommongodb = db.usercollection.find_one_and_delete({'useremail': request.form['email']})
    print(responsefrommongodb)
    return redirect(url_for('searchUser'))



@app.route('/delete3', methods=['POST'])  
def deleteUser3():
    print(request.form['photoid']) 
    responsefrommongodb = db.uploadcollection.find_one_and_delete({'pthotoid': request.form['photoid']})
    print(responsefrommongodb)
    return redirect(url_for('viewimage'))


@app.route('/delete4', methods=['POST'])  
def deleteUser4():
    print(request.form['photoid']) 
    responsefrommongodb = db.uploadcollection.find_one_and_delete({'pthotoid': request.form['photoid']})
    print(responsefrommongodb)
    return redirect(url_for('image'))


@app.route('/delete5', methods=['POST'])  
def deleteUser5():
    print(request.form['email']) 
    responsefrommongodb = db.usercontactcollection.find_one_and_delete({'useremail': request.form['email']})
    print(responsefrommongodb)
    return redirect(url_for('viewcontac'))





@app.route('/imageinfo', methods=['GET','POST'])  
def image(): 
    # if request.method == 'GET':
    #     return render_template('imageinfo.html')
    # else:      
        userobj = db.uploadcollection.find({'username': session['uname']})  
        # print(uobj)        
        if userobj:
            #print(userobj['username'])
            return render_template('imageinfo.html', userdata = userobj,show_results=1)
        else:
            return render_template('imageinfo.html', errormsg = "NO IMAGE FOUND")


@app.route('/accountinfo', methods=['GET','POST'])  
def account(): 
    if request.method == 'GET':
        return render_template('account.html')
    else:      
        uobj = db.usercollection.find_one({'useremail': request.form['email']})
        print(uobj)        
        if uobj:
            #print(userobj['username'])
            return render_template('account.html', userdata = uobj,show_results=1)
        else:
            return render_template('account.html', errormsg = "INVALID EMAIL ID")



@app.route('/viewimage')  
def viewimage(): 
    userobj = db.uploadcollection.find({})
    print(userobj)
    return render_template('viewimage.html', userdata = userobj)


@app.route('/viewcontact')  
def viewcontac(): 
    userobj = db.usercontactcollection.find({})
    print(userobj)
    return render_template('viewcontact.html', userdata = userobj)








@app.route('/userprofile')  
def viewUserProfile(): 
    uemail = session['uemail']      
    userobj = db.usercollection.find_one({'useremail': uemail})
    print(userobj)
    return render_template('userprofile.html', userdata = userobj,uname=session['uname'])

   
@app.route('/update', methods=["GET", "POST"])  
def updateUserProfile():
    if request.method == 'GET':
        uemail = session['uemail']      
        userobj = db.usercollection.find_one({'useremail': uemail})
        return render_template('updateuser.html',userdata = userobj)
    else:
        db.usercollection.update_one( {'useremail': session['uemail'] },
        { "$set": { 'usermobile': request.form['ph'],
                    'userpass': request.form['userpass'],
                    # 'useraddress': request.form['address'] 
                  } 
        })
        return redirect(url_for('viewUserProfile'))



if __name__ =="__main__":  
    app.run(debug = True,port=4000)