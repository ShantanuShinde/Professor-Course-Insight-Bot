import getpass
import os


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("GOOGLE_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent, chat_agent_executor
from langgraph.checkpoint.memory import InMemorySaver
print("here")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
schema = "professors (id, first_name, last_name, email) Key(id) \
          courses (course_id, title, class_level) Key(course_id) \
          grades (professor_id, course_id, section_id, A, Aminus, Bplus, B, Bminus, Cplus, C, Cminus, Dplus, D, Dminus, F, W) Key(professor_id, course_id, section_id)"
system_prompt = f"You are a SQL query generator. You generate concise queries with DISTINCT keyword for the provided prompt, with out any code blocks or markdown formatting. \
                 if prompt isn't related to getting SQL query. \
                 Course ID is of format <subject_prefix><course_number> eg: CS1234. \
                 schema: {schema}"

checkpointer = InMemorySaver()
sql_generator = create_react_agent(model=llm, tools=[], prompt=system_prompt, checkpointer=checkpointer)
config = {"configurable": {"thread_id": "1"}}
def get_sql_query(user_input: str):
    for event in sql_generator.stream({"messages": [{"role": "user", "content": user_input}]}, config=config, stream_mode="values"):
        if len(event["messages"][-1].response_metadata) != 0:
            print(event["messages"][-1].content)
            return event["messages"][-1].content
