try:
    import paho.mqtt.client as mqtt
except:
    os.system("pip3 install paho-mqtt")
    import paho.mqtt.client as mqtt

try:
    import pandas as pd
except:
    os.system("pip3 install pandas")
    import pandas as pd

data = []
df = pd.DataFrame(columns=["temperature", "humidity"])
temperature = []
humidity = []

def on_connect(client, userdata, flags, rc):
    print("Connected to broker")

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    if "temperature" in msg.topic:
        temperature.append(data)
    elif "humidity" in msg.topic:
        humidity.append(data)
    
    if len(humidity) == len(temperature):
        auxiliar_df = pd.DataFrame({"temperature": temperature, "humidity": humidity})
        auxiliar_df.to_csv("almacenamiento.csv")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("172.20.10.4", 1883, 60)
client.subscribe("room/temperature")
client.subscribe("room/humidity")
client.loop_forever()