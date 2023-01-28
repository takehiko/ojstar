from json import dumps
import psycopg2
import os
from psycopg2.extras import DictCursor
import urllib.parse
import re

print(psycopg2.apilevel)

# DATABASE_URL = "postgresql://postgres:Password@localhost:5432/db"
DATABASE_URL = "postgresql://postgres:Password@db-container:5432/db"


def getCon():
    return psycopg2.connect(DATABASE_URL)


def outputTofile(num):
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute(
        'SELECT * from question where question_id = %s', (num,))
    question = dict(cur.fetchone())
    cur.close()
    conn.close()

    print(question)

    strToFile(question["output"], "correct1.txt")
    strToFile(question["output2"], "correct2.txt")
    strToFile(question["output3"], "correct3.txt")
    strToFile(question["input"], "input1.txt")
    strToFile(question["input2"], "input2.txt")
    strToFile(question["input3"], "input3.txt")

def outputTofileByQuestion(question):
    strToFile(question["output"], "correct1.txt")
    strToFile(question["output2"], "correct2.txt")
    strToFile(question["output3"], "correct3.txt")
    strToFile(question["input"], "input1.txt")
    strToFile(question["input2"], "input2.txt")
    strToFile(question["input3"], "input3.txt")

def strToFile(str, FileName):
    if os.path.exists(FileName):
        os.remove(FileName)

    with open(FileName, 'w') as f:
        f.write(str)


def getCorrectOutput(question_id: int):
    conn = getCon()
    cur = conn.cursor()
    cur.execute(
        'SELECT output from question where question_id = %s', (question_id,))
    for row in cur:
        print(row[0])
        print(type(row[0]))
    cur.close()
    conn.close()


def getQuestion(num: int) -> dict:
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT * from question where question_id = %s', (num,))

    res = cur.fetchone()

    res = dict(res) if res else None

    cur.close()
    conn.close()

    return res


def getModelAnswer(num: int) -> dict:
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT question.name as name, modelanswer.source as source from question,modelanswer where question.question_id = %s and question.question_id = modelanswer.question_id', (num,))
    res = cur.fetchone()
    res = dict(res) if res else None
    cur.close()
    conn.close()
    return res


def getALLQuestions() -> dict:
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT * from question')
    results = cur.fetchall()
    dict_result = []
    for row in results:
        dict_result.append(dict(row))

    cur.close()
    conn.close()

    return dict_result


def registerSource(student_id: int, question_id: int, result: str, source: str, readhint: int):
    conn = getCon()
    cur = conn.cursor()
    cur.execute("INSERT INTO submit(student_id,question_id,result,source,readhint) VALUES (%s,%s,%s,%s,%s) RETURNING response_id",
                (student_id, question_id, result, source, readhint,))

    conn.commit()  # https://www.psycopg.org/docs/connection.html?highlight=commit#connection.commit
    resID = cur.fetchone()

    cur.close()
    conn.close()

    return resID


def replaceSpecialCharacter(s):
    c = s.group(0)
    d = {
        "&": "&amp;",
        "'": "&#039;",
        '"': "&quot;",
        "<": "&lt;",
        ">": "&gt;",
        "\n": "<br>",
        " ": "&nbsp;",
        "\t": "&nbsp;&nbsp;&nbsp;&nbsp;"
    }
    return d[c] if (c in d) else c


def getSubmit(cond=''):
    query = 'SELECT * FROM submit ' + cond
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute(query)
    cols = [col.name for col in cur.description] # カラム名のリスト
    submits = "<table border='1'><thead><tr>"
    for col in cols:
        submits += "<th>" + col + "</th>"
    submits += "</tr></thead><tbody>"
    for i in cur:
        d = dict(i)
        submits += "<tr>"
        for col in cols:
            submits += "<td>" + (re.sub(r'[&\'"<>\n \t]', replaceSpecialCharacter, (str(d[col]))) if col in d else '&nbsp;') + "</td>"
        submits += "</tr>"
    submits += "</tbody></table>"
    cur.close()
    conn.close()
    return submits


def getALLsubmit():
    return getSubmit('')


def getSubmitByStudentID(studenID):
    return getSubmit(f"WHERE student_id='{studenID}'")


def getSubmitByQuestionID(questionID):
    return getSubmit(f"WHERE question_id='{questionID}'")


def getSubmitByResponseID(response):
    # 数値-数値
    m = re.match(r'^(\d+)-(\d+)', response)
    if m:
        return getSubmit(f'WHERE response_id BETWEEN {m.group(1)} AND {m.group(2)}')
    # -数値
    m = re.match(r'^-(\d+)', response)
    if m:
        return getSubmit(f'WHERE response_id <= {m.group(1)}')
    # 数値-
    m = re.match(r'^(\d+)-', response)
    if m:
        return getSubmit(f'WHERE response_id >= {m.group(1)}')
    # その他（数値のみの場合を含む）
    return getSubmit(f"WHERE response_id='{response}'")

def getSubmitByID(response):
    return getSubmitByResponseID(response)

def getResponseID(studentID, questionID, result, source):
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT response_id FROM submit WHERE student_id = %s AND question_id = %s AND result = %s AND source = %s',
                (studentID, questionID, result, source))
    res = cur.fetchone()
    cur.close()
    conn.close()
    return dict(res)["response_id"]


if __name__ == "__main__":
    # registerSource(1, 1, "a", "b")
    print(getALLsubmit())
