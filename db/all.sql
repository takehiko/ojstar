CREATE TABLE question (
    question_id SERIAL NOT NULL,
    name text UNIQUE,
    question_content text NOT NULL,
    iframe_url text NOT NULL,
    input text NOT NULL,
    output text NOT NULL,
    input2 text NOT NULL,
    output2 text NOT NULL,
    input3 text NOT NULL,
    output3 text NOT NULL,
    hint text NOT NULL DEFAULT 'ヒントはありません。',
    difficulty VARCHAR(10) DEFAULT 'NONE',
    basename text DEFAULT '',
    commentary text DEFAULT '',
    PRIMARY KEY (question_id)
);
CREATE TABLE submit (
    response_id SERIAL NOT NULL,
    student_id int NOT NULL,
    question_id int NOT NULL,
    result text NOT NULL,
    source text NOT NULL,
    readhint INT NOT NULL DEFAULT 0,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (response_id),
    FOREIGN KEY (question_id) REFERENCES question (question_id)
);
INSERT INTO question (
        question_id,
        name,
        question_content,
        iframe_url,
        input,
        output,
        input2,
        output2,
        input3,
        output3,
        hint
    )
VALUES (
        1,
        '第1問',
        'scanf関数を呼び出して、2つの正の整数を受け取り変数nおよびmに格納したあと、出力例のように、行数がn、列数がmの「*」による長方形のような並びを出力するプログラムを作成してください。',
        'https://paiza.io/projects/e/UNWMZBJv3imIf1-purutqQ?theme=twilight',
        E'3 4\n',
        E'****\n****\n****\n',
        E'6 5\n',
        E'*****\n*****\n*****\n*****\n*****\n*****\n',
        E'1 1\n',
        E'*\n',
        '九九のプログラムを手直しするといいでしょう。変数n、mと別に、forループのための変数宣言が必要となります。繰返し回数と、forループの中で何を出力すればよいかを正しく書いて、Acceptedを目指してください。'
    ),(
        2,
        '第2問',
        'scanf関数を呼び出して、1つの整数を受け取り変数nに格納したあと、出力例のように、1行目に1個の「*」、1行増えるごとに「*」の数を1ずつ増やして、n行目にn個の「*」で、直角三角形のような並びを出力するプログラムを作成してください。<br>0または負の値がnに格納された場合には、何も出力せずにプログラムを終了してください。1の場合には、「*」と改行だけを出力しなさい。',
        'https://paiza.io/projects/e/Evck7TD6YSM3n5v3phhgEQ?theme=twilight',
        E'4\n',
        E'*\n**\n***\n****\n',
        E'7\n',
        E'*\n**\n***\n****\n*****\n******\n*******\n',
        E'1 1\n',
        E'*\n',
        '第1問と同じように、2重ループにします。外側の繰返しの条件は、nと外側のループ用変数を使用して、条件式を書いてください。内側の繰返しの条件は、内側と外側のループ用変数を使用して、条件式を書いてください。i 行目（1≦i≦n）には「*」を連続して i 個、出力させましょう。'
    ),(
        3,
        '第3問',
        'scanf関数を呼び出して、1つの整数を受け取り変数nに格納したあと、出力例のように、1行目にn個の「*」、1行増えるごとに「*」の数を1ずつ減らして、n行目に1個の「*」で、直角三角形のような並びを出力するプログラムを作成してください。<br>0または負の値がnに格納された場合には、何も出力せずにプログラムを終了してください。1の場合には、「*」と改行だけを出力しなさい。',
        'https://paiza.io/projects/e/Evck7TD6YSM3n5v3phhgEQ?theme=twilight',
        E'4\n',
        E'****\n***\n**\n*\n',
        E'6\n',
        E'******\n*****\n****\n***\n**\n*\n',
        E'1 1\n',
        E'*\n',
        '第2問が正しく作れたら、2重ループの内側のforの行を変更するだけで、第3問もAcceptedを得ることができます。第2問では、i 行目（1≦i≦n）には「*」を連続して i 個、出力させればよかったのですが、この問題では、i 行目に「*」を連続して何個、出力すればいいでしょうか。n と i を使った式で表してみてください。'
    );

-- iframe_urlの値の取得方法
-- 1. https://paiza.io/ja にアクセスし、コード作成ボタンを押す
-- 2. ソースコードを打ち込み、必要に応じて入力欄に値を指定し、実行ボタンを押す
-- 3. 実行ボタンの行の右端にある共有と埋め込みボタンを押す
-- 4. 埋め込みタグ内のsrc属性の値をコピーする
-- 注意:複数の問題を登録する際、手順1からやり直す
