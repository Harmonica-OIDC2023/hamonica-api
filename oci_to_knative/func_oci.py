from fdk import response
import slack_sdk

# knative func
def main(ctx, data):
    channel_id = "C05LE8PAS5T"
    token = "xoxb-5694295360293-5699670812292-VMecMKyfzpfXIcez96p8CDsz"

    client = slack_sdk.WebClient(token=token)
    client.chat_postMessage(channel=channel_id, text="knative-function-test")