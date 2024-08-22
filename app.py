import os
import pandas as pd
import json
import traceback
import PyPDF2
import traceback
from MCQ_GENERATOR.utils import read_file,get_table_data
from MCQ_GENERATOR.logger import logging
from MCQ_GENERATOR.prompt import TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain import HuggingFaceHub
import streamlit as st

llm=HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.2", model_kwargs={"temperature":0.5, "max_new_tokens":4000},
    huggingfacehub_api_token="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")
@st.cache_data
def gen_qqq(text,num,subject,RESPONSE_JSON):
    quiz_generation_prompt = PromptTemplate(
        input_variables=["text", "subject", "response_json","num_ques"],
        template=TEMPLATE
        )

    quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

    generate_evaluate_chain=SequentialChain(chains=[quiz_chain], input_variables=["text", "subject", "response_json","num_ques"],
                                            output_variables=["quiz"], verbose=True,)
    response=generate_evaluate_chain(
            {
            "text": text,
            "subject":subject,
            "response_json": json.dumps(RESPONSE_JSON),
            "num_ques":num
            }
            )
    return response

#Loading the JSON PATH
json_path=r"./Response.json"#path to the json response expected
with open(json_path,'r') as file:
    RESPONSE_JSON=json.load(file)

#Title for app
st.title("Quizzing")
#Creating a form
with st.form("User_inputs"):
    #File_upload
    uploaded_file = st.file_uploader("Upload your pdf/txt file here")
    #Input Fields
    num=st.number_input("No. of questions",min_value=5,max_value=69)
    subject=st.text_input("Subject of the Quiz:",max_chars=25)
    #Create Button
    button=st.form_submit_button("Create Quiz!")
    session_state=st.session_state

    if 'q' not in session_state:
        session_state.q=False
    if not session_state.q:
        session_state.q=button


if session_state.q and uploaded_file is not None and num and subject:
    with st.spinner("Loading..."):
        try:
            text=read_file(uploaded_file)
            response=gen_qqq(text,num,subject,RESPONSE_JSON)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error occurred!")
        else:
            if isinstance(response,dict):
                qq=response.get('quiz',None)
                if qq is not None:
                    i1=qq.find('```')
                    i2=qq.rfind('```')
                    q=qq[i1+8:i2-1]
                    data=get_table_data(q)
                    if data is not None:
                        selected_options=[]
                        correct_ans=[]
                        correct_value=[]
                        for ques in data:
                            options=list(ques["Options"].values())
                            cur_selected=st.radio(ques["Question"],options,index=None)
                            selected_options.append(cur_selected)
                            correct_ans.append(ques["Correct_option"])
                            correct_value.append(ques["Correct_value"])
                        if st.button("Submit"):
                            marks=0
                            st.header("Your Result:")
                            for i,question in enumerate(data):
                                selected_op=selected_options[i]
                                correct_op=correct_ans[i]
                                correct_val=correct_value[i]
                                st.subheader(f"{question['Question']}")
                                st.write(f"You selected: {selected_op}")
                                st.write(f"Correct Answer: {correct_val}")
                                if (selected_op==correct_val):
                                    marks+=1
                            st.subheader(f"You scored {marks} out of {len(data)}")


                        # df=pd.DataFrame(data)
                        # df.index=df.index+1
                        # st.table(df)
                    else:
                        st.error("Generation error!!")
            else:
                st.write(response)
            

