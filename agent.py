#! ./AutoDyneTest/bin/python3
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from pdb import set_trace       # For debugging

# Prompt definition and configuration
agent_prompt= """
You are an AI assistant helping in email writing in a polite but concise matter.
Your task is to create processional replies to emails based on the content of
email.

Please output two things: a subject and a body, the first one in one line and
the other one next. And please tag them with "Subject:" and "Body:".

Sign the body as follows:
Best, 
[Name] [Company]
"""
def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    """ Configures the agent to behave in order to write email answers
    """
    user_name = config["configurable"].get("user_name")
    #past_messages = config["configurable"].get("past_messages")
    system_msg = agent_prompt
    return [{"role": "system", "content": system_msg}] + state["messages"]


def get_response(body:str, subject:str, sender:str) -> dict:
    # Checkpoint for enabling memory
    checkpointer_0 = InMemorySaver()

    # Model specification
    model_0 = init_chat_model(
        "anthropic:claude-3-7-sonnet-latest",
        temperature=0
    )

    # Agent creation
    agent = create_react_agent(
        model=model_0,
        tools=[],
        checkpointer=checkpointer_0,
        prompt=agent_prompt
    )

    # Run the agent
    response = agent.invoke(
        {"messages": [{"role": "user", "content": body}]},
        # Chat configuration
        config = {"configurable": {"thread_id": "1",
                                   "sender": sender,
                                   "subject": subject}}
    )

    return response

