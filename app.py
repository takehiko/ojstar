import re
from flask import Flask, request, jsonify, render_template
from judge import main, runModelAnswer
import dbaccess
from waitress import serve

import urllib.parse
app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/top', methods=['GET', 'POST'])
def top():
    return render_template('top.html')


@app.route('/question/<int:questionID>', methods=['GET', 'POST'])
def question(questionID):
    questionInfo = dbaccess.getQuestion(questionID)
    return render_template('index.html', question=questionInfo) if questionInfo else f'<h1>Question {questionID} not found</h1>'


@app.route('/space', methods=['GET', 'POST'])
def space():
    return render_template('space.html')


@app.route('/choice', methods=['POST', 'GET'])
def choice():
    return render_template('choice.html')


@app.route('/result/s/<string:studentID>', methods=['POST', 'GET'])
def result_s(studentID):
    submits = dbaccess.getSubmitByStudentID(studentID)
    return render_template('result.html', submits=submits)


@app.route('/result/q/<string:questionID>', methods=['POST', 'GET'])
def result_q(questionID):
    submits = dbaccess.getSubmitByQuestionID(questionID)
    return render_template('result.html', submits=submits)


@app.route('/result/id/<string:response>', methods=['POST', 'GET'])
def result_id(response):
    submits = dbaccess.getSubmitByResponseID(response)
    return render_template('result.html', submits=submits)


@app.route('/result/all', methods=['POST', 'GET'])
def result_all():
    submits = dbaccess.getALLsubmit()
    return render_template('result.html', submits=submits)


@app.route('/result', methods=['POST', 'GET'])
def result():
    submits = dbaccess.getSubmit("ORDER BY response_id DESC LIMIT 50")
    print("result")
    print(submits)

    return render_template('result.html', submits=submits)


#@app.route('/getALLsubmits', methods=['POST', 'GET'])
#def getALLsubmits():
#    contents = jsonify(dbaccess.getALLsubmit())
#
#    return contents


@ app.route('/submit_sourcecode', methods=['POST'])
def judge():
    print("judge")
    questionID = int(request.form['questionID'])
    encodedSource = request.form['source']
    studentID = request.form['studentID']
    readhint = int(request.form['readhint'])
    source = urllib.parse.unquote(encodedSource)

    print("questionID: ", questionID)
    print("source: ", source)
    print("studentID: ", studentID)
    print("readhint: ", readhint)

    question = dbaccess.getQuestion(questionID)
    dbaccess.outputTofileByQuestion(question)

    result = main(source, int(question["endline"]))
    # result = main(source, 0)
    # result = main(source, 1)
    # result = main(source, 2)
    # result = main(source, -1)
    # encodedResult = urllib.parse.quote(result)

    # print(result)
    # source = source.replace('\n', '<br>')
    resID = dbaccess.registerSource(studentID, questionID,
                                    result, source, readhint)

    # resID = dbaccess.getResponseID(studentID, questionID, result, source)

    return jsonify({"result": result, "responseID": resID})


@ app.route('/getALLQuestions', methods=['GET', 'POST'])
def getALLQuestions():
    return jsonify(dbaccess.getALLQuestions())


@app.route('/sample/<int:questionID>/<string:input>', methods=['POST', 'GET'])
def sample(questionID, input):
    if re.search(r'[^0-9\s\+\-]', input) != None:
        return f'<h1>Invalid Input</h1>'
    if re.search(r'\d\d\d', input) != None:
        return f'<h1>Invalid Input</h1>'
    question = dbaccess.getModelAnswer(questionID)
    if question == None:
        return f'<h1>Invalid Question</h1>'
    #print("debug:runModelAnswer")
    #print(question)
    output = runModelAnswer(question["source"], input)

    print("sample")
    print(output)

    return render_template('sample.html', question_name=question["name"], input=input, output=output)


# https://qiita.com/ekzemplaro/items/2766618ba5968ee62b70
# host='0.0.0.0' でないとdockerで動かした際に、host側で見ることができない
# threaded = true 同時アクセス制御
development = True

if development:
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
else:
    serve(app, host='0.0.0.0', port=8000)
