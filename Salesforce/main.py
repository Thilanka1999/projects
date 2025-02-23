from bot.bot import process
from bot.slack_client import slack_client
from threading import Event


if __name__ == "__main__":
    print("Starting Slack bot...")
    slack_client.socket_mode_request_listeners.append(process)
    slack_client.connect()
    
    print("Listening for messages...")
    Event().wait()