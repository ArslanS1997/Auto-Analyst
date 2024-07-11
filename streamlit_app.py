import streamlit as st
import pandas as pd
from retrievers import *
# import json
from agents import *
import plotly.express as px
import traceback
# import subprocess
import sys
from io import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def fix_code_increment():
    st.session_state['fix_code'] =1

def start_analysis():
    st.session_state['start_analysis'] = 1



from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

st.title("Auto-Analyst")
dspy.configure(lm =dspy.GROQ(model='llama3-70b-8192', api_key ="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",max_tokens=10000 ) )

Settings.embed_model = OpenAIEmbedding(api_key='sk-proj-iZICe72trRYdwjB0AB6wT3BlbkFJd98z3nzkRv69ZhkV8VVj')

uploaded_file = st.file_uploader("Upload your file here...")

if 'new_analysis' not in st.session_state:
    st.session_state['new_analysis'] = 0
if 'fix_button' not in st.session_state:
    st.session_state['fix_button'] = 0
if 'start_analysis' not in st.session_state:
    st.session_state['start_analysis'] = 0

st.write(st.session_state)
execution =''
# e =''
# user_given_context =''
if uploaded_file:
    uploaded_df = pd.read_csv(uploaded_file, parse_dates=True, infer_datetime_format=True)
    df = uploaded_df
    st.write(uploaded_df.head())
    desc = st.text_input("Write a description for the uploaded dataset")
    if desc:
        dict_ = make_data(uploaded_df,desc)
    # with open("uploaded_dataframe.json", "w") as fp:
    #     json.dump(dict_ ,fp)
        dict_['df_name'] = 'df'
        dict_['row_count'] = str(len(df))
        # dict_['filename'] ='uploaded_df.csv'
        # df.to_csv('uploaded_df.csv', index=False)
        
    
        doc = [Document(text = str(dict_))]
        # documents.append(doc)
        retrievers['dataframe_index'] =  VectorStoreIndex.from_documents(doc)
        st.write('Document Uploaded Successfully!')
        agents =[preprocessing_agent,statistical_analytics_agent,sk_learn_agent,data_viz_agent]
        auto_analyst_agent = auto_analyst(agents=agents, retrievers=retrievers)
        user_goal = st.text_input("What is the end-goal of the analysis you are conducting", key='user_goal', on_change=start_analysis)
        

        # while st.session_state['new_analysis']==0:
            

    if st.session_state['start_analysis']==1:
        agent_response = auto_analyst_agent(query=user_goal)
        st.write("### The complete Analytics Story")
        st.markdown(agent_response['story_teller_agent'].story)
        st.markdown(agent_response['code_combiner_agent'].refined_complete_code.replace('#','####'))
        fig = px.line(x=[1,1,1,1], y=[1,1,1,1])
        try:
            execution = agent_response['code_combiner_agent'].refined_complete_code.split('```')[1].replace('#','####').replace('python','')
            with stdoutIO() as s:
                exec(execution)
            st.write(s.getvalue().replace('#','#####'))



            # with open('the_code.py','w') as f:
            #     f.write(execution)
            # result = subprocess.Popen([sys.executable, "code.py"], stdout=subprocess.PIPE, text=True)
            # stdout, stderr = result.communicate()
            # st.write(stdout)
            # st.write(stderr)
            # st.write(str(execution))
            st.plotly_chart(fig)
        except:
            e = traceback.format_exc()
            st.write("The code is giving an error on excution "+str(e)[:1500])
            # user_given_context = st.text_input("Help give additional context to guide the agent to fix the code", key='user_given_context')



        with st.chat_input("Give additional context for correcting the error"):
            fix_button = st.button("Fix Code", type="primary", on_click=fix_code_increment)
            new_analysis = st.button("New Analysis", type="primary")
            # st.write(st.session_state)
            while st.session_state['fix_button'] + st.session_state['new_analysis']==0:
                if fix_button!=0:
                    fixed_code_agent = dspy.ChainOfThought(code_fix)
                    fixed_code = fixed_code_agent(faulty_code=execution, error=str(e)[:1000],user_given_context=user_given_context)
                    # st.write(fixed_code.fixed_code)
                    st.code(fixed_code.fixed_code,language="python", line_numbers=False)
                    if len(fixed_code.fixed_code.split('```')[1])>1:
                        execution=fixed_code.fixed_code.split('```')[1].replace('python','').replace('Python','').replace('```','')
                    else:
                        execution=fixed_code.fixed_code.split('```')[0].replace('python','').replace('Python','').replace('```','')
                    if execution!='':
                        with stdoutIO() as s:
                            exec(execution)
                        st.write(s.getvalue().replace('#','#####'))
                        st.plotly_chart(fig)
                elif new_analysis!=0:
                    del user_goal
            # else:

# else:
#     st.session_state['fix_button'] = 1
                # elif new_analysis:
                #     user_goal

                # elif new_analysis:
                    # break


                # st.write(str(execution))


            










    




