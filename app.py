from flask import Flask , render_template ,request,jsonify
import pickle
import numpy as np
import pandas as pd
import io


model_f = None
with open('RandomForestModel.pkl', 'rb') as f:
    model_f = pickle.load(f)
# Load the Trained ML model 
#model=pickle.load(open("RandomForestModel.pkl","rb"))

#intialize flask app
app=Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict',methods=['POST'])
def predict():
    try:
        #data = request.data  # Assuming the raw bytes are sent directly

        # Use BytesIO to simulate a file-like object from bytes
        model_file = io.BytesIO(model_f)

        # Load the model from the byte stream
        model = pickle.load(model_file)
        #get input data from form
        data=request.form
        # extract data from form and convert it into a dataframe
        age=float(data['age'])
        gender=int(data['gender'])
        education=int(data['education'])
        experience=float(data['experience'])
        
        # one-hot encoding for job roles(intialize all as False)
        job_roles=['Job Title_Back end Developer', 'Job Title_Content Marketing Manager', 'Job Title_Data Analyst', 'Job Title_Data Scientist', 'Job Title_Digital Marketing Manager', 'Job Title_Director of Data Science', 'Job Title_Director of HR', 'Job Title_Director of Marketing', 'Job Title_Financial Analyst', 'Job Title_Financial Manager', 'Job Title_Front End Developer', 'Job Title_Front end Developer', 'Job Title_Full Stack Engineer', 'Job Title_Human Resources Coordinator', 'Job Title_Human Resources Manager', 'Job Title_Junior HR Coordinator', 'Job Title_Junior HR Generalist', 'Job Title_Junior Marketing Manager', 'Job Title_Junior Sales Associate', 'Job Title_Junior Sales Representative', 'Job Title_Junior Software Developer', 'Job Title_Junior Software Engineer', 'Job Title_Junior Web Developer', 'Job Title_Marketing Analyst', 'Job Title_Marketing Coordinator', 'Job Title_Marketing Director', 'Job Title_Marketing Manager', 'Job Title_Operations Manager', 'Job Title_Product Designer', 'Job Title_Product Manager', 'Job Title_Receptionist', 'Job Title_Research Director', 'Job Title_Research Scientist', 'Job Title_Sales Associate', 'Job Title_Sales Director', 'Job Title_Sales Executive', 'Job Title_Sales Manager', 'Job Title_Sales Representative', 'Job Title_Senior Data Scientist', 'Job Title_Senior HR Generalist', 'Job Title_Senior Human Resources Manager', 'Job Title_Senior Product Marketing Manager', 'Job Title_Senior Project Engineer', 'Job Title_Senior Research Scientist', 'Job Title_Senior Software Engineer', 'Job Title_Software Developer', 'Job Title_Software Engineer', 'Job Title_Software Engineer Manager', 'Job Title_Web Developer']

        job_selected = data['job_role']
        
        if job_selected not in job_roles:
            return jsonify({'error': 'Invalid job role'})
        job_data = [True if job == job_selected else False for job in job_roles]
       
        # Combine all inputs into a single array
        input_data = [age, gender, education, experience] + job_data

        # Convert to numpy array
        input_array = np.array([input_data]).reshape(1, -1)
    
        # Predict salary
        prediction = model.predict(input_array)[0]
       
        return jsonify({'predicted_salary': round(prediction, 2)})
    
    except Exception as e:
        return jsonify({'error': str(e)})

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
