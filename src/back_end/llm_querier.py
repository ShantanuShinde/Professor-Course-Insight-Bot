import getpass
import os


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("OPENAI_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent, chat_agent_executor
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

llm1 = ChatOpenAI(model="gpt-4")
llm2 = ChatOpenAI(model="gpt-4")

schema = """The table 'courses' has the following columns:
  subject_prefix: text, nullable — the subject abbreviation (e.g., CS, ACCT)
  course_number: text, nullable — the course number (e.g., 1200, 2301)
  title: text, nullable — the full title of the course
  class_level: text, nullable — the classification of the course (e.g., Undergraduate, Graduate)
The table 'grades_by_professor' has the following columns:
  subject_prefix: text, nullable — the subject abbreviation (e.g., CS, ACCT)
  course_number: text, nullable — the course number (e.g., 1200, 2301)
  profFirst: text, nullable — the professor's first name
  profLast: text, nullable — the professor's last name
  term: text, nullable — the academic term code (e.g., 24F, 25S)
  A_plus: bigint, nullable — number of A+ grades
  A: bigint, nullable — number of A grades
  A_minus: bigint, nullable — number of A- grades
  B_plus: bigint, nullable — number of B+ grades
  B: bigint, nullable — number of B grades
  B_minus: bigint, nullable — number of B- grades
  C_plus: bigint, nullable — number of C+ grades
  C: bigint, nullable — number of C grades
  C_minus: bigint, nullable — number of C- grades
  D_plus: bigint, nullable — number of D+ grades
  D: bigint, nullable — number of D grades
  D_minus: bigint, nullable — number of D- grades
  F: bigint, nullable — number of F grades
  W: bigint, nullable — number of withdrawals
The table 'professor_course_mapping' has the following columns:
  subject_prefix: text, nullable — the subject abbreviation (e.g., CS, ACCT)
  course_number: text, nullable — the course number (e.g., 1200, 2301)
  profFirst: text, nullable — the professor's first name
  profLast: text, nullable — the professor's last name
The table 'professors' has the following columns:
  professorId: text, nullable — unique identifier for the professor
  profFirst: text, nullable — the professor's first name
  profLast: text, nullable — the professor's last name
  email: text, nullable — the professor's email address
  phone_number: text, nullable — the professor's phone number
The table 'profs_remarks' has the following columns:
  profFirst: text, nullable — the professor's first name
  profLast: text, nullable — the professor's last name
  avgDifficulty: double, nullable — average difficulty rating of the professor
  avgRating: double, nullable — average overall rating of the professor
  department: text, nullable — department to which the professor belongs
  totalRatings: bigint, nullable — total number of ratings received
  r1: bigint, nullable — count of 1-star ratings
  r2: bigint, nullable — count of 2-star ratings
  r3: bigint, nullable — count of 3-star ratings
  r4: bigint, nullable — count of 4-star ratings
  r5: bigint, nullable — count of 5-star ratings
  professorTags: text, nullable — tags describing the professor (e.g., "Tough grader", "Inspirational")
  wouldTakeAgainPercent: double, nullable — percentage of students who would take the professor again
The table 'sections' has the following columns:
  sectionId: text, nullable — unique identifier for the section
  course_reference: text, nullable — reference ID linking to the course
  professorId: text, nullable — unique identifier of the professor teaching the section
  instruction_mode: text, nullable — mode of instruction (e.g., Face-to-Face, Online)
  meeting_days: text, nullable — days the class meets (e.g., Mon, Wed, Fri)"""


sql_system_prompt = f"You are a My SQL query generator. You generate concise queries with DISTINCT keyword for the provided prompt, with out any code blocks or markdown formatting. \
                 Only give query, no other text. \
                 Also use full form of course titles. eg: NLP = Natural Language Processing \
                 Also always give SQL queries, no direct answers. \
                 Utilize keywords such as LIMIT for restricting size of result if asked to. \
                 Do not give any destructive queries such as DROP or DELETE.\
                 schema: {schema}"
nl_system_prompt = "You generate natural language responses. You will be given a question and a result from a SQL query relating to the question.\
                    If the query result is too big, ask for followup questions to get more specific answers. \
                    DO NOT GIVE TOO BIG RESULTS, ALWAYS GIVE PARTIAL AND ASK QUESTION TO GET MORE SPECIFIC QUESTION. \
                    You need to convert the query result into natural language response and answer the question. If the result says 'Failed' or the it is empty\
                    reply saying that 'I cannot answer the question. Also answer as if taking to another person, don't mentioned implementation details'"

checkpointer1 = InMemorySaver()
sql_generator = create_react_agent(model=llm1, tools=[], prompt=sql_system_prompt, checkpointer=checkpointer1)
config = {"configurable": {"thread_id": "1"}}
def get_sql_query(user_input: str):
    for event in sql_generator.stream({"messages": [{"role": "user", "content": user_input}]}, config=config, stream_mode="values"):
        if len(event["messages"][-1].response_metadata) != 0:
            return event["messages"][-1].content
        
checkpointer2 = InMemorySaver()
nl_generator = create_react_agent(model=llm2, tools=[], prompt=nl_system_prompt, checkpointer=checkpointer2)
def get_nl_response(question: str, sql_result: str):
    model_input = f"question: {question} SQL result: {sql_result}"
    for event in nl_generator.stream({"messages": [{"role": "user", "content": model_input}]}, config=config, stream_mode="values"):
        if len(event["messages"][-1].response_metadata) != 0:
            return event["messages"][-1].content
