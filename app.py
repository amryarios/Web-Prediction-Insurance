from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model_file = open('model_uas.pkl', 'rb')
model = pickle.load(model_file, encoding='bytes')

@app.route('/')
def index():
    return render_template('index.html', charges=0)

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Predict the insurance cost based on user inputs
    and render the result to the html page
    '''
    age, sex, bmi, children, smoker, = [x for x in request.form.values()]

    data = []

    data.append(int(age))
    if sex == 'Laki-Laki':
        data.extend([0, 1])
    else:
        data.extend([1, 0])

    data.append(int(bmi))
    data.append(int(children))

    if smoker == 'Ya':
        data.extend([0, 1])
    else:
        data.extend([1, 0])
    
    prediction = model.predict([data])
    output = round(prediction[0], 2)

    return render_template('index.html', charges=output, age=age, sex=sex, bmi=bmi, children=children, smoker=smoker)


if __name__ == '__main__':
    app.run(debug=True)
