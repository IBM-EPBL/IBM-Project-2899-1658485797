import re
import numpy as np
import os
from flask import Flask,  app,request,render_template
from keras import models
from keras.models import load_model
from keras.utils import load_img, img_to_array
from tensorflow.python.ops.gen_array_ops import concat
from keras.applications.inception_v3 import preprocess_input
import requests
from flask import Flask,  request,  render_template,  redirect,  url_for
#Loading the model
from cloudant. client import Cloudant

ACCOUNT_NAME, API_KEY="9fb89a85-3269-409a-b07e-d6f1c6655d2d-bluemix","ivgHwvQ6hgCJKUFrvXyTKjJ5paxq6El4LniER2zT_mc7"
client = Cloudant.iam(ACCOUNT_NAME, API_KEY, connect=True)

my_database=client.create_database('my_database')

model1 = load_model('C:\\Users\\ADMIN\\Downloads\\vggmodelfinalbody.h5')
model2 = load_model('C:\\Users\\ADMIN\\Downloads\\vggmodelfinallevel.h5')

app = Flask(__name__)

#default home page or route
@app.route('/')
def index():
    return  render_template("index.html")

@app.route('/index')
def home():
    return render_template("index.html")

#registration page
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/afterreg', methods=['POST']) 
def afterreg(): 
    x = [x for x in request.form.values()] 
    print(x) 
    data = {
    '_id' : x[1],  # Setting _id is optional
    'name' : x[0],
    'psw' : x[2]
    }
    print(data)

    query = {'_id': {'$eq': data['_id']}}

    docs= my_database.get_query_result(query) 
    print(docs)

    print(len(docs.all()))

    if(len(docs.all()) == 0):
        url = my_database.create_document(data) 
        #response requests.get(url)

        return render_template('prediction.html') 
    else:
        return render_template('register.html', pred="*You are already a member, please Login using your details")


#login page
@app.route('/login') 
def login(): 
    return render_template('login.html')

@app.route('/afterlogin', methods=['POST']) 
def afterlogin(): 
    user = request.form['email'] 
    passw = request.form['password'] 
    print(user, passw)

    query = {'_id': {'$eq': user}}

    docs = my_database.get_query_result(query) 
    print(docs)

    print(len(docs.all()))

    if(len(docs.all())==0):
        return render_template('login.html', pred="*Credentials are invalid")

    else:
        if((user==docs[0][0]['_id'] and passw==docs[0][0]['psw'])): 
            return redirect(url_for('prediction'))
        else:
            print('Invalid User')

@app.route('/logout') 
def logout():
    return render_template('logout.html')

@app.route('/prediction') 
def prediction():
    return render_template('prediction.html')

@app.route('/result', methods=["GET", "POST"])
def res():
    
    if request.method=="POST":
        # f = request.files['file']
        # basepath = os.path.dirname(__file__) #getting the current path i.e where app.py is present 
        # #print("current path", basepath) 
        # filepath = os.path.join(basepath, 'uploads', f.filename) #from anywhere in the system we can give image t 
        # #print("upload folder is", filepath) 
        # f.save(filepath)

        imagefile=request.files['file']
        img_pa="E:\\IBM\\static\\uploads\\" + imagefile.filename
        imagefile.save(img_pa)

        # img = image.load_img(img_pa, target_size=(224,224)) 
        # x = image.img_to_array(img)#ing to array 
        # x - np.expand_dims (x, axis=8) #used for adding one more dimension
        # #print(x)
        # img_data = preprocess_input(x) 
        # prediction1 = np.argmax(model1.predict(img_data)) 
        # prediction2 = np.argsax(model2.predict(img_data))

        img1 = load_img(img_pa,target_size=(224,224))
        img1 = img_to_array(img1)
        img1 = img1/255.0
        img1 = np.expand_dims(img1,axis=0)
        prediction1 = np.argmax(model1.predict(img1),axis=1)
        prediction2 = np.argmax(model2.predict(img1),axis=1)
        #prediction-model.predict(x)#instead of predict_classes (x) we can use predict(x) --->predict_classes
        #print("prediction is ",prediction)

        index1 = ['front', 'rear', 'side']
        index2 = ['minor', 'moderate', 'severe']
        #result = str(index[output[0]])

        # print(prediction1,prediction2)
        # print(type(prediction1))
        result1 = index1[prediction1[0]]    
        result2 = index2[prediction2[0]]

        
        if (result1 == "front" and result2 == "minor"): 
            value = "3000 - 5000 INR"
        elif(result1 == "front" and result2 == "moderate"): 
            value = "6000 - 8000 INR"
        elif (result1 == "front" and result2 == "severe"):
            value = "9000 - 11000 INR"
        elif (result1 == "rear" and result2 == "minor"):
            value = "4000- 6000 INR"
        elif (result1 == "rear" and result2 == "moderate"):
            value = "7000- 9000 INR"
        elif (result1 =="rear" and result2 == "severe"):
            value = "11000 - 13000 INR" 
        elif (result1 =="side" and result2 == "minor"):
            value = "6000 - 8000 INR" 
        elif(result1 =="side" and result2 == "moderate"):
            value = "9000 - 11000 INR"
        elif(result1 == "side" and result2 == "severe"):
            value = "12000 - 15000 INR"
        else:
            value = "16008 - 50000 INR"

        return value    
    return None

if __name__ == "__main__":
    app.run(debug=True, port = 8080)