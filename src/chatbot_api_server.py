from flask import Flask, request
from llm_querier import get_sql_query, get_nl_response
from sql_manager import get_query_results

app = Flask(__name__)

@app.route('/api/ask', methods=['POST'])
def answer_question():
    question = request.args.get('question')
    query = get_sql_query(question)
    result = get_query_results(query)
    response = get_nl_response(question, result)
    return {"response" : response}

if __name__ == '__main__':
    app.run(debug=True)