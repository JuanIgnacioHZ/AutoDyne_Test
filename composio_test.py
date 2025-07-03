#!AutoDyneTest/bin/python
# Library imports
from composio_openai import ComposioToolSet, Action, App
from agent import get_response
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
    # the fisrt one. Also recover the email data and break after that.
    last_email = {"body": None,
                  "sender_address": None,
                  "sender_name": None,
                  "subject": None}
    for i in unread_messages["data"]["response_data"]["value"]:
        if i["id"] == new_email_id:    # Match the ID's and recover sender
            sender = i["sender"]["emailAddress"]["address"]
            # Email data
            last_email["body"] = i["body"]["content"]
            last_email["sender_address"] = sender
            last_email["sender_name"] = i["sender"]["emailAddress"]["name"]
            last_email["subject"] = i["subject"]
            break

    # Recovers all the messages from the sender
#    relevant_messages = toolset.execute_action(
#            action=Action.OUTLOOK_OUTLOOK_LIST_MESSAGES,
#            params={
#                "from_address": sender,
#                },
#    )
    # With all the emails in memory, collect the relevant data
#    relevant_data = []
#    for i in relevant_messages["data"]["response_data"]["value"]:
        # Data entry
#        tmp_data_entry = {"body": i["body"]["content"],
#                          "sender_address": sender,
#                          "sender_name": i["sender"]["emailAddress"]["name"],
#                          "subject": i["subject"]}
        # Adds the data to a list
#        relevant_data.append(tmp_data_entry)

    # With all of this, the agent can be activated
    agent_answer = get_response(last_email["body"],
                                last_email["subject"],
                                last_email["sender_name"])

    # Retrieves answer data from the angent's response
    answer_text = (agent_answer["messages"][1].content).split("\n\nBody:\n")
    subject = answer_text[0][9:]
    body = answer_text[1]

    # Once the data is obtained, the answering email is sent:
    result = toolset.execute_action(
                action=Action.OUTLOOK_OUTLOOK_REPLY_EMAIL,
                params={
                    "comment": body,
                    "message_id": new_email_id,
                    },
    )

    # Prints status to terminal
    if result['successfull'] and not(result['error']):
        print("LOG: Answer successfully sent without errors")
    else:
        print("LOG: There was en error during the replying.",
              "Status: {result}")

# Runs as a server
if __name__ == "__main__":
    print("LOG: Listening")
    listener.wait_forever()

