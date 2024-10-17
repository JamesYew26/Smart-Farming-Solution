import grovepi
import time

# Define the digital port where the relay is connected
RELAY_PORT = 6

# Set the relay port as an output
grovepi.pinMode(RELAY_PORT, "OUTPUT")

def activate_pump(duration=5):
    try:
        # Turn on the relay (and pump)
        print("Activating pump...")
        grovepi.digitalWrite(RELAY_PORT, 1)  # Relay is activated
        time.sleep(duration)  # Keep the pump on for the specified duration
        
        # Turn off the relay (and pump)
        print("Deactivating pump...")
        grovepi.digitalWrite(RELAY_PORT, 0)  # Relay is deactivated
    except KeyboardInterrupt:
        print("Operation interrupted.")
    finally:
        # Ensure the relay is turned off when exiting
        grovepi.digitalWrite(RELAY_PORT, 0)
        print("Cleanup complete.")

# Example usage: Activate the pump for 5 seconds
activate_pump(duration=5)
