import os
import subprocess
import re
from hashlib import sha256


def main(str, lineend = 0):
    result = ""

    if "system" in str:
        return "Dangerous Program"

    stringToFile(str)
    if os.path.isfile("./submit.c"):

        result = compile("submit.c", lineend)
        deleteBinary()

    return result


def stringToFile(str):
    f = open("submit.c", "w")
    f.write(str)
    f.close()


def compile(FileName, lineend = 0):
    command = "gcc {}".format(FileName)

    cp = subprocess.run(command, shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if cp.returncode != 0:
        return "Compile Error"

    return func(lineend)


def func(lineend = 0):
    command = "./a.out"

    for index in range(1, 4):

        try:
            # refer https://docs.python.org/ja/3/library/subprocess.html
            cp = subprocess.run(command, shell=False, stdin=open(f'input{index}.txt', "r"),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2, check=True)

            stdout = cp.stdout.decode("utf-8")
        except subprocess.TimeoutExpired:
            # print("Time Limit Exceeded")
            return "Time Limit Exceeded"
        except subprocess.CalledProcessError:
            # print("Runtime Error")
            return "Runtime Error"
        else:
            if answerJudge(stdout, f'correct{index}.txt', lineend) == "Wrong Answer":
                return "Wrong Answer"

    return "Accepted"


def answerJudge(stdout, FileName, lineend):
    stdout = processLineEnd(stdout, lineend)
    print(stdout)
    stdout = stdout.encode("utf-8")
    submitHash = sha256(stdout).hexdigest()

    ans = open(FileName, "r").read()
    ans = processLineEnd(ans, lineend)
    ans = ans.encode("utf-8")
    print(ans)

    ansHash = sha256(ans).hexdigest()

    if submitHash == ansHash:
        # print("Accepted")
        return "Accepted"
    else:
        # print("Wrong Answer")
        return "Wrong Answer"


# （lineend < 0 : 置換しない）
# lineend >= 0 : 最終行の改行を取り除く（デフォルト）
# lineend >= 1 : 各行の末尾空白を取り除く
# lineend >= 2 : 先頭および末尾の空行を（空白文字があれば合わせて）取り除く
def processLineEnd(str, lineend = 0):
    if lineend >= 2:
        str = re.sub(re.compile("\A(^\s*\n)+|(^\s*\n)+\s*\Z", re.M), "", str)
    if lineend >= 1:
        str = re.sub(re.compile("\s+$", re.M), "", str)
    if lineend >= 0:
        str = re.sub("\n\Z", "", str)

    return str


def deleteBinary(FileName="./a.out"):
    if os.path.isfile(FileName):
        os.remove(FileName)


def runModelAnswer(source, input):
    # sourceをファイルに保存
    f = open("model.c", "w")
    f.write(source)
    f.close()
    # コンパイル
    command = "gcc model.c -o model"
    cp = subprocess.run(command, shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode != 0:
        return "Compile Error"
    if os.path.isfile("model") == False:
        return "Compile Error (Executable file not created)"
    # inputを与えてプログラムを実行し，結果を獲得
    command = "./model"
    output = ""
    try:
        cp = subprocess.run(command, input=input.encode(), shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2, check=True)
        output = cp.stdout.decode("utf-8")
    except subprocess.TimeoutExpired:
        return "Time Limit Exceeded"
    except subprocess.CalledProcessError:
        return "Runtime Error"
    # ファイル削除
    os.remove("model")
    os.remove("model.c")
    # 結果を返す
    return output

if __name__ == "__main__":
    FileName = ["accepted.c", "wronganswer.c",
                "RuntimeError.c", "CompileError.c", "endlessloop.c", "dangerous.c"]

    for file in FileName:
        file = "./testFile/" + file
        print(file + " test")
        print(compile(file))
        deleteBinary()

    teststr = "abcdefgh\nfjfjf\n\n\n\n"
    print(teststr)

    teststr = processLineEnd(teststr, 0)

    print(teststr)
