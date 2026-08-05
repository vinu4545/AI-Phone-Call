# import asyncio
# import logging

# from websockets.exceptions import ConnectionClosed
# from backend.media.media_session import MediaSession


# logger = logging.getLogger(__name__)


# class AudioSender:

#     FRAME_DURATION = 0.02      # 20 ms

#     def __init__(self, session: MediaSession):

#         self.session = session

#     async def start(self):

#         logger.info("AudioSender Started")

#         websocket = self.session.websocket

#         try:

#             while self.session.running:

#                 pcm = await self.session.get_outgoing_audio()

#                 if pcm is None:
#                     continue

#                 await websocket.send(pcm)

#                 logger.info(
#                     "Sender -> %d bytes",
#                     len(pcm)
#                 )

#                 #
#                 # IMPORTANT
#                 # Stream at real-time speed.
#                 #
#                 await asyncio.sleep(self.FRAME_DURATION)

#         except ConnectionClosed:

#             logger.info("Sender WebSocket Closed")

#         except Exception:

#             logger.exception("AudioSender crashed")

#         finally:

#             logger.info("AudioSender Stopped")