from flask import Flask, request, render_template

app = Flask(__name__, template_folder='.')

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/submit-car', methods=['POST'])
def submit_car():
    title = request.form.get('title')
    instructions = request.form.get('instructions')
    
    # Collect all car manufacturers and custom manufacturers
    car_manufacturers = request.form.getlist('carManufacturer[]')
    custom_manufacturers = request.form.getlist('customManufacturer[]')

    # Print out the submitted values for logging or further processing
    print(f"Title: {title}")
    print(f"Instructions: {instructions}")
    print(f"Car Manufacturers: {car_manufacturers}")
    
    for manufacturer in car_manufacturers:
        if manufacturer == 'Other':
            # Find the corresponding custom manufacturer input if needed
            index = car_manufacturers.index(manufacturer)
            print(f"Custom Manufacturer: {custom_manufacturers[index]}")

    return f"Form submitted successfully! Title: {title}, Manufacturers: {car_manufacturers}"


@app.route('/submit-car', methods=['GET'])
def submit_car_o():
    return render_template('skusam select filter 10.html')

if __name__ == '__main__':
    app.run(debug=True)
