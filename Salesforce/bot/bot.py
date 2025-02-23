
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode import SocketModeClient
import json

from bot.llm_parser import extract_function_using_llm
from bot.functions import salesforce_function_mapper

def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        # Acknowledge the request
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        event = req.payload["event"]
        channel = event["channel"]
        user_id = event.get("user")

        # Get bot's user ID
        bot_user_id = client.web_client.auth_test()["user_id"]

        # Ignore messages from the bot itself (to avoid looping)
        if user_id == bot_user_id:
            return

        # Check if the event is a message
        if event["type"] == "message" and event.get("subtype") is None:
            message = event["text"]

            # Use LLM to extract Salesforce operation and arguments
            operation, object_name, args = extract_function_using_llm(message)

            if operation and operation in salesforce_function_mapper:
                try:
                    # Execute the Salesforce operation
                    if operation == "query":
                        result = salesforce_function_mapper[operation](args["query"])
                    elif operation == "insert":
                        result = salesforce_function_mapper[operation](object_name, args["data"])
                    elif operation == "update":
                        result = salesforce_function_mapper[operation](object_name, args["record_id"], args["data"])
                    elif operation == "delete":
                        result = salesforce_function_mapper[operation](object_name, args["record_id"])

                    # Send the result back to Slack
                    client.web_client.chat_postMessage(channel=channel, text=f"Result: {json.dumps(result, indent=2)}")
                except Exception as e:
                    client.web_client.chat_postMessage(channel=channel, text=f"Error: {str(e)}")
            else:
                client.web_client.chat_postMessage(channel=channel, text="Invalid operation format or operation not found.")
