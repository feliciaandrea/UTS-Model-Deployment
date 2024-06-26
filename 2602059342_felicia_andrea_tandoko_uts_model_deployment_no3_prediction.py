import streamlit as st
import joblib
import numpy as np
import pandas as pd

model = joblib.load('XGBoost.pkl')
gender_encode = joblib.load('gender_encode.pkl')
geography_encode = joblib.load('geography_encodee.pkl')
scaling = joblib.load('scaling.pkl')

def make_prediction(features):
    input_array = np.array(features).reshape(1,-1)
    prediction = model.predict(input_array)
    return prediction[0]

def main():
    st.title('Churn Classification Model')
    st.write('Enter customer information')

    Age = st.slider('Age', 0, 100, 25)
    Gender = st.selectbox('Gender', ['Male', 'Female'])
    Geography = st.selectbox('Geography', ['France', 'Germany', 'Spain'])
    EstimatedSalary = st.number_input('Estimated Salary', value=0.0)
    Tenure = st.slider('Tenure', 0, 10, 5)
    HasCrCard = st.selectbox('Has Credit Card', ['Yes', 'No'])
    IsActiveMember = st.selectbox('Is Active Member', ['Yes', 'No'])
    Balance = st.number_input('Balance', value=0.0)
    CreditScore = st.slider('Credit Score', 300, 850, 500)
    NumOfProducts = st.slider('Number of Products', 1, 4, 1)

    HasCrCard = 1 if HasCrCard == 'Yes' else 0
    IsActiveMember = 1 if IsActiveMember == 'Yes' else 0

    data = {'Credit Score': CreditScore, 'Age': Age, 'Tenure': Tenure,
            'Balance': Balance, 'Num Of Products': NumOfProducts,
            'HasCrCard': HasCrCard, 'IsActiveMember': IsActiveMember,
            'Estimated Salary': EstimatedSalary, 'Gender': Gender, 'Geography': Geography}

    df=pd.DataFrame([list(data.values())], columns=['Credit Score', 'Age', 'Tenure', 'Balance',
                                                    'Num Of Products', 'Has Cr Card', 'Is Active Member',
                                                    'Estimated Salary', 'Gender', 'Geography'])

    df = df.replace(gender_encode)
    geo = df[['Geography']]
    geo_encode = pd.DataFrame(geography_encode.transform(geo).toarray(),columns=geography_encode.get_feature_names_out())
    df = pd.concat([df, geo_encode], axis=1)
    df = df.drop('Geography', axis=1)

    if st.button('Make Prediction'):
      prediction = make_prediction(df)
      if prediction == 1:
          st.write('The customer is likely to churn')
      else:
          st.write('The customer is not likely to churn')

if __name__ == "__main__":
    main()
