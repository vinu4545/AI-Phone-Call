import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from esl.esl_client import ESLClient

client = ESLClient()

client.connect()

client.send("event plain ALL")

print(client.receive())

print("Waiting for events...")

while True:

    data = client.receive()

    print(data)