import getpass
import os


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("GOOGLE_API_KEY")


from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent, chat_agent_executor
from langgraph.checkpoint.memory import InMemorySaver

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
system_prompt = "You are a SQL query generator. You generate concise queries for the provided prompt and schema. Say 'Irrelevant prompt' if prompt isn't related to getting SQL query"


# def chatbot(state: State):
#     return {"messages": [llm.invoke(state["messages"])]}

# graph_builder.add_node("chatbot", chatbot)

# graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("chatbot", END)
# graph = graph_builder.compile()
checkpointer = InMemorySaver()
graph = create_react_agent(model=llm, tools=[], prompt=system_prompt, checkpointer=checkpointer)
config = {"configurable": {"thread_id": "1"}}
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config=config, stream_mode="values"):
        if len(event["messages"][-1].response_metadata) != 0:
            return event["messages"][-1].content
# while True:
#     try:
#         user_input = input("User: ")
#         if user_input.lower() in ["quit", "exit", "q"]:
#             break

#         stream_graph_updates(user_input)
#     except:
#         # fallback if input() is not available
#         user_input = "What do you know about LangGraph?"
#         print("User: " + user_input)
#         stream_graph_updates(user_input)
#         break