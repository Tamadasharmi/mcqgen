import os
import PyPDF2
import json
import traceback
import streamlit as st
def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("PDF_ReadError!!")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "Unsupported file format!! Please input .pdf or .txt files."
            )

@st.cache_data
def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]
        
        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq=value["question"]
            # options=" || ".join(
            #     [
            #         f"{option}-> {option_value}" for option, option_value in value["options"].items()
                 
            #      ]
            # )
            options=value["options"]
            
            correct=value["correct"]
            quiz_table_data.append({"Question": mcq,"Options": options, "Correct_option": correct, "Correct_value": options[correct]})
        
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False