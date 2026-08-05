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

            print(
                f"{header:28}: {info.getHeader(header)}"
            )

        print("========================")

        uuid = info.getHeader("unique-id")

        print("\nUUID:", uuid)

        print("\nAnswering call...")

        reply = self.con.execute("answer")

        print("Answer reply:", reply)

        #
        # Give FreeSWITCH a moment after answering.
        #
        time.sleep(0.5)

        command = (
            f"{uuid} "
            f"start "
            f"ws://127.0.0.1:9000 "
            f"mono "
            f"8000"
        )

        print("\n============================================================")
        print("Starting Audio Stream")
        print("============================================================")
        print(command)

        try:

            reply = self.con.api(
                f"uuid_audio_stream {command}"
            )

            print("\n============================================================")
            print("API OBJECT")
            print("============================================================")
            print(reply)

            #
            # Actual API body
            #
            try:

                print("\n============================================================")
                print("API BODY")
                print("============================================================")
                print(reply.getBody())

            except Exception as e:

                print("getBody() failed:", e)

            #
            # Entire serialized event
            #
            try:

                print("\n============================================================")
                print("SERIALIZED EVENT")
                print("============================================================")
                print(reply.serialize())

            except Exception as e:

                print("serialize() failed:", e)

        except Exception as e:

            print("\nAPI Exception")
            print(e)

        #
        # Check channel every 5 seconds.
        #
        for i in range(24):

            exists = self.con.api(
                f"uuid_exists {uuid}"
            )

            print(
                f"[{i * 5:03d}s] uuid_exists ->",
                exists.getBody()
            )

            time.sleep(5)

        print("\nDone.")