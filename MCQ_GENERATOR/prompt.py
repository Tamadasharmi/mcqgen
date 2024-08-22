TEMPLATE="""
    [INST]
    You are an experienced teacher with 10 years of experience in the {subject}. You completely understand the Context. You are preparing a set of {num_ques} multiple 
    choice questions and their answers as a JSON file.

    Context:{text}

    Here is the expected JSON format for 5 questions and their correct answers:{response_json}

    ###Instructions:
    1.Generate non-repeating questions.The questions should be unique.
    2.Make sure to give 4 options for each question and the correct answer as well.
    3.The JSON file should be in the format of the response specified.
    4.For each question , give 3 wrong options and one correct option.


    [/INST]
    """