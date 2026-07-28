from pathlib import Path

# FreeSWITCH
FS_HOST = "127.0.0.1"
FS_PORT = 8021
FS_PASSWORD = "ClueCon"

# Outbound ESL Server
OUTBOUND_HOST = "127.0.0.1"
OUTBOUND_PORT = 8084

# FreeSWITCH Python ESL bindings
ESL_PATH = Path.home() / "freeswitch" / "libs" / "esl" / "python3"

# Greeting audio
HELLO_WAV = Path(__file__).resolve().parent.parent / "audio" / "hello.wav"

# AI_EXTENSION = "9999"