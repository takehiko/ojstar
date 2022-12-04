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
        output3
    )
VALUES (
        1,
        '第1問',
        'scanf関数を呼び出して、2つの正の整数を受け取り変数nおよびmに格納したあと、出力例のように、行数がn、列数がmの「*」による長方形のような並びを出力するプログラムを作成してください。',
        'https://paiza.io/projects/e/SKlUEYW3t3FKZPTwaLoKSg?theme=twilight',
        E'3 4\n',
        E'****\n****\n****\n',
        E'6 5\n',
        E'*****\n*****\n*****\n*****\n*****\n*****\n',
        E'1 1\n',
        E'*\n'
    );
