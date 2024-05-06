from sklearn import tree
import pandas as pd
import base64
from sklearn.model_selection import train_test_split
import math
from tensorflow import keras
from keras.models import load_model
from streamlit_option_menu import option_menu
import pickle
import streamlit as st
import io
from PIL import ImageOps, Image
import numpy as np
import joblib
import PIL.Image
import tensorflow as tf
from streamlit_chat import message
import os
#import openai
import tensorflow as tf
from PIL import Image
import numpy as np
#rom tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow import keras
from keras.layers import Dense
from keras.models import Sequential, load_model
import tensorflow as tf
#openai.api_key = "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"
from code.DiseaseModel import DiseaseModel
from code.helper import prepare_symptoms_array


with open('pic2.jpg', "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# sidebar for navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction WebApp',

                           ['HOME',
                            'Disease Prediction',
                            'Heart Disease Prediction',
                            #'Hepatitis Mortality Predictor',
                            #'Parkinsons Prediction',
                            'Parkison Prediction',
                            'Diabetes Prediction',
                            #'Diabetes Prediction',
                            # 'Plant Diesease Detection',
                            'Liver Disease Prediction',
                            'Pneumonia Detector',
                            'Malaria Detector',
                            'Risk Factor Assessment',
                            'Help - ChatBot'],

                           icons=['house','heart','person','stack','lungs','bug','exclamation-triangle','robot'],
                           default_index=0)

if (selected == 'HOME'):
    st.title("Multiple Disease Prediction WebApp")
    st.write("")
    image = Image.open('HOME.jpg')
    new_image = image.resize((800, 500))
    st.image(new_image)
    st.title("**Welcome to our Disease Prediction Web App**")
    st.write("Harnessing the power of machine learning and advanced algorithms, our web application allows you to predict and assess various diseases with ease. Input your information and receive accurate predictions for conditions such as heart disease, hepatitis, Parkinson's disease, diabetes, pneumonia, and liver disease.")
    st.write("Our cutting-edge models, trained on extensive datasets, provide reliable insights into your health. Whether you're concerned about your cardiovascular health, liver function, or risk factors for diabetes, our app has you covered. Simply enter your details, and our intelligent algorithms will analyze the data to generate personalized predictions.")
    st.write("In addition to disease predictions, our app features an AI-powered chatbot equipped with state-of-the-art language models. Chat with our virtual doctor and get expert advice on various health-related queries.")
    st.write("With our web application, you can take charge of your well-being, make informed decisions, and seek timely medical intervention when necessary. Experience the future of healthcare with our comprehensive disease prediction app and embark on a journey towards a healthier life.")
    st.write("Connect Me at:")
    st.write("Github Link : https://github.com/vinaykumar11111/multiple_disease-prediction")
    st.write("LinkedIn Link : ")
    st.write("Email : contact123@gmail")       



if selected == 'Disease Prediction': 
    # Create disease class and load ML model
    disease_model = DiseaseModel()
    disease_model.load_xgboost('model/xgboost_model.json')

    # Title
    st.write('# Disease Prediction using Machine Learning')

    symptoms = st.multiselect('What are your symptoms?', options=disease_model.all_symptoms)

    X = prepare_symptoms_array(symptoms)

    # Trigger XGBoost model
    if st.button('Predict'): 
        # Run the model with the python script
        
        prediction, prob = disease_model.predict(X)
        st.write(f'## Disease: {prediction} with {prob*100:.2f}% probability')


        tab1, tab2= st.tabs(["Description", "Precautions"])

        with tab1:
            st.write(disease_model.describe_predicted_disease())

        with tab2:
            precautions = disease_model.predicted_disease_precautions()
            for i in range(4):
                st.write(f'{i+1}. {precautions[i]}')



# Liver Disease Prediction Page used # https://www.kaggle.com/datasets/abhi8923shriv/liver-disease-patient-dataset
if (selected == 'Liver Disease Prediction'):

    st.title('Liver Disease Prediction')
    st.button("About", help="The Liver Disease Predictor App is a powerful tool designed to assess the likelihood of liver disease based on specific patient information. By inputting the patient's sex (A), age (B), total bilirubin (C), direct bilirubin (D), alkaline phosphatase (E), alanine aminotransferase (F), aspartate aminotransferase (G), total proteins (H), albumin (I), and albumin and globulin ratio (J), the app generates a comprehensive analysis. Utilizing advanced algorithms, it evaluates the data to provide an accurate prediction regarding the presence or absence of liver disease. This app empowers healthcare professionals to make informed decisions and facilitate early intervention, ultimately improving patient outcomes and liver health management.  DataSet Used : https://www.kaggle.com/datasets/abhi8923shriv/liver-disease-patient-dataset")
    image = Image.open('Liver.jpeg')
    new_image = image.resize((800, 500))
    st.image(new_image)
    info = pd.read_csv('dataset.csv')
    info['Albumin_and_Globulin_Ratio'].fillna(
        info['Albumin_and_Globulin_Ratio'].median(), inplace=True)

    dt = tree.DecisionTreeClassifier()
    info.rename(columns={'Dataset': 'Target'}, inplace=True)

    X = info.drop('Target', axis=1)
    y = info['Target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

    dt.fit(X_train, y_train)

    B = st.slider("Age", int(info["Age"].min()), int(info["Age"].max()))
    A = st.slider("Gender", int(
        info["sex"].min()), int(info["sex"].max()))
    C = st.slider("Total Bilirubin", int(
        info["Total_Bilirubin"].min()), int(info["Total_Bilirubin"].max()))
    D = st.slider("Direct Bilirubin", int(
        info["Direct_Bilirubin"].min()), int(info["Direct_Bilirubin"].max()))
    E = st.slider("Alkaline Phosphotase", int(
        info["Alkaline_Phosphotase"].min()), int(info["Alkaline_Phosphotase"].max()))
    F = st.slider("Alamine Aminotransferase", int(
        info["Alamine_Aminotransferase"].min()), int(info["Alamine_Aminotransferase"].max()))
    G = st.slider("Aspartate Aminotransferase", int(
        info["Aspartate_Aminotransferase"].min()), int(info["Aspartate_Aminotransferase"].max()))
    H = st.slider("Total Protiens", int(
        info["Total_Protiens"].min()), int(info["Total_Protiens"].max()))
    I = st.slider("Albumin", int(
        info["Albumin"].min()), int(info["Albumin"].max()))
    J = st.slider("Albumin Globulin Ratio", int(
        info["Albumin_and_Globulin_Ratio"].min()), int(info["Albumin_and_Globulin_Ratio"].max()))

    features = [A, B, C, D, E, F, G, H, I, J]
    st.write(info.astype(int).info())
    pretty_result = {"Sex": A, "age": B, "Total_Bilirubin": C, "Direct_Bilirubin": D, "Alkaline_Phosphotase": E, "Alamine_Aminotransferase": F,
                     "Aspartate_Aminotransferase": G, "Total_Protiens": H, "Albumin": I, "Albumin_and_Globulin_Rati": J}
    st.json(pretty_result)
    if st.button('Submit'):
        results = dt.predict([features])
        st.title('Predection')
        for final in results:
            if final == 1:
                st.warning('\n You have a Liver Disease')
            else:
                st.success(' You do NOT have a Liver Disease')


# Heart Disease Prediction Page
if (selected == 'Heart Disease Prediction'):
    st.title('Heart Disease Prediction using ML')
    st.button("About", help="The Heart Disease Predictor App is a cutting-edge tool designed to assess the risk of heart disease based on specific patient information. By inputting the patient's age, chest pain type (cp), sex, resting blood pressure (trestbps), cholesterol level (chol), fasting blood sugar (fbs), resting electrocardiographic results (restecg), exercise-induced angina (exang), ST depression induced by exercise relative to rest (oldpeak), slope of the peak exercise ST segment (slope), number of major vessels colored by fluoroscopy (ca), thallium stress test result (thal), and maximum heart rate achieved (thalach), the app utilizes advanced algorithms to generate a comprehensive analysis. This empowers healthcare professionals to make informed decisions, provide personalized care, and effectively manage heart disease.\nDataset used Link : https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset?datasetId=216167&sortBy=voteCount")
    image = Image.open('heart2.png')
    new_image = image.resize((800, 500))
    st.image(new_image)

    age = st.slider('age', 29, 77, 40, 1)
    cp = st.slider('cp', 0, 3, 1, 1)
    sex = st.slider('sex', 0, 1, 0, 1, help="0=female,1=male")
    trestbps = st.slider('trestbps', 94, 200, 80, 1)
    chol = st.slider('chol', 126, 564, 246, 2)
    fbs = st.slider('fbs', 0, 1, 0, 1)
    restecg = st.slider('restecg', 0, 2, 1, 1)
    exang = st.slider('exang', 0, 1, 0, 1)
    oldpeak = st.slider('oldpeak', 0.0, 6.2, 3.2, 0.2)
    slope = st.slider('slope', 0, 2, 1, 1)
    ca = st.slider('ca', 0, 4, 2, 1)
    thal = st.slider('thal', 0, 3, 1, 1)
    thalach = st.slider('thalach', 71, 202, 150, 1)

    X_test_sc = [[age, sex, cp, trestbps, chol, fbs,
                  restecg, thalach, exang, oldpeak, slope, ca, thal]]

    load_clf = pickle.load(
        open('heart_disease_model.pkl', 'rb'))

    pretty_result = {"age": age, "cp": cp, "sex": sex, "trestbps": trestbps, "chol": chol, "fbs": fbs,
                     "restecg": restecg, "exang": exang, "oldpeak": oldpeak, "slope": slope, "ca": ca, "thal": thal, "thalach": thalach}
    st.json(pretty_result)

    prediction = load_clf.predict(X_test_sc)
    answer = prediction[0]
    if st.button('Predict'):
        if answer == 0:
            st.success("Heart Disease was Not Detected")
        else:
            st.error("Heart Disease was Detected")
    st.markdown(
        "Note", help="This prediction is based on the Machine Learning Algorithm, Support Vector Machine.")

    #
    # DONE
    #

# Diabetes Disease Prediction Page
#import pickle
#if (selected == 'Diabetes Prediction'):
#    st.title(
 #       "Diabetes Risk Prediction for Females")
  #  st.markdown(
   #     "About", help="The Diabetes Risk Prediction for Females Predictor App is a powerful tool designed specifically for women to assess their risk of developing diabetes. By inputting the patient's information, including the number of pregnancies, glucose levels, blood pressure, skin thickness, insulin levels, BMI (body mass index), diabetes pedigree function, and age, the app utilizes advanced algorithms to generate a personalized analysis. It takes into account factors that are particularly relevant to females and their unique risk profiles. The app provides an accurate prediction of the likelihood of developing diabetes, enabling individuals to take proactive steps towards prevention, early detection, and appropriate management of the condition. Dataset Used : https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database")
   # image = Image.open('Diabetes.jpg')
  #  new_image = image.resize((800, 500))
 #   st.image(new_image)
  #  st.header("Just fill in the information below")
 #   Pregnancies = st.slider("Input Your Number of Pregnancies", 0, 16)
  #  Glucose = st.slider("Input your Gluclose", 74, 200)
 #   BloodPressure = st.slider("Input your Blood Pressure", 30, 130)
 #   SkinThickness = st.slider("Input your Skin thickness", 0, 100)
   # Insulin = st.slider("Input your Insulin", 0, 200)
  #  BMI = st.slider("Input your BMI", 14.0, 60.0)
  #  DiabetesPedigreeFunction = st.slider(
  #      "Input your Diabetes Pedigree Function", 0.0, 6.0)
  #  Age = st.slider("Input your Age", 0, 100)

#    inputs = [[Pregnancies, Glucose, BloodPressure, SkinThickness,
       #        Insulin, BMI, DiabetesPedigreeFunction, Age]]
  #  pretty_result = {'Pregnancies': Pregnancies, 'Glucose': Glucose, 'Blood Pressure': BloodPressure, 'Skin Thickness': SkinThickness,
  #                   'Insulin': Insulin, 'BMI': BMI, 'Diabetes Pedigree Function': DiabetesPedigreeFunction, 'Age': Age}
   # st.json(pretty_result)
   # model = pickle.load(
   #     open('Diabetes.pkl', 'rb'))
  #  if st.button('Predict'):
    #    result = model.predict(inputs)
    #    updated_res = result.flatten().astype(int)
    #    if updated_res == 0:
     #       st.success(
       #         "Unlikely for diabetes, but prioritize self-care nonetheless.")
      #      st.text("The AdaBoost Classifier was used.")
       # else:
       #     st.warning(
          #      "Possible diabetes risk, prioritize self-care.")
         #   st.text("The AdaBoost Classifier was used.")


#
# Done
#

# Parkinsons Disease Prediction Page
#if (selected == "Parkinsons Prediction"):
 #   # page title
  #  st.title("Parkinson's Disease Prediction")
   # st.button("About", help="The Parkinson's Disease Prediction Predictor App is a valuable tool designed to assess the risk of Parkinson's disease in individuals. By utilizing advanced algorithms and inputting relevant information such as age, gender, family history, tremors, rigidity, bradykinesia, gait disturbances, and balance problems, the app generates a comprehensive analysis. It evaluates the collected data to provide an accurate prediction regarding the likelihood of developing Parkinson's disease. This empowers healthcare professionals to identify individuals at risk, facilitate early intervention, and optimize management strategies. The app aids in improving patient outcomes by enabling timely diagnosis and personalized treatment plans for Parkinson's disease. Datset Used : https://www.kaggle.com/datasets/vikasukani/parkinsons-disease-data-set")
  #  image = Image.open('parkinsons-disease.jpg')
   # new_image = image.resize((800, 500))
    #st.image(new_image)
    #st.header("Just fill in the information below")
    #col1, col2, col3, col4 = st.columns(4)
    #with col1:
     #   fo = st.text_input('MDVP: Fo(Hz)')
    #with col2:
     #   fhi = st.text_input('MDVP: Fhi(Hz)')
    #with col3:
     #   flo = st.text_input('MDVP: Flo(Hz)')
    #with col4:
     #   Jitter_percent = st.text_input('MDVP: Jitter(%)')

   # with col1:
    #    Jitter_Abs = st.text_input('MDVP: Jitter(Abs)')
    #with col2:
     #   RAP = st.text_input('MDVP: RAP')
    #with col3:
     #   PPQ = st.text_input('MDVP: PPQ')
    #with col4:
     #   DDP = st.text_input('Jitter: DDP')

  #  with col1:
  #      Shimmer = st.text_input('MDVP: Shimmer')
  #  with col2:
   #     Shimmer_dB = st.text_input('MDVP: Shimmer(dB)')
    #with col3:
     #   APQ3 = st.text_input('Shimmer: APQ3')
    #with col4:
     #   APQ5 = st.text_input('Shimmer: APQ5')

   # with col1:
    #    APQ = st.text_input('MDVP: APQ')
   # with col2:
    #    DDA = st.text_input('Shimmer: DDA')
    #with col3:
     #   NHR = st.text_input('NHR')
    #with col4:
     #   HNR = st.text_input('HNR')

  #  with col1:
   #     RPDE = st.text_input('RPDE')
    #with col2:
     #   DFA = st.text_input('DFA')
    #with col3:
     #   spread1 = st.text_input('spread1')
    #with col4:
     #   spread2 = st.text_input('spread2')

   # with col1:
    #    D2 = st.text_input('D2')
    #with col2:
   #     PPE = st.text_input('PPE')

    # creating a button for Prediction

   # parkinsons_model = pickle.load(open(
    #    'parkinsons_model.sav', 'rb'))
   # if st.button("Parkinson's Test Result"):
      #  parkinsons_prediction = parkinsons_model.predict(
      #      [[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]])

      #  if (parkinsons_prediction[0] == 1):
    #        st.warning("The person has Parkinson's disease")
    #    else:
       #     st.success("The person does Not have Parkinson's disease")

#
#  Done
#

# Hepatitis Mortality Predictor Page


#def get_value(val, my_dict):
 #   for key, value in my_dict.items():
  #      if val == key:
   #         return value
#

#def get_key(val, my_dict):
 #   for key, value in my_dict.items():
  #      if val == key:
   #         return key


#def get_fvalue(val):
 #   feature_dict = {"No": 1, "Yes": 2}
  #  for key, value in feature_dict.items():
   #     if val == key:
    #        return value


#if (selected == 'Hepatitis Mortality Predictor'):
 #   st.title("Hepatitis Mortality Predictor")
  #  st.button("About", help="The Hepatitis Mortality Predictor App is a valuable tool designed to assess the risk of mortality in individuals with hepatitis. By inputting the patient's age, sex, steroid usage, antiviral treatment, presence of fatigue, spiders, ascites, varices, bilirubin levels, alkaline phosphatase levels, SGOT levels, albumin levels, prothrombin time, and histology data, the app utilizes advanced algorithms to generate a comprehensive analysis. It evaluates the collected information to provide an accurate prediction regarding the mortality risk associated with hepatitis. This empowers healthcare professionals to identify high-risk individuals, provide timely interventions, and optimize treatment strategies to improve patient outcomes and survival rates for individuals with hepatitis. DataSet Used : https://www.kaggle.com/datasets/codebreaker619/hepatitis-data")
   # image = Image.open('Hepatitis.jpg')
    #new_image = image.resize((800, 500))
    #st.image(new_image)
   # st.header("Just fill in the information below")
   # age = st.number_input("Age", 7, 80)
    #gender_dict = {"male": 1, "female": 2}
    #sex = st.radio("Sex", tuple(gender_dict.keys()))
 #   feature_dict = {"No": 1, "Yes": 2}
  #  steroid = st.radio("Do You Take Steroids?", tuple(feature_dict.keys()))
   # antivirals = st.radio("Do You Take Antivirals?",
    #                      tuple(feature_dict.keys()))
    #fatigue = st.radio("Do You Have Fatigue", tuple(feature_dict.keys()))
 #   spiders = st.radio("Presence of Spider Naeve", tuple(feature_dict.keys()))
 #   ascites = st.selectbox("Ascities", tuple(feature_dict.keys()))
 #   varices = st.selectbox("Presence of Varices", tuple(feature_dict.keys()))
 #   bilirubin = st.number_input("bilirubin Content", 0.0, 8.0)
 #   alk_phosphate = st.number_input("Alkaline Phosphate Content", 0.0, 296.0)
 #   sgot = st.number_input("Sgot", 0.0, 648.0)
 #   albumin = st.number_input("Albumin", 0.0, 6.4)
 #   protime = st.number_input("Prothrombin Time", 0.0, 100.0)
 #   histology = st.selectbox("Histology", tuple(feature_dict.keys()))

  #  feature_list = [age, get_value(sex, gender_dict), get_fvalue(steroid), get_fvalue(antivirals), get_fvalue(fatigue), get_fvalue(
   #     spiders), get_fvalue(ascites), get_fvalue(varices), bilirubin, alk_phosphate, sgot, albumin, int(protime), get_fvalue(histology)]

 #   pretty_result = {"age": age, "sex": sex, "steroid": steroid, "antivirals": antivirals, "fatigue": fatigue, "spiders": spiders, "ascites": ascites,
  #                   "varices": varices, "bilirubin": bilirubin, "alk_phosphate": alk_phosphate, "sgot": sgot, "albumin": albumin, "protime": protime, "histolog": histology}
 #   st.json(pretty_result)
  #  single_sample = np.array(feature_list).reshape(1, -1)

   # model_choice = "DecisionTree"
    #loaded_model = joblib.load(
     #   open('hepB_model.pkl', 'rb'))
 #   prediction = loaded_model.predict(single_sample)
  #  pred_prob = loaded_model.predict_proba(single_sample)

  #  if st.button("Predict"):
   #     prediction = loaded_model.predict(single_sample)
    #    pred_prob = loaded_model.predict_proba(single_sample)

     #   if prediction == 1:
      #      st.warning("Patient Dies")
       #     pred_probability_score = {
        #        "Die": pred_prob[0][0]*100, "Live": pred_prob[0][1]*100}
         #   st.subheader(
          #      "Prediction Probability Score using {}".format(model_choice))
           # st.json(pred_probability_score)
           # st.subheader("Prescriptive Analytics")

           # prescriptive_message_temp = """
	  #  <div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		#    <h3 style="text-align:justify;color:black;padding:10px">Recommended Life style modification</h3>
		 #   <ul>
		  #  <li style="text-align:justify;color:black;padding:10px">Exercise Daily</li>
		   # <li style="text-align:justify;color:black;padding:10px">Get Plenty of Rest</li>
#		    <li style="text-align:justify;color:black;padding:10px">Exercise Daily</li>
#		    <li style="text-align:justify;color:black;padding:10px">Avoid Alchol</li>
#		    <li style="text-align:justify;color:black;padding:10px">Proper diet</li>
#		    <ul>
#		    <h3 style="text-align:justify;color:black;padding:10px">Medical Mgmt</h3>
#		    <ul>
#		    <li style="text-align:justify;color:black;padding:10px">Consult your doctor</li>
#		    <li style="text-align:justify;color:black;padding:10px">Take your interferons</li>
#		    <li style="text-align:justify;color:black;padding:10px">Go for checkups</li>
#		    <ul>
#	    </div>
#	    """
 #           st.markdown(prescriptive_message_temp, unsafe_allow_html=True)
#
 #       else:
  #          st.success("Patient Lives")
   #         pred_probability_score = {
    #            "Die": pred_prob[0][0]*100, "Live": pred_prob[0][1]*100}
     #       st.subheader(
      #          "Prediction Probability Score using {}".format(model_choice))
       #     st.json(pred_probability_score)'''
# Malaria Disease Prediction Page
if (selected == 'Malaria Detector'):
    st.title('Malaria Detection')
    st.button("About", help="The malaria Detector Predictor App is an innovative tool designed to assist in the detection of malaria based on infection images. By uploading the patient's result images, the app utilizes advanced image recognition algorithms to analyze the presence of abnormalities indicative of malaria. It evaluates the image for signs such as infiltrates, consolidation, and lung opacities. The app provides a prediction regarding the likelihood of malaria, empowering healthcare professionals to make informed decisions and facilitate timely interventions. This app aids in improving the accuracy and efficiency of malaria diagnosis, leading to better patient outcomes and more effective treatment strategies. Dataset used : https://www.kaggle.com/datasets/iarunava/cell-images-for-detecting-malaria")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        # Preprocess the image
        def preprocess_image(image):
            img = image.resize((224, 224))
            img = np.asarray(img)
            img = img.reshape((1, 224, 224, 3))
            img = img.astype(np.float32) / 255.0
            return img

        # Load the pre-trained VGG19 model
        malaria_model = load_model('CNN_Model.h5')

        if st.button('Predict'):
            # Preprocess the uploaded image
            processed_image = preprocess_image(image)

            # Make prediction
            prediction = malaria_model.predict(processed_image)

            # Convert the prediction result to text
            if prediction[0][0] > 0.5:
                st.error('Infected with Malaria')
            else:
                st.success('Not infected with Malaria')
    

#
#  pretty well
#

# # Plant Diesease Detection Predictor Page

# def load_modell(path):

#     # Xception Model
#     xception_model = tf.keras.models.Sequential([
#         tf.keras.applications.xception.Xception(
#             include_top=False, weights='imagenet', input_shape=(512, 512, 3)),
#         tf.keras.layers.GlobalAveragePooling2D(),
#         tf.keras.layers.Dense(4, activation='softmax')
#     ])

#     # DenseNet Model
#     densenet_model = tf.keras.models.Sequential([
#         tf.keras.applications.densenet.DenseNet121(
#             include_top=False, weights='imagenet', input_shape=(512, 512, 3)),
#         tf.keras.layers.GlobalAveragePooling2D(),
#         tf.keras.layers.Dense(4, activation='softmax')
#     ])

#     # Ensembling the Models
#     inputs = tf.keras.Input(shape=(512, 512, 3))
#     xception_output = xception_model(inputs)
#     densenet_output = densenet_model(inputs)
#     outputs = tf.keras.layers.average([densenet_output, xception_output])
#     model = tf.keras.Model(inputs=inputs, outputs=outputs)

#     # Loading the Weights of Model
#     model.load_weights(path)
#     return model
# #


# def clean_image(image):
#     image = np.array(image)
#     image = np.array(Image.fromarray(
#         image).resize((512, 512), Image.ANTIALIAS))
#     image = image[np.newaxis, :, :, :3]
#     return image


# def get_prediction(model, image):
#     datagen = tf.keras.preprocessing.image.ImageDataGenerator(
#         rescale=1./255)
#     test = datagen.flow(image)
#     predictions = model.predict(test)
#     predictions_arr = np.array(np.argmax(predictions))
#     return predictions, predictions_arr


# def make_results(predictions, predictions_arr):
#     result = {}
#     if int(predictions_arr) == 0:
#         result = {"status": " is Healthy ",
#                   "prediction": f"{int(predictions[0][0].round(2)*100)}%"}
#     if int(predictions_arr) == 1:
#         result = {"status": ' has Multiple Diseases ',
#                   "prediction": f"{int(predictions[0][1].round(2)*100)}%"}
#     if int(predictions_arr) == 2:
#         result = {"status": ' has Rust ',
#                   "prediction": f"{int(predictions[0][2].round(2)*100)}%"}
#     if int(predictions_arr) == 3:
#         result = {"status": ' has Scab ',
#                   "prediction": f"{int(predictions[0][3].round(2)*100)}%"}
#     return result


# if (selected == "Plant Diesease Detection"):
#     model = load_modell('plant_disease.h5')
#     st.title('Plant Diesease Detection')
#     st.write(
#         "Just Upload your Plant's Leaf Image and get predictions if the plant is healthy or not")
#     filee = st.file_uploader("Choose a Image file", type=["png", "jpg"])
#     b = False
#     st.write("Take a photo")
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("start Camera"):
#             b = 0
#         else:
#             b = 1
#     with col2:
#         if st.button("stop Camera"):
#             b = 1
#         else:
#             b = 0

#     camera_photo = st.camera_input("", disabled=b)
#     if filee is None:
#         uploaded_file = camera_photo
#     else:
#         uploaded_file = filee
#     st.image(uploaded_file)

#     if uploaded_file != None:
#         progress = st.text("Crunching Image")
#         my_bar = st.progress(0)
#         i = 0

#         image = Image.open(io.BytesIO(uploaded_file.read()))
#         st.image(np.array(Image.fromarray(
#             np.array(image)).resize((700, 400), Image.ANTIALIAS)), width=None)
#         my_bar.progress(i + 40)

#         image = clean_image(image)
#         predictions, predictions_arr = get_prediction(model, image)
#         my_bar.progress(i + 30)
#         result = make_results(predictions, predictions_arr)

#         my_bar.progress(i + 30)
#         progress.empty()
#         i = 0
#         my_bar.empty()

#         st.write(
#             f"The plant {result['status']} with {result['prediction']} prediction.")

#
#  half
#



# React to user input


# Pneumonia Detector Prediction Page
if (selected == 'Pneumonia Detector'):
    st.title("Pneumonia Detector")
    st.button("About", help="The Pneumonia Detector Predictor App is an innovative tool designed to assist in the detection of pneumonia based on chest X-ray images. By uploading the patient's chest X-ray, the app utilizes advanced image recognition algorithms to analyze the presence of abnormalities indicative of pneumonia. It evaluates the X-ray image for signs such as infiltrates, consolidation, and lung opacities. The app provides a prediction regarding the likelihood of pneumonia, empowering healthcare professionals to make informed decisions and facilitate timely interventions. This app aids in improving the accuracy and efficiency of pneumonia diagnosis, leading to better patient outcomes and more effective treatment strategies. Dataset used : https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia")
    image = Image.open('Pneumonia-p.jpg')
    new_image = image.resize((800, 500))
    st.image(new_image)
    st.header("Load X-Ray Chest image")
    img = st.file_uploader(label="Click Browse Files and Upload", type=[
                           'jpeg', 'jpg', 'png'], key="xray")

    if img is not None:
        # Preprocessing Image
        i11 = Image.open(img).convert("RGB")
        p_img = i11.resize((224, 224))
        p_img = np.array(p_img) / 255.0

        if st.checkbox('Zoom image'):
            image = np.array(Image.open(img))
            st.image(image, use_column_width=True)
        else:
            st.image(p_img)

    # Loading model
        MODEL = "pneumonia_classifiers.h5"
        loading_msg = st.empty()
        loading_msg.text("Predicting...")
        model = keras.models.load_model(f"{MODEL}", compile=True)

    # Predicting result
        prediction = 1
        prob = model.predict(np.reshape(p_img, [1, 224, 224, 3]))
        prob = prob.reshape(1, -1)[0]
        if prob[0] > 0.5:
            prediction = True
        else:
            prediction = False
        loading_msg.text('')

        if prediction:
            st.warning("Pneumonia Detected! :slightly_frowning_face")
        else:
            st.success("No Pneumonia Detected, Healthy! :smile")

        st.text(f"Probability of Pneumonia is {round(prob[0] * 100, 2)}%")
class RiskFactorAssessment:
    def __init__(self):
        # Initialize risk factors and their corresponding scores
        self.risk_factors = {
            'smoking': 2,
            'alcohol': 2,
            'unhealthy_diet': 2,
            'physical_inactivity': 2,
            'high_blood_pressure': 3,
            'high_blood_sugar': 3,
            'high_cholesterol': 3,
            'overweight': 2,
            'family_history': 3
        }

    def assess_risk(self, user_factors):
        # Calculate the total risk score based on the user's factors
        total_score = sum(self.risk_factors[factor] for factor in user_factors if factor in self.risk_factors)

        # Determine the risk level based on the total score
        if total_score < 5:
            risk_level = 'Low'
        elif total_score < 10:
            risk_level = 'Medium'
        else:
            risk_level = 'High'

        return risk_level, total_score
if selected == 'Risk Factor Assessment':
    st.title("Risk Factor Assessment")
    
    # Create a new RiskFactorAssessment object
    assessment = RiskFactorAssessment()

    # Create checkboxes for each risk factor
    user_factors = []
    for factor in assessment.risk_factors:
        if st.checkbox(f"Do you have this risk factor? {factor}"):
            user_factors.append(factor)

    # Assess the risk if the user has input their factors
    if st.button("Assess Risk"):
        risk_level, total_score = assessment.assess_risk(user_factors)
        st.write(f"Risk Level: {risk_level}, Total Score: {total_score}")

# Q&A Chatbot
#from langchain.llms import OpenAI

import streamlit as st
import os
import textwrap

import google.generativeai as genai

# Disable Application Default Credentials (ADC) using environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

# Function to configure genai and get response (outside any function)
def configure_and_get_response(question):
  # Configure genai library with your API key (replace with actual key)
  genai.configure(api_key="AIzaSyAVU9zzaC9H9ZOUX0wBYqDchFkoznTkZBs")
  model = genai.GenerativeModel('gemini-pro')
  chat = model.start_chat(history=[])
  response = chat.send_message(question, stream=True)
  return response
##initialize our streamlit app

#st.set_page_config(page_title="Q&A Demo")

if selected == 'Help - ChatBot':
  st.header("Gemini Chatbot")
  input = st.text_input("Ask your question:", key="chat_input")

  if st.button("Ask"):
    # Call the function to configure genai and get response
    response = configure_and_get_response(input)
    st.subheader("The Response is:")
    for chunk in response:
      st.write(chunk.text)
    st.write("_" * 80)

  else:
    st.write("Type your question and hit Ask to chat with the AI.")
## If ask button is clicked


diabetes_model = joblib.load("models/diabetes_model.sav")

if selected == 'Diabetes Prediction':  # pagetitle
    st.title("Diabetes disease prediction")
    image = Image.open('d3.jpg')
    st.image(image, caption='diabetes disease prediction')
    # columns
    # no inputs from the user
    name = st.text_input("Name:")
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.number_input("Number of Pregnencies")
    with col2:
        Glucose = st.number_input("Glucose level")
    with col3:
        BloodPressure = st.number_input("Blood pressure  value")
    with col1:

        SkinThickness = st.number_input("Sckinthickness value")

    with col2:

        Insulin = st.number_input("Insulin value ")
    with col3:
        BMI = st.number_input("BMI value")
    with col1:
        DiabetesPedigreefunction = st.number_input(
            "Diabetespedigreefunction value")
    with col2:

        Age = st.number_input("AGE")

    # code for prediction
    diabetes_dig = ''

    # button
    if st.button("Diabetes test result"):
        diabetes_prediction=[[]]
        diabetes_prediction = diabetes_model.predict(
            [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreefunction, Age]])

        # after the prediction is done if the value in the list at index is 0 is 1 then the person is diabetic
        if diabetes_prediction[0] == 1:
            diabetes_dig = "we are really sorry to say but it seems like you are Diabetic."
            image = Image.open('positive.jpg')
            st.image(image, caption='')
        else:
            diabetes_dig = 'Congratulation,You are not diabetic'
            image = Image.open('negative.jpg')
            st.image(image, caption='')
        st.success(name+' , ' + diabetes_dig)
        


parkinson_model = joblib.load("models/parkinsons_model.sav")
if selected == 'Parkison Prediction':
    st.title("Parkison prediction")
    image = Image.open('p1.jpg')
    st.image(image, caption='parkinsons disease')
  # parameters
#    name	MDVP:Fo(Hz)	MDVP:Fhi(Hz)	MDVP:Flo(Hz)	MDVP:Jitter(%)	MDVP:Jitter(Abs)	MDVP:RAP	MDVP:PPQ	Jitter:DDP	MDVP:Shimmer	MDVP:Shimmer(dB)	Shimmer:APQ3	Shimmer:APQ5	MDVP:APQ	Shimmer:DDA	NHR	HNR	status	RPDE	DFA	spread1	spread2	D2	PPE
   # change the variables according to the dataset used in the model
    name = st.text_input("Name:")
    col1, col2, col3 = st.columns(3)
    with col1:
        MDVP = st.number_input("MDVP:Fo(Hz)")
    with col2:
        MDVPFIZ = st.number_input("MDVP:Fhi(Hz)")
    with col3:
        MDVPFLO = st.number_input("MDVP:Flo(Hz)")
    with col1:
        MDVPJITTER = st.number_input("MDVP:Jitter(%)")
    with col2:
        MDVPJitterAbs = st.number_input("MDVP:Jitter(Abs)")
    with col3:
        MDVPRAP = st.number_input("MDVP:RAP")

    with col2:

        MDVPPPQ = st.number_input("MDVP:PPQ ")
    with col3:
        JitterDDP = st.number_input("Jitter:DDP")
    with col1:
        MDVPShimmer = st.number_input("MDVP:Shimmer")
    with col2:
        MDVPShimmer_dB = st.number_input("MDVP:Shimmer(dB)")
    with col3:
        Shimmer_APQ3 = st.number_input("Shimmer:APQ3")
    with col1:
        ShimmerAPQ5 = st.number_input("Shimmer:APQ5")
    with col2:
        MDVP_APQ = st.number_input("MDVP:APQ")
    with col3:
        ShimmerDDA = st.number_input("Shimmer:DDA")
    with col1:
        NHR = st.number_input("NHR")
    with col2:
        HNR = st.number_input("HNR")
  
    with col2:
        RPDE = st.number_input("RPDE")
    with col3:
        DFA = st.number_input("DFA")
    with col1:
        spread1 = st.number_input("spread1")
    with col1:
        spread2 = st.number_input("spread2")
    with col3:
        D2 = st.number_input("D2")
    with col1:
        PPE = st.number_input("PPE")

    # code for prediction
    parkinson_dig = ''
    
    # button
    if st.button("Parkinson test result"):
        parkinson_prediction=[[]]
        # change the parameters according to the model
        parkinson_prediction = parkinson_model.predict([[MDVP, MDVPFIZ, MDVPFLO, MDVPJITTER, MDVPJitterAbs, MDVPRAP, MDVPPPQ, JitterDDP, MDVPShimmer,MDVPShimmer_dB, Shimmer_APQ3, ShimmerAPQ5, MDVP_APQ, ShimmerDDA, NHR, HNR,  RPDE, DFA, spread1, spread2, D2, PPE]])

        if parkinson_prediction[0] == 1:
            parkinson_dig = 'we are really sorry to say but it seems like you have Parkinson disease'
            image = Image.open('positive.jpg')
            st.image(image, caption='')
        else:
            parkinson_dig = "Congratulation , You don't have Parkinson disease"
            image = Image.open('negative.jpg')
            st.image(image, caption='')
        st.success(name+' , ' + parkinson_dig)
