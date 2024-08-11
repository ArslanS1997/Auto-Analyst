# This file is for the streamlit frontend

# All imports
from agents import *
import streamlit as st
from retrievers import *
import os
import statsmodels.api as sm
from streamlit_feedback import streamlit_feedback
from llama_index.core import Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from io import StringIO
import traceback
import contextlib
import sys
import plotly as px
import matplotlib.pyplot as plt
def reset_everything():
    st.cache_data.clear()





# stores std output generated on the console to be shown to the user on streamlit app
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

# Markdown changes made to the sidebar
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #ff8080;
        color: #ffffff;
        title-color:#ffffff
    }
</style>
<style>
  [data-testid=stSidebar] h1 {
    color: #ffffff

   }
</style>
""", unsafe_allow_html=True)


# Load the agents into the system
agent_names= [data_viz_agent,sk_learn_agent,statistical_analytics_agent,preprocessing_agent]
# Configure the LLM to be ChatGPT-4o-mini
# You can change this to use your particular choice of LLM
dspy.configure(lm = dspy.OpenAI(model='gpt-4o-mini',api_key=os.environ['OPENAI_API_KEY'], max_tokens=16384))

# dspy.configure(lm =dspy.GROQ(model='llama3-70b-8192', api_key =os.environ.get("GROQ_API_KEY"),max_tokens=10000 ) )

# sets the embedding model to be used as OpenAI default
Settings.embed_model = OpenAIEmbedding(api_key=os.environ["OPENAI_API_KEY"])

# Imports images
st.image('./images/Auto-analysts icon small.png', width=70)
st.title("Auto-Analyst")
    

# asthetic features for streamlit app
st.logo('./images/Auto-analysts icon small.png')
st.sidebar.title(":white[Auto-Analyst] ")
st.sidebar.text("Have all your Data Science ")
st.sidebar.text("Analysis Done!")

# creates the file_uploader
uploaded_file = st.file_uploader("Upload your file here...", on_change=reset_everything())
st.write("You can upload your own data or use sample data by clicking the button below")
# creates a button to use the sample data
sample_data = st.button("Use Sample Data")
if sample_data:

    uploaded_file = "Housing.csv"

# more markdown changes
st.markdown(
    """
    <style>
    .css-1l1u5u8 code {
        color: black; /* Change this to your desired color */
        background-color: #f5f5f5; /* Optional: change background color if needed */
        padding: 2px 4px;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# displays the instructions for the user
st.markdown(instructions)


retrievers = {}
# df = pd.read_csv('open_deals_min2.csv')
#initializes the uploaded_df or sample df into a dataframe
# also caches that data for performance
@st.cache_data
def initialize_data(button_pressed=False):
    if button_pressed==False:
        uploaded_df = pd.read_csv(uploaded_file, parse_dates=True)
    else:
        uploaded_df = pd.read_csv("Housing.csv")
        st.write("LOADED")
    return uploaded_df


#initializes the planner based system
@st.cache_resource
def intialize_agent():

    return auto_analyst(agents=agent_names,retrievers=retrievers)

#intializes the independent components
@st.cache_resource
def initial_agent_ind():
    return auto_analyst_ind(agents=agent_names,retrievers=retrievers)

#initializes the two retrievers one for data, the other for styling to be used by visualization agent
@st.cache_data(hash_funcs={StringIO: StringIO.getvalue})
def initiatlize_retrievers(_styling_instructions, _doc):
    retrievers ={}
    style_index =  VectorStoreIndex.from_documents([Document(text=x) for x in _styling_instructions])
    retrievers['style_index'] = style_index
    retrievers['dataframe_index'] =  VectorStoreIndex.from_documents([Document(text=x) for x in _doc])

    return retrievers
    
# a simple function to save the output 
def save():
    filename = 'output2.txt'
    outfile = open(filename, 'a')
    
    outfile.writelines([str(i)+'\n' for i in st.session_state.messages])
    outfile.close()


# Defines how the chat system works
def run_chat():
    # defines a variable df (agent code often refers to the dataframe as that)
    if 'df' in st.session_state:
        df = st.session_state['df']
        if df is not None:
            st.write(df.head(5))
            if "show_placeholder" not in st.session_state:
                st.session_state.show_placeholder = True
        else:
            st.error("No data uploaded yet, please upload a file or use sample data")
   
    # Placeholder text to display above the chat box
    placeholder_text = "Welcome to Auto-Analyst, How can I help you? You can use @agent_name to call a specific agent or let the planner route the query!"

    # Display the placeholder text above the chat box
    if "show_placeholder" in st.session_state and st.session_state.show_placeholder:
        st.markdown(f"**{placeholder_text}**")

    # User input taken here    
    user_input = st.chat_input("What are the summary statistics of the data?")

    # Once the user enters a query, hide the placeholder text
    if user_input:
        st.session_state.show_placeholder = False


    # If user has given input or query
    if user_input:
        # this chunk displays previous interactions
        if st.session_state.messages!=[]:
            for m in st.session_state.messages:
                if '-------------------------' not in m:
                    st.write(m.replace('#','######'))






        st.session_state.messages.append('\n------------------------------------------------NEW QUERY------------------------------------------------\n')
        st.session_state.messages.append(f"User: {user_input}")
        
        #all the agents the user mentioned by name to be stored in this list
        specified_agents = []
        # checks for each agent if it is mentioned in the query
        for a in agent_names: 
            if a.__pydantic_core_schema__['schema']['model_name'] in user_input.lower():
                specified_agents.insert(0,a.__pydantic_core_schema__['schema']['model_name'])

    # this is triggered when user did not mention any of the agents in the query
    # this is the planner based routing
        if specified_agents==[]:



            # Generate response in a chat message object
            with st.chat_message("Auto-Anlyst Bot",avatar="🚀"):
                st.write("Responding to "+ user_input)
                # sends the query to the chat system
                output=st.session_state['agent_system_chat'](query=user_input)
                #only executes output from the code combiner agent
                execution = output['code_combiner_agent'].refined_complete_code.split('```')[1].replace('#','####').replace('python','')
                st.markdown(output['code_combiner_agent'].refined_complete_code)
                
                # Tries to execute the code and display the output generated from the console
                try:
                    
                    with stdoutIO() as s:
                        exec(execution)
                       
                    st.write(s.getvalue().replace('#','########'))

                    
                # If code generates an error (testing code fixing agent will be added here)
                except:

                    e = traceback.format_exc()
                    st.markdown("The code is giving an error on excution "+str(e)[:1500])
                    st.write("Please help the code fix agent with human understanding")
                    user_given_context = st.text_input("Help give additional context to guide the agent to fix the code", key='user_given_context')
                    st.session_state.messages.append(user_given_context)

    # this is if the specified_agent list is not empty, send to individual mentioned agents
        else:
            for spec_agent in specified_agents:
                with st.chat_message(spec_agent+" Bot",avatar="🚀"):
                    st.markdown("Responding to "+ user_input)
                    # only sends to the specified agents 
                    output=st.session_state['agent_system_chat_ind'](query=user_input, specified_agent=spec_agent)

                    # Fail safe sometimes code output not structured correctly
                    if len(output[spec_agent].code.split('```'))>1:
                        execution = output[spec_agent].code.split('```')[1].replace('#','####').replace('python','').replace('fig.show()','st.plotly_chart(fig)')
                    else:
                        execution = output[spec_agent].code.split('```')[0].replace('#','####').replace('python','').replace('fig.show()','st.plotly_chart(fig)')


                    # does the code execution and displays it to the user
                    try:
                        
                        with stdoutIO() as s:
                            exec(execution)
                    

                        st.write(s.getvalue().replace('#','########'))


                        
                # If code generates an error (testing code fixing agent will be added here)

                    except:

                        e = traceback.format_exc()
                        st.markdown("The code is giving an error on excution "+str(e)[:1500])
                        st.write("Please help the code fix agent with human understanding")
                        user_given_context = st.text_input("Help give additional context to guide the agent to fix the code", key='user_given_context')
                        st.session_state.messages.append(user_given_context)


# simple feedback form to capture the user's feedback on the answers
        with st.form('form'):
            streamlit_feedback(feedback_type="thumbs", optional_text_label="Do you like the response?", align="flex-start")

            st.session_state.messages.append('\n---------------------------------------------------------------------------------------------------------\n')
            st.form_submit_button('Save feedback',on_click=save())






# initializes some variables in the streamlit session state
# messages used for storing query and agent responses
if "messages" not in st.session_state:
    st.session_state.messages = []
# thumbs used to store user feedback
if "thumbs" not in st.session_state:
    st.session_state.thumbs = ''
#stores df
if "df" not in st.session_state:
    st.session_state.df = None
#stores short-term memory
if "st_memory" not in st.session_state:
    st.session_state.st_memory = []

# if user has uploaded a file or used our sample data
if uploaded_file or sample_data:
    # intializes the dataframe
    st.session_state['df'] = initialize_data()
    
    st.write(st.session_state['df'].head())
    # if user asked for sample data
    if sample_data:
        desc = "Housing Dataset"
        doc=[str(make_data(st.session_state['df'],desc))]
    # if user uploaded their own data
    else:
        # They give a small description so the LLM/Agent can be given additional context
        desc = st.text_input("Write a description for the uploaded dataset")
        doc=['']
        if st.button("Start The Analysis"):

            dict_ = make_data(st.session_state['df'],desc)
            doc = [str(dict_)]

# this initializes the retrievers 
    if doc[0]!='':
        retrievers = initiatlize_retrievers(styling_instructions,doc)
        
        st.success('Document Uploaded Successfully!')
        st.session_state['agent_system_chat'] = intialize_agent()
        st.session_state['agent_system_chat_ind'] = initial_agent_ind()
        st.write("Begin")
    



# saves user feedback if given
if st.session_state['thumbs']!='':
    filename = 'output2.txt'
    outfile = open(filename, 'a',encoding="utf-8")
    
    outfile.write(str(st.session_state.thumbs)+'\n')
    outfile.write('\n------------------------------------------------END QUERY------------------------------------------------\n')

    outfile.close()
    st.session_state['thumbs']=''
    st.write("Saved your Feedback")





run_chat()

#shortens the short-term memory to only include previous 10 interactions
if len(st.session_state.st_memory)>10:
    st.session_state.st_memory = st.session_state.st_memory[:10]

