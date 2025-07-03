#!AutoDyneTest/bin/python
# Library imports
from composio_openai import ComposioToolSet, Action, App

from pdb import set_trace

# Toolset interface
toolset = ComposioToolSet()

# Fetch the required toolset for Outlook App
outlook_toolset = toolset.get_tools(
        actions=[
            Action.OUTLOOK_OUTLOOK_LIST_MESSAGES,
            Action.OUTLOOK_OUTLOOK_REPLY_EMAIL,
            Action.OUTLOOK_OUTLOOK_SEND_EMAIL
            ]
        )

# Now, the trigger is set up
listener = toolset.create_trigger_listener()

@listener.callback(
        filters={
            "trigger_name": "OUTLOOK_OUTLOOK_MESSAGE_TRIGGER"
        }
)
def process_incoming_outlook_message(event) -> None:
    """ Function for processing the incoming emails

        Receives the event which triggers the call, with it gathers the email
    id and all the messages coming from that sender. Then recovers relevant
    information from it to be used as reference in the prompt.
        With all of that, calls Langgraph to write an answer (with memory) and
    sends that as a reply.
    """
    print("LOG: Received new email. Processing")
    new_email_id = event.payload["id"]  # Gets the new email ID

    # All the unread emails are fetched
    unread_messages = toolset.execute_action(
            action=Action.OUTLOOK_OUTLOOK_LIST_MESSAGES,
            params={
                "folder": "inbox",
                "is_read": False,
                },
    )

    # Then, go through all of them and get which one matches, usually will be
    # the fisrt one. Break after that
    for i in unread_messages["data"]["response_data"]["value"]:
        if i["id"] == new_email_id:    # Match the ID's and recover sender
            sender = i["sender"]["emailAddress"]["address"]
            break

    # Recovers all the messages from the sender
    relevant_messages = toolset.execute_action(
            action=Action.OUTLOOK_OUTLOOK_LIST_MESSAGES,
            params={
                "from_address": sender,
                },
    )
    # With all the emails in memory, collect the relevant data
    relevant_data = []
    for i in relevant_messages["data"]["response_data"]["value"]:
        # Data entry
        tmp_data_entry = {"body": i["body"]["content"],
                          "sender_address": sender,
                          "sender_name": i["sender"]["emailAddress"]["name"],
                          "subject": i["subject"]}
        # Adds the data to a list
        relevant_data.append(tmp_data_entry)

    # Separates the last received message to focus on what is immediate
    last_email_data = relevant_data.pop(-1)

    # With all of this, the agent can be reactivated
    


    set_trace()
    # With that, 

print("LOG: Listening")
listener.wait_forever()
# This gets the messages from server
#message_fetch_data = outlook_toolset.execute_action(
#        action=Action.OUTLOOK_OUTLOOK_LIST_MESSAGES,
#        params={
#            "folder": "inbox",
#            "is_read": False,
#            },
#)

# Then, the number of received emails is gotten from the list
#mail_count = len(message_fetch_data["data"]["response_data"]["value"])



































