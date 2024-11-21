from flask import Flask, request, render_template

app = Flask(__name__, template_folder='.')

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/submit-car', methods=['POST'])
def submit_car():
    title = request.form.get('title')
    instructions = request.form.get('instructions')
    car_manufacturer = request.form.get('carManufacturer')
    custom_manufacturer = request.form.get('customManufacturer')

    # Log or process the form data
    print(f"Title: {title}")
    print(f"Instructions: {instructions}")
    print(f"Car Manufacturer: {car_manufacturer}")
    if custom_manufacturer:
        print(f"Custom Manufacturer: {custom_manufacturer}")

    # Here you can process the form data or store it in a database
    return f"Form submitted successfully! Title: {title}, Manufacturer: {car_manufacturer}"

@app.route('/submit-car', methods=['GET'])
def submit_car_o():
    return render_template('skusam select filter 7.html')

if __name__ == '__main__':
    app.run(debug=True)
