import os
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient

slack_app_token = os.environ.get("SLACK_APP_TOKEN")
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")


slack_client = SocketModeClient(
    app_token=slack_app_token,
    web_client=WebClient(token=slack_bot_token),
)
