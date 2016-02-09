from docker import Client
import json

client = Client()

filters = {
    'event': ['start', 'restart', 'die', 'stop'],
    'type': 'container'
}

for event in client.events(filters=filters):
    data = json.loads(event)
