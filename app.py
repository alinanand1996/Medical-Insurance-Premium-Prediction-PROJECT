from flask import Flask, render_template,request
import pickle
import numpy as np
import pandas as pd

#loading pickle files
model= pickle.load(open('model.pkl','rb'))
scaler= pickle.load(open('scaler.pkl','rb'))
scalers=pickle.load(open('scalers.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/submit',methods=['POST'])

def submit():
    cnam = request.form.get('cust_name')
    cage = int(request.form.get('cust_age'))
    gender = request.form.get('cust_gender')
    cjob = request.form.get('cust_occupation')
    
    cholestrol = float(request.form.get('cust_cholesterol_level'))
    disease = request.form.getlist('disease')
    glucose_level = float(request.form.get('cust_average_glucose_level'))
    height = float(request.form.get('cust_height'))
    weight = float(request.form.get('cust_weight'))
    loc = request.form.get('patient_location')

    sports = request.form.get('patient_participates_in_adventure_sports')
    medExp = float(request.form.get('cust_average_medExp'))

    if gender=='male': gen=1 
    else: gen=0

    if cjob=='Manual Labourer': job=0
    elif cjob=='Office Worker': job=1
    elif cjob=='Self-employed': job=2
    elif cjob=='Un-employed': job=3
    

    len_lst=len(disease)
    if len_lst==1:
        if disease[0]=='Heart disease':  disease_hist=2
        elif disease[0]=='Other major disease': disease_hist=1
    elif len_lst==0: disease_hist=0
    else:
        if disease[0]=='Heart disease' and disease[1]=='Other major disease': disease_hist=3
    

     
    if len_lst==1:
        if disease[0]=='Heart disease':  disease='Have heart disease history'
        elif disease[0]=='Other major disease': disease='Have other major disease history'
    elif len_lst==0: disease_hist=0
    else:
        if disease[0]=='Heart disease' and disease[1]=='Other major disease': disease= 'Have both heart disease and othe major disease history'
    

    height=height/100
    bmi=weight/height

    if loc=='Rural': Ploc=0
    elif loc=='Sub-Urban': Ploc=1
    elif loc=='Urban': Ploc=2

    if sports=='yes':sport=1
    else: sport=0


    #converting to array
    cols=[ 'patient_participates_in_adventure_sports', 'patient_occupation',
       'patient_cholesterol_level', 'patient_age',
       'patient_has_major_disease_history', 'patient_gender',
       'patient_average_glucose_level', 'patient_body_mass_index',
       'patient_location', 'patient_average_medical_expenses']
    values=[sport,job,cholestrol,cage,disease_hist,gen,glucose_level,bmi,medExp,Ploc]
    df=pd.DataFrame([values],columns=cols)
    scaled_data=scaler.fit_transform(df)
    scaled_data_df=pd.DataFrame(scaled_data,columns=cols)
    data_scaled=scalers.fit_transform(df)
    datascaleddf=pd.DataFrame(data_scaled,columns=cols)
   
    pred=model.predict(df)
    pred=int(pred[0])
    data=[cnam,cage,gender,cjob,cholestrol,disease,glucose_level,bmi,sports,Ploc,medExp,pred]
    #data=dict(zip(cols,values))
    return render_template('result.html',cnam=cnam,cage=cage,gender=gender,cjob=cjob,cholestrol=cholestrol,disease=disease,glucose_level=glucose_level,bmi=bmi,sports=sports,medExp=medExp,loc=loc,pred=pred)

if __name__ == "__main__":
    app.run(debug=True)











    
