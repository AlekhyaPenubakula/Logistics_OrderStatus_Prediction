from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)


model_path = r'model_k.pkl'
model = pickle.load(open(model_path, "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        
        input_df = pd.DataFrame([{
            'ShipmentMode': int(request.form['ShipmentMode']),
            'ProductCategory': int(request.form['ProductCategory']),
            'Quantity': float(request.form['Quantity']),
            'OrderToShipmentDays': int(request.form['OrderToShipmentDays']),
            'ShipmentToDeliveryDays': int(request.form['ShipmentToDeliveryDays']),
            'OrderToDeliveryDays': int(request.form['OrderToDeliveryDays']),
            'UnitPrice': float(request.form['UnitPrice']),
            'Discount': float(request.form['Discount']),
            'ShippingCost': float(request.form['ShippingCost']),
            'DeliveryTimeDays': float(request.form['DeliveryTimeDays'])
        }])

    
        prediction = model.predict(input_df)[0]

        
        if prediction == 2:
            result = "Returned"
        elif prediction == 1:
            result = "Shipped"
        else:
            result = "Cancelled"
        
        return render_template('submit.html', Result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
