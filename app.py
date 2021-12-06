import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

BOT_ID = app.client.api_call("auth.test")['user_id']

@app.event("message")
def handle_message_events(body,client):
    event = body.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    timestamp = event.get('event_ts')

    # Deleted and reply messages should not be sent to the events api.
    deleted_message = True if event.get('deleted_ts') else False
    threaded_message = True if event.get('thread_ts') else False
    
    # Change if not deleted message and add and not threaded_message
    try:
        if not deleted_message and not threaded_message:
            if user_id != BOT_ID:
                client.reactions_add(channel=channel_id, name="ticket", timestamp=timestamp)
    except Exception as e:
        logging.critical(f"Error: {e} " )

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()