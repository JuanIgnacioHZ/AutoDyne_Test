#! ./AutoDyneTest/bin/python3
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from pdb import set_trace       # For debugging

# Example data gathering function
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


# Model specification
model_0 = init_chat_model(
    "anthropic:claude-3-7-sonnet-latest",
    temperature=0
)

# Agent creation
agent = create_react_agent(
    model=model_0,
    tools=[get_weather],
    prompt="You are an assistant helping in email writing in a polite but concise matter."
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

set_trace()
