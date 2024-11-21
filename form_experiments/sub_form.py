from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='.')

@app.route('/submit-car', methods=['POST'])
def submit_car():
    try:
        # Get the car manufacturer from the request body (JSON)
        print(f"idem ziskat data")
        data = request.get_json()

        # Check if 'carManufacturer' is provided in the request
        car_manufacturer = data.get('carManufacturer')

        print(f"Car manufacturer: {car_manufacturer}")

        if not car_manufacturer:
            return jsonify({"message": "Car manufacturer is required."}), 400

        # You can now process the car manufacturer (e.g., store it in a database)
        # For this example, we just print it
        print(f"Received car manufacturer: {car_manufacturer}")

        # Respond back with a success message
        return jsonify({"message": "Car manufacturer received successfully!", "car": car_manufacturer}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@app.route('/submit-car', methods=['GET'])
def submit_car_o():
    return render_template('skusam select filter 6.html')

if __name__ == '__main__':
    app.run(debug=True)
