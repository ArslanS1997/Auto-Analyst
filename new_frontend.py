from agents import *
import streamlit as st
from retrievers import *
import os
import statsmodels.api as sm
from streamlit_feedback import streamlit_feedback
from llama_index.core import Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from io import StringIO
import traceback
import contextlib
import sys
import plotly as px
def reset_everything():
    st.cache_data.clear()






@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

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
dspy.configure(lm = dspy.OpenAI(model='gpt-4o-mini',api_key=os.environ['OPENAI_API_KEY'], max_tokens=16384))

# dspy.configure(lm =dspy.GROQ(model='llama3-70b-8192', api_key =os.environ.get("GROQ_API_KEY"),max_tokens=10000 ) )

Settings.embed_model = OpenAIEmbedding(api_key=os.environ["OPENAI_API_KEY"])

# with st.columns(3):
st.image('Auto-analysts icon small.png', width=70)
st.title("Auto-Analyst")
    
    # st.markdown("<h1 style='text-align: center; color: black;'>Auto-Analyst</h1>", unsafe_allow_html=True)


    # 
st.logo('Auto-analysts icon small.png')
st.sidebar.title(":white[Auto-Analyst] ")
st.sidebar.text("Have all your Data Science ")
st.sidebar.text("Analysis Done!")
uploaded_file = st.file_uploader("Upload your file here...", on_change=reset_everything())
st.write("You can upload your own data or use sample data by clicking the button below")
sample_data = st.button("Use Sample Data")
if sample_data:
    # temp_df = pd.read_csv("Housing.csv")
    # del uploaded_file
    uploaded_file = "Housing.csv"


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

st.markdown(instructions)


retrievers = {}
# df = pd.read_csv('open_deals_min2.csv')
@st.cache_data
def initialize_data(button_pressed=False):
    if button_pressed==False:
        uploaded_df = pd.read_csv(uploaded_file, parse_dates=True)
    else:
        uploaded_df = pd.read_csv("Housing.csv")
        st.write("LOADED")
    return uploaded_df



@st.cache_resource
def intialize_agent():

    return auto_analyst(agents=agent_names,retrievers=retrievers)

@st.cache_resource
def initial_agent_ind():
    return auto_analyst_ind(agents=agent_names,retrievers=retrievers)

# def initiatlize_retrievers():
@st.cache_data(hash_funcs={StringIO: StringIO.getvalue})
def initiatlize_retrievers(_styling_instructions, _doc):
    retrievers ={}
    style_index =  VectorStoreIndex.from_documents([Document(text=x) for x in _styling_instructions])
    retrievers['style_index'] = style_index
    retrievers['dataframe_index'] =  VectorStoreIndex.from_documents([Document(text=x) for x in _doc])
    # retrievers['st_memory_index'] = VectorStoreIndex.from_documents([Document(text="Initializing memory")])

    return retrievers
    
def save():
    # st.write("Saving")
    filename = 'output2.txt'
    # st.session_state.messages.append("This is user feedback"+str(st.session_state['thumbs']))
    outfile = open(filename, 'a')
    
    outfile.writelines([str(i)+'\n' for i in st.session_state.messages])
    outfile.close()


# Streamlit app
def run_chat():
    if 'df' not in st.session_state['df']:
        df = st.session_state['df']
        try:
            st.write(df.head(5))
        except:
            print("load df")
   


    # User input
    user_input = st.chat_input("Welcome to Auto-Analyst, How can I help you? You can use @agent_name call a specific agent or let the planner route the query!")
    # button = st.button("Submit Query")

    # Generate and display response
    # st.write(uploaded_file)
    if user_input:
        if st.session_state.messages!=[]:
         
            for m in st.session_state.messages:
                if '-------------------------' not in m:
                    st.write(m.replace('#','######'))






        st.session_state.messages.append('\n------------------------------------------------NEW QUERY------------------------------------------------\n')
        st.session_state.messages.append(f"User: {user_input}")
        
        specified_agents = []
        for a in agent_names: 
            if a.__pydantic_core_schema__['schema']['model_name'] in user_input.lower():
                specified_agents.insert(0,a.__pydantic_core_schema__['schema']['model_name'])
                # break
        if specified_agents==[]:



            # Generate response
            # conversation = Conversation(user_input)
            with st.chat_message("Auto-Anlyst Bot",avatar="🚀"):
                st.write("Responding to "+ user_input)
                output=st.session_state['agent_system_chat'](query=user_input)
                # st.session_state.previous_replies.append(output)
                # fig = px.line(x=[1,1,1,1], y=[1,1,1,1])
                execution = output['code_combiner_agent'].refined_complete_code.split('```')[1].replace('#','####').replace('python','')
                st.markdown(output['code_combiner_agent'].refined_complete_code)
                
                try:
                    
                    with stdoutIO() as s:
                        exec(execution)
                       
                    st.write(s.getvalue().replace('#','########'))

                    

                except:
                    # st.session_state['load'] =0

                    e = traceback.format_exc()
                    st.markdown("The code is giving an error on excution "+str(e)[:1500])
                    st.write("Please help the code fix agent with human understanding")
                    user_given_context = st.text_input("Help give additional context to guide the agent to fix the code", key='user_given_context')
                    st.session_state.messages.append(user_given_context)
        else:
            for spec_agent in specified_agents:
                with st.chat_message(spec_agent+" Bot",avatar="🚀"):
                    st.markdown("Responding to "+ user_input)
                    output=st.session_state['agent_system_chat_ind'](query=user_input, specified_agent=spec_agent)
                    # st.session_state.previous_replies.append(output)
                    # fig = px.line(x=[1,1,1,1], y=[1,1,1,1])
                    if len(output[spec_agent].code.split('```'))>1:
                        execution = output[spec_agent].code.split('```')[1].replace('#','####').replace('python','').replace('fig.show()','st.plotly_chart(fig)')
                    else:
                        execution = output[spec_agent].code.split('```')[0].replace('#','####').replace('python','').replace('fig.show()','st.plotly_chart(fig)')


                    # st.markdown(execution)

                    
                    try:
                        
                        with stdoutIO() as s:
                            exec(execution)
                    

                        st.write(s.getvalue().replace('#','########'))


                        

                    except:
                        # st.session_state['load'] =0

                        e = traceback.format_exc()
                        st.markdown("The code is giving an error on excution "+str(e)[:1500])
                        st.write("Please help the code fix agent with human understanding")
                        user_given_context = st.text_input("Help give additional context to guide the agent to fix the code", key='user_given_context')
                        st.session_state.messages.append(user_given_context)



        with st.form('form'):
            streamlit_feedback(feedback_type="thumbs", optional_text_label="Do you like the response?", align="flex-start")

            st.session_state.messages.append('\n---------------------------------------------------------------------------------------------------------\n')


            
            st.form_submit_button('Save feedback',on_click=save())
    # else:






        

        # bot_response = response

        # Append bot response to messages
        # st.session_state.messages.append(f"Bot: {bot_response}")

        # Clear input box
        

    # Display messages
    # for message in st.session_state.messages:
    #     st.markdown(message)
# intialize_duckDb()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thumbs" not in st.session_state:
    st.session_state.thumbs = ''
if "df" not in st.session_state:
    st.session_state.df = None
if "st_memory" not in st.session_state:
    st.session_state.st_memory = []

if uploaded_file or sample_data:
    # st.write(uploaded_file)
    st.session_state['df'] = initialize_data()
    
    st.write(st.session_state['df'].head())
    if sample_data:
        desc = "Housing Dataset"
        doc=[str(make_data(st.session_state['df'],desc))]
    else:
        desc = st.text_input("Write a description for the uploaded dataset")
        doc=['']
        if st.button("Start The Analysis"):

            dict_ = make_data(st.session_state['df'],desc)
            doc = [str(dict_)]

    if doc[0]!='':
        # st.write(styling_instructions)
        retrievers = initiatlize_retrievers(styling_instructions,doc)
        
        st.success('Document Uploaded Successfully!')
        st.session_state['agent_system_chat'] = intialize_agent()
        st.session_state['agent_system_chat_ind'] = initial_agent_ind()
        st.write("Begin")
    




if st.session_state['thumbs']!='':
    filename = 'output2.txt'
    # st.session_state.messages.append("This is user feedback"+str(st.session_state['thumbs']))
    outfile = open(filename, 'a',encoding="utf-8")
    
    outfile.write(str(st.session_state.thumbs)+'\n')
    outfile.write('\n------------------------------------------------END QUERY------------------------------------------------\n')

    outfile.close()
    st.session_state['thumbs']=''
    st.write("Saved your Feedback")





run_chat()
# st.write(df)

if len(st.session_state.st_memory)>10:
    st.session_state.st_memory = st.session_state.st_memory[:10]

