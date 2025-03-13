import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pickle

custom_css = """
<style>
    /* Main background (applies to the whole page) */
    body, .reportview-container {
        font-family: "Arial", sans-serif;
        text-align: center;
    
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #516494;
    }
   
    /* Bold sidebar title */
    [data-testid="stSidebar"] h1 {
        font-weight: bold;
        text-align: left;
    }
   
    /* Style the dog speech text (lighter green background) */
    .dog-text {
        text-align: center;
        font-size: 15px;
        color: #000000;
        background-color: #8796bf;  /* Lighter green than the page background */
        padding: 15px;
        border-radius: 10px;
        box-shadow: none;
    }
   
    /* Targeting Streamlit markdown elements directly */
    div.stMarkdown p {  
        padding: 15px;
        border-radius: 10px;
        box-shadow: none;
    
    /* Center the image */
    .center {
        display: flex;
        justify-content: center;
    }
    
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.sidebar.title("Welcome to The Diabetometer!")


st.sidebar.image("Doggy.jpg", width=200)
st.sidebar.markdown(
    "<p class='dog-text'>🐶 Woof! Hi, I am <b>Doctor Olivia McCutie</b>, and I am here to help you with your analysis."
    " How <b>The Diabetometer</b> works is, you need to fill in all the necessary data shown in your screen, and our "
    "<b>Super-Duper Intelligent friend Diabetometer</b> will predict if you have diabetes or not with incredible accuracy so that "
    "you don't have to do all those boring and expensive tests! Isn't it great? Woof Woof! 🐶</p>",
    unsafe_allow_html=True
)

st.title("Parameters for the prediction")

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Before we start, please tell us your name:</p>', unsafe_allow_html=True)
name=st.text_input("First Name:")
last_name=st.text_input("Last Name:")
name_button=st.button("SUBMIT")
if name_button==True:
    name=name
    last_name=last_name

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br>Please insert your weight in KG:</p>', unsafe_allow_html=True)
weightkg=st.slider("",min_value=30.00,max_value=500.00,value=70.00,step=0.5)
weightlb=weightkg*2.205
st.markdown(f'<p style="font-size:16px; color:grey;">(This in pounds would be: {weightlb:.2f} lb)</p>', unsafe_allow_html=True)

st.markdown(f'<p style="font-size:20px; font-weight:bold; text-align:left; ">Please insert your height in METERS:</p>', unsafe_allow_html=True)
heightmt=st.slider("",min_value=0.60,max_value=2.80,value=1.65,step=0.01)
heightft=heightmt*3.281
st.markdown(f'<p style="font-size:16px; color:grey;">(This is in feet would be: {heightft:.2f} feet)</p>', unsafe_allow_html=True)

BMI=weightkg/(heightmt**2)
st.markdown(f'<p style="font-size:20px; text-align:left; "><b>Your BMI ratio is --&rarr;</b> {BMI:.2f} KG/M<sup>2</sup></p>', unsafe_allow_html=True)

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Please insert the aproximate hours you sleep per night:</p>', unsafe_allow_html=True)
sleep=st.slider("",min_value=0.0,max_value=12.0,value=6.0,step=0.5)

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Please insert your aproximate stress level:</p>', unsafe_allow_html=True)
stresslvl=st.slider("",min_value=1.0,max_value=10.0,value=5.0,step=0.5)

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Please insert the number of pregnancies you have gone through:</p>', unsafe_allow_html=True)
pregnancies=st.slider("",min_value=0,max_value=20,value=6,step=1)

min_birth_date = datetime.date(1900, 1, 1)
max_birth_date = datetime.date.today()
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Please insert your date of birth:</p>', unsafe_allow_html=True)
birth=st.date_input('',min_value=min_birth_date,max_value=max_birth_date)
today = datetime.date.today()
age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
st.markdown(f'<p style="font-size:16px; color:grey;">(Meaning you are {age} years old)</p>', unsafe_allow_html=True)

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Now please from the following boxes, check the ones which apply to you:</p>', unsafe_allow_html=True)
col1,col2,col3=st.columns(3)
with col1:
    history=st.checkbox("Family history of diabetes")
    hypertension=st.checkbox("Hypertension")
with col2:
    hyperlipidemia=st.checkbox("Hyperlipidemia")
    cardiovasc=st.checkbox("Cardiovascular disease")
with col3:
    polyov=st.checkbox("Polycystic Ovary Syndrome")

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br>Please select your smoking status at the moment:</p>', unsafe_allow_html=True)
smoker=st.radio("",('Never','Former','Current'))
smokestat=0
if smoker=='Current':
    smokestat=2
elif smoker=='Former':
    smokestat=1
else:
    smokestat=0

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">Lastly, please select your ethnicity:</p>', unsafe_allow_html=True)
ethnicity=st.selectbox('',('African','Asian','Caucasian','Hispanic','Other'))
African=0
Asian=0
Caucasian=0
Hispanic=0
Other=0
if ethnicity=='African':
    African=1
    Asian=0
    Caucasian=0
    Hispanic=0
    Other=0
elif ethnicity=='Asian':
    African=0
    Asian=1
    Caucasian=0
    Hispanic=0
    Other=0
elif ethnicity=='Caucasian':
    African=0
    Asian=0
    Caucasian=1
    Hispanic=0
    Other=0
elif ethnicity=='Hispanic':
    African=0
    Asian=0
    Caucasian=0
    Hispanic=1
    Other=0
elif ethnicity=='Other':
    African=0
    Asian=0
    Caucasian=0
    Hispanic=0
    Other=1

st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True) #JUST A SPACE BETWEEN TEXT AND BUTTON

loaded_model = pickle.load(open('picklemodel.pkl','rb'))
scaler = pickle.load(open('scalermodel.pkl','rb'))

input_data1 = np.array([[age, pregnancies, smokestat, sleep, stresslvl, BMI]])
std_data = scaler.transform(input_data1)

input_data2 = np.array([[history, hypertension, hyperlipidemia, cardiovasc, polyov, African, Asian, Caucasian, Hispanic, Other]])

final_data = np.hstack((std_data, input_data2))
final_reshaped = final_data.reshape(1, -1)

prediction = loaded_model.predict_proba(final_reshaped)

button=st.button("GET TEST RESULTS")
if button==True:
    if prediction[0][1]>0.3:
        st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">There are considerably high odds of you having diabetes, but do not worry, it could be a false positive. You should consider taking more tests to be sure, better be safe than sorry</p>', unsafe_allow_html=True)
    else:
        st.balloons()
        st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; ">You are as healthy as an apple, good job, keep it up!</p>', unsafe_allow_html=True)
