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

        uuid = info.getHeader("unique-id")

        print("\nUUID:", uuid)

        print("\nAnswering call...")

        reply = self.con.execute("answer")

        print("Answer reply:", reply)

        command = (
            f"{uuid} "
            f"start "
            f"ws://127.0.0.1:9000 "
            f"mono "
            f"8000"
        )

        print("\nExecuting API:")
        print("uuid_audio_stream", command)

        try:

            reply = self.con.api(
                f"uuid_audio_stream {command}"
            )

            print("\nAPI reply:")
            print(reply)

        except Exception as e:

            print("\nAPI exception:")
            print(e)

        print("\nSleeping for 120 seconds...")

        time.sleep(120)

        print("\nDone.")