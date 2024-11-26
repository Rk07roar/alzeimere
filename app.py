from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For session management

# Hardcoded user credentials (replace with a database in production)
users = {"admin": "password123"}

@app.route('/')
def home():
    # If the user is not logged in, redirect them to the sign-in page (disease_info.html)
    if 'username' not in session:
        return redirect(url_for('signin'))
    return render_template('index.html')  # Display the risk prediction form (index.html)

@app.route('/disease_info', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('home'))  # Redirect to index.html after sign-in
        else:
            return render_template('disease_info.html', error="Invalid credentials. Please try again.")
    
    return render_template('disease_info.html')

@app.route('/signout')
def signout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('signin'))

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        systolic_bp = int(request.form['systolicbp'])
        diastolic_bp = int(request.form['diastolicbp'])
        cholesterol_total = int(request.form['cholesteroltotal'])
        cholesterol_ldl = int(request.form['cholesterolldl'])
        cholesterol_hdl = int(request.form['cholesterolhdl'])
        cholesterol_triglycerides = int(request.form['cholesteroltriglycerides'])
        mmse = int(request.form['mmse'])
        functional_assessment = int(request.form['functionalassessment'])
        adl = int(request.form['adl'])
        confusion = request.form['confusion']
        disorientation = request.form['disorientation']
        personality_changes = request.form['personalitychanges']
        difficulty_completing_tasks = request.form['difficultycompletingtasks']
        forgetfulness = request.form['forgetfulness']
        
        risk_percentage = 0

        # Health checks for risk calculation
        if age > 65:
            risk_percentage += 15
        if bmi > 30:
            risk_percentage += 10
        if systolic_bp > 140 or diastolic_bp > 90:
            risk_percentage += 20
        if cholesterol_total > 240 or cholesterol_ldl > 160:
            risk_percentage += 15
        if mmse < 24:
            risk_percentage += 20
        if functional_assessment > 2 or adl > 2:
            risk_percentage += 10
        if confusion.lower() == 'yes' or disorientation.lower() == 'yes' or personality_changes.lower() == 'yes':
            risk_percentage += 25
        if difficulty_completing_tasks.lower() == 'yes' or forgetfulness.lower() == 'yes':
            risk_percentage += 25

        risk_percentage = min(risk_percentage, 100)

        if risk_percentage > 70:
            risk_level = "High Risk"
        elif risk_percentage > 40:
            risk_level = "Moderate Risk"
        else:
            risk_level = "Low Risk"

        if risk_level == "High Risk":
            precautions = "Consult a healthcare provider for further assessment and explore options for lifestyle changes, medication, and monitoring."
        elif risk_level == "Moderate Risk":
            precautions = "Maintain a healthy lifestyle, including regular physical activity, healthy eating, and mental exercises."
        else:
            precautions = "Continue to monitor your health, and engage in activities that support cognitive health, such as reading or puzzles."

        return render_template('result.html', name=name, risk_level=risk_level, risk_percentage=risk_percentage, precautions=precautions)

if __name__ == '__main__':
    app.run(debug=True)
