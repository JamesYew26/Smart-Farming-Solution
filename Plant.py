from time import sleep
from grovepi import *
from grove_rgb_lcd import *
from pyrebase import pyrebase
from datetime import datetime

# Sensor and relay setup
relay = 6
moisture_sensor = 14
light_sensor = 15
dht_sensor = 16

# Configure GPIO modes
pinMode(moisture_sensor, "INPUT")
pinMode(light_sensor, "INPUT")
pinMode(dht_sensor, "INPUT")
pinMode(relay, "OUTPUT")

# Firebase configuration
config = {
    "apiKey": "AIzaSyDSVKWrU1Eqn0-C8BoJOXIKZGm11UcuFsQ",
    "authDomain": "iot-firebase-df0be.firebaseapp.com",
    "databaseURL": "https://iot-firebase-df0be-default-rtdb.asia-southeast1.firebasedatabase.app",
    "storageBucket": "iot-firebase-df0be.appspot.com"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("junchee0206@gmail.com", "JunChee26_")
db = firebase.database()

# Function to validate sensor readings
def validate_readings(temperature, humidity, light, moisture):
    # Temperature should be between -40°C and 80°C
    if not (-40 <= temperature <= 80):
        print("Invalid temperature reading:", temperature)
        return False
    
    # Humidity should be between 0% and 100%
    if not (0 <= humidity <= 100):
        print("Invalid humidity reading:", humidity)
        return False
    
    # Light and moisture should be within the range of 0 to 1023
    if not (0 <= light <= 1023):
        print("Invalid light reading:", light)
        return False
    
    if not (0 <= moisture <= 1023):
        print("Invalid moisture reading:", moisture)
        return False
    
    return True

# Function to check if the temperature is suitable for the plant
def check_temperature(temperature):
    # Define the optimal temperature range for the plant (e.g., 15°C to 30°C)
    if temperature < 15:
        print("Warning: Temperature is too low for the plant!")
        setText("Temp too low!")
        setRGB(0, 0, 255)  # Set the LCD color to blue
    elif temperature > 30:
        print("Warning: Temperature is too high for the plant!")
        setText("Temp too high!")
        setRGB(255, 0, 0)  # Set the LCD color to red
    else:
        print("Temperature is within the ideal range for the plant.")
        setText(f"Temp: {temperature:.2f}°C")
        setRGB(137, 207, 240)  # Set the LCD to a neutral color

# Function to determine soil moisture status
def check_soil_moisture(moisture):
    # Define thresholds for soil moisture levels
    if moisture < 300:
        print("Soil is very dry. Activating the pump...")
        digitalWrite(relay, 1)  # Turn on the pump
        sleep(2)                # Pump runs for 2 seconds
        digitalWrite(relay, 0)  # Turn off the pump
    elif 300 <= moisture < 600:
        print("Soil is dry, consider watering.")
    elif 600 <= moisture < 800:
        print("Soil is moderately moist.")
    else:
        print("Soil is wet, no watering needed.")

# Main loop
while True:
    try:
        # Delay to avoid too frequent readings
        sleep(30)

        # Read sensor values
        moisture = analogRead(moisture_sensor)
        [temperature, humidity] = dht(dht_sensor, 0)
        light = analogRead(light_sensor)

        # Validate sensor readings
        if validate_readings(temperature, humidity, light, moisture):
            # Display readings
            print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity}%, Light: {light}, Moisture: {moisture}")

            # Check temperature and display appropriate message
            check_temperature(temperature)

            # Check soil moisture and control the pump if necessary
            check_soil_moisture(moisture)

            # Prepare data for Firebase
            timestamp = datetime.now().isoformat()
            data = {
                "Temperature": str(temperature),
                "Humidity": str(humidity),
                "Moisture": moisture,
                "Light": light,
                "Time": timestamp
            }

            # Update data in Firebase
            db.child("Plant").push(data)

            # Update the LCD with the time
            print("On going...")

        else:
            print("Invalid sensor readings, skipping update.")

    except KeyboardInterrupt:
        # Handle exit
        setText("Program exited")
        break
    except TypeError:
        print("Type error occurred")
    except IOError:
        print("IO Error occurred")
