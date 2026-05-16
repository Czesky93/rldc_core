"""Telegram notifier integration stub.

This module defines a simple TelegramNotifier class used to send messages
to a configured Telegram chat. In the current stub implementation the
messages are printed to stdout instead of actually being sent. To enable
real messaging you could integrate with the python-telegram-bot library or
invoke Telegram's Bot API directly. Keeping this logic in a separate
module decouples the rest of the application from the messaging layer and
makes it easy to substitute a different notifier in the future.
"""

from typing import Optional
import logging


logger = logging.getLogger(__name__)


class TelegramNotifier:
    """A simple notifier that sends messages to Telegram.

    Parameters
    ----------
    token: Optional[str]
        Bot token for authenticating with the Telegram API. If not
        provided, messages will be logged/printed instead of sent.
    chat_id: Optional[str]
        Target chat ID. Required for real messaging.
    """

    def __init__(self, token: Optional[str] = None, chat_id: Optional[str] = None) -> None:
        self.token = token
        self.chat_id = chat_id
        self.enabled = bool(token and chat_id)

    def send_message(self, message: str) -> None:
        """Send a message to Telegram or log it if not enabled.

        Parameters
        ----------
        message: str
            The text message to send.

        Returns
        -------
        None
        """
        if self.enabled:
            # In a real implementation use requests or a Telegram bot library to
            # POST the message to the Bot API endpoint.
            try:
                import requests  # Optional dependency
                url = f"https://api.telegram.org/bot{self.token}/sendMessage"
                data = {"chat_id": self.chat_id, "text": message}
                resp = requests.post(url, data=data, timeout=10)
                resp.raise_for_status()
                logger.info("Sent Telegram message: %s", message)
            except Exception as e:
                logger.error("Failed to send Telegram message: %s", e)
        else:
            # When disabled we simply log the message and print to stdout for visibility
            logger.info("Telegram message: %s", message)
            print(f"[Telegram] {message}")