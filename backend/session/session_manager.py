import logging
from threading import Lock


logger = logging.getLogger(__name__)


class SessionManager:

    def __init__(self):

        self._sessions = {}

        self._lock = Lock()

    # ====================================================
    # Create
    # ====================================================

    def create(self, call_uuid):

        with self._lock:

            if call_uuid in self._sessions:
                logger.warning(
                    "Session already exists: %s",
                    call_uuid
                )
                return self._sessions[call_uuid]

            session = {
                "uuid": call_uuid,
                "esl": None,
                "media": None,
            }

            self._sessions[call_uuid] = session

            logger.info(
                "Created session %s",
                call_uuid
            )

            return session

    # ====================================================
    # Lookup
    # ====================================================

    def get(self, call_uuid):

        with self._lock:
            return self._sessions.get(call_uuid)

    # ====================================================
    # ESL
    # ====================================================

    def attach_esl(
        self,
        call_uuid,
        esl_connection
    ):

        with self._lock:

            session = self._sessions.get(call_uuid)

            if session is None:
                raise KeyError(call_uuid)

            session["esl"] = esl_connection

            logger.info(
                "ESL attached to %s",
                call_uuid
            )

    # ====================================================
    # Media
    # ====================================================

    def attach_media(
        self,
        call_uuid,
        media_session
    ):

        with self._lock:

            session = self._sessions.get(call_uuid)

            if session is None:
                raise KeyError(call_uuid)

            session["media"] = media_session

            logger.info(
                "Media attached to %s",
                call_uuid
            )

    # ====================================================
    # Remove
    # ====================================================

    def remove(self, call_uuid):

        with self._lock:

            if call_uuid in self._sessions:

                del self._sessions[call_uuid]

                logger.info(
                    "Removed session %s",
                    call_uuid
                )

    # ====================================================
    # Count
    # ====================================================

    def active_sessions(self):

        with self._lock:
            return len(self._sessions)


session_manager = SessionManager()