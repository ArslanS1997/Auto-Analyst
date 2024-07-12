import streamlit as st
import pandas as pd
from retrievers import *
import json
from agents import *
import plotly.express as px
import traceback
# import subprocess
import sys
from io import StringIO
import contextlib
import time
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from groq import Groq
import os
from llama_index.core.readers.json import JSONReader


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
def reset_everything():
    if 'new_analysis'  in st.session_state:
        st.session_state['new_analysis'] = 0
    if 'fix_button'  in st.session_state:
        st.session_state['fix_button'] = 0
    if 'start_analysis'  in st.session_state:
        st.session_state['start_analysis'] = 0
    if 'begin_execution'  in st.session_state:
        st.session_state['begin_execution'] = 0



def fix_code_increment(e, execution, user_given_context):
    counter = 0
    fixed_code_agent = dspy.ChainOfThought(code_fix)
    fixed_code = fixed_code_agent(faulty_code=execution, error=str(e)[:1000],user_given_context=user_given_context)
    # st.write(fixed_code.fixed_code)
    st.code(fixed_code.fixed_code,language="python", line_numbers=False)
    if len(fixed_code.fixed_code.split('```')[1])>1:
        execution=fixed_code.fixed_code.split('```')[1].replace('python','').replace('Python','').replace('```','')
    else:
        execution=fixed_code.fixed_code.split('```')[0].replace('python','').replace('Python','').replace('```','')
    try:
        st.write("Begin writing the fixed code")
        if execution!='':
            with stdoutIO() as s:
                exec(execution)
            st.markdown(s.getvalue().replace('#','#####'))
            st.plotly_chart(fig)
        else:
            if counter==0:
                st.write("Wait as it fixes the code......")
                counter+=1
            else:
                st.write('.')
        
    except:
        st.write("Unable to Fix based on context and error description")
        if st.button("Try Again?"):
            context = st.text_input("Rephrase the error")
            fix_code_increment(e,execution, context)
        if st.button("New Analysis"):
            reset_everything()
            
        
    st.write(st.session_state)
    # st.session_state['load'] = 1
    st.session_state['fix_button'] = 0
    # reset_everything()
   

def start_analysis():
    st.session_state['start_analysis'] = 1
    
    

def begin_execution(user_goal,auto_analyst_agent):
    # st.write(st.session_state['user_goal'])
    st.session_state['begin_execution'] = 1
    st.write(st.session_state['user_goal'])
    # user_goal = 
    if st.session_state['begin_execution']==1:
            st.write("Start working on user-goal :")
            st.write(str(user_goal))
            agent_response = auto_analyst_agent(query=st.session_state['user_goal'])
            st.write("The complete Analytics Story")
            st.markdown(agent_response['story_teller_agent'].story)
            st.markdown(agent_response['code_combiner_agent'].refined_complete_code.replace('#','####'))
            fig = px.line(x=[1,1,1,1], y=[1,1,1,1])
            execution = agent_response['code_combiner_agent'].refined_complete_code.split('```')[1].replace('#','####').replace('python','')

            try:
                # execution = agent_response['code_combiner_agent'].refined_complete_code.split('```')[1].replace('#','####').replace('python','')
                if execution!='':
                    with st.echo():
                        exec(execution)
                    st.markdown(s.getvalue().replace('#','########'))
                    if 'fig' in execution:
                        st.plotly_chart(fig)
            except:
                st.session_state['load'] =0

                e = traceback.format_exc()
                st.markdown("The code is giving an error on excution "+str(e)[:1500])
                st.write("Please help the code fix agent with human understanding")
                user_given_context = st.text_input("Help give additional context to guide the agent to fix the code", key='user_given_context')
                st.session_state['fix_button'] = 1
                st.button("Submit Fix Code", on_click=fix_code_increment, args=[e, execution, user_given_context])
    if st.session_state['fix_button']==0:
        reset_everything()
    else:
        st.write("Please give additional context for the agent to try again")
    # st.session_state['begin_execution'] = 0
    
# def file_loader():
    






agents =[preprocessing_agent,statistical_analytics_agent,sk_learn_agent,data_viz_agent]

dspy.configure(lm =dspy.GROQ(model='llama3-70b-8192', api_key =os.environ.get("GROQ_API_KEY"),max_tokens=10000 ) )

Settings.embed_model = OpenAIEmbedding(api_key=os.environ["OPENAI_API_KEY"])

retrievers = {}


# documents = reader.load_data(input_file='dataframe.json')



if 'new_analysis' not in st.session_state:
    st.session_state['new_analysis'] = 0
if 'fix_button' not in st.session_state:
    st.session_state['fix_button'] = 0
if 'start_analysis' not in st.session_state:
    st.session_state['start_analysis'] = 0
if 'begin_execution' not in st.session_state:
    st.session_state['begin_execution'] = 0
if 'user_goal' not in st.session_state:
    st.session_state['user_goal'] = ''
if 'desc' not in st.session_state:
    st.session_state['desc'] = ''
if 'load' not in st.session_state:
    st.session_state['load'] = 0
if 'dict_' not in st.session_state:
    st.session_state['dict_'] = {}

# if 'auto_analyst_'

# @st.cache_data(hash_funcs={StringIO: StringIO.getvalue})
# def create_auto_analyst(agents, _retrievers):
#     return auto_analyst(agents=agents, retrievers=_retrievers)
@st.cache_data(hash_funcs={StringIO: StringIO.getvalue})
def create_retrievers(_styling_instructions, _doc):
    retrievers ={}
    style_index =  VectorStoreIndex.from_documents(_styling_instructions)
    retrievers['style_index'] = style_index
    retrievers['dataframe_index'] =  VectorStoreIndex.from_documents(doc)
    st.write('Document Uploaded Successfully!')
    return retrievers

# @st.cache_data(persist="disk")
# def fetch_and_clean_data(uploaded_file):
#     count = 0
#     uploaded_df = pd.read_csv(uploaded_file, parse_dates=True, infer_datetime_format=True)
#     df = uploaded_df
#     st.write(uploaded_df.head())
#     desc = st.text_input("Write a description for the uploaded dataset")
#     st.button("Start Analysis", on_click=start_analysis)

#     if st.session_state['start_analysis']==1:
        
#         dict_ = make_data(uploaded_df,desc)
#     # with open("uploaded_dataframe.json", "w") as fp:
#     #     json.dump(dict_ ,fp)
#         dict_['df_name'] = 'df'
#         dict_['row_count'] = str(len(df))
#         # dict_['filename'] ='uploaded_df.csv'
#         # df.to_csv('uploaded_df.csv', index=False)
        
    
#         doc = [Document(text = str(dict_))]
#         # documents.append(doc)
#         retrievers['dataframe_index'] =  VectorStoreIndex.from_documents(doc)
#         st.write('Document Uploaded Successfully!')
#         return retrievers
#     else:
#         if desc=='' and count==0:
#             st.write("Write a description of atleast 30-40 words, describe in detail the context surrounding the data, also add description about the column names")
#             count+=1

    # Fetch data from URL here, and then clean it up.
    
@st.cache_data
def get_data(uploaded_df):
    return uploaded_df






st.write(st.session_state)
execution =''
count =0
st.title("Auto-Analyst - Let the AI do all the heavy lifting")
uploaded_file = st.file_uploader("Upload your file here...")
if st.session_state['fix_button'] == 0:
    

    # e =''
    # user_given_context =''
    if uploaded_file:
        if st.session_state['load'] == 0 :
                
            uploaded_df = pd.read_csv(uploaded_file, parse_dates=True, infer_datetime_format=True)
            df = get_data(uploaded_df)
            st.write(uploaded_df.head())
            desc = st.text_input("Write a description for the uploaded dataset")
            st.button("Start Analysis", on_click=start_analysis)

            if st.session_state['start_analysis']==1:
                
                dict_ = make_data(uploaded_df,desc)
                # with open("uploaded_dataframe.json", "w") as fp:
                #     json.dump(dict_ ,fp)
                
                # dict_[]
                # dict_['row_count'] = str(len(df))
                # dict_['filename'] ='uploaded_df.csv'
                # df.to_csv('uploaded_df.csv', index=False)
                
            
                doc = [Document(text = str(dict_))]
                # documents.append(doc)

                # retrievers = create_retrievers(styling_instructions,doc)
                # auto_analyst_agent = auto_analyst(agents,retrievers)
                st.session_state['dict_'] = dict_
                st.session_state['load'] = 1
                
                
            else:
                if desc=='' and count==0:
                    st.write("Write a description of atleast 30-40 words, describe in detail the context surrounding the data, also add description about the column names")
                    count+=1
                


        if st.session_state['load'] == 1:
            # reader = JSONReader()
            # doc = reader.load_data(input_file='uploaded_dataframe.json')
            doc = [Document(text = str(st.session_state['dict_']))]
            retrievers = create_retrievers(styling_instructions,doc)
            auto_analyst_agent = auto_analyst(agents=agents, retrievers=retrievers)

            user_goal = st.chat_input("Define the end-goal of your analysis", on_submit=begin_execution, key='user_goal', args=(st.session_state['user_goal'],auto_analyst_agent))




    