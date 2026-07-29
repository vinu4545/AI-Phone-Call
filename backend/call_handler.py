import sys
import time 
from backend.config.config import ESL_PATH

# Add the FreeSWITCH ESL Python module path
sys.path.insert(0, str(ESL_PATH))

from ESL import ESLconnection


class CallHandler:
    def __init__(self, request):
        self.fd = request.fileno()
        self.con = ESLconnection(self.fd)

    def handle(self):
        print("=" * 60)

        print("Connected:", self.con.connected())

        if not self.con.connected():
            print("Failed to establish ESL connection.")
            return

        info = self.con.getInfo()

        print("\n===== CHANNEL INFO =====")

        headers = [
            "unique-id",
            "caller-caller-id-number",
            "caller-caller-id-name",
            "caller-destination-number",
            "channel-name",
        ]

        for header in headers:
            print(f"{header:28}: {info.getHeader(header)}")

        print("========================")

        print("\nAnswering call...")

        reply = self.con.execute("answer")

        print("Answer reply:", reply)
        wav_file = "/home/vinay-gaddam/Documents/Orbit_Services/AI-Phone-Call/recordings/hello.wav"
        reply = self.con.execute(
            "playback",
            wav_file
        )
        print("Playback reply:", reply)

        # print("\nEntering event loop...\n")

        # counter = 0

        # while True:

        #     connected = self.con.connected()

        #     print(f"[{counter}] connected = {connected}")

        #     if not connected:
        #         print("\nESL connection has been closed.")
        #         break

        #     event = self.con.recvEventTimed(1000)

        #     if event:
        #         event_name = event.getHeader("Event-Name")
        #         print(f"[{counter}] Event: {event_name}")

        #         if event_name == "CHANNEL_HANGUP":
        #             print("\nCaller hung up.")
        #             break

        #     else:
        #         print(f"[{counter}] No event received.")

        #     counter += 1

        print("Sleeping...")

        time.sleep(120)

        print("Done sleeping")

        print("\nCall session ended.")