from agents import *
import streamlit as st
from retrievers import *
import os
from streamlit_feedback import streamlit_feedback
from llama_index.core import Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from io import StringIO
import traceback
import contextlib
import sys
import plotly as px

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old



# Load the pre-trained conversational model
agent_names= [data_viz_agent,sk_learn_agent,statistical_analytics_agent,preprocessing_agent]
dspy.configure(lm = dspy.OpenAI(model='gpt-4o-mini',api_key=os.environ['OPENAI_API_KEY'], max_tokens=4096))

# dspy.configure(lm =dspy.GROQ(model='llama3-70b-8192', api_key =os.environ.get("GROQ_API_KEY"),max_tokens=10000 ) )

Settings.embed_model = OpenAIEmbedding(api_key=os.environ["OPENAI_API_KEY"])
st.title("Auto-Analyst - Let the AI do all the heavy lifting")
st.sidebar.title("Auto-Analyst")
st.sidebar.text("Have all your Data Sciences Analysis Done!")
uploaded_file = st.file_uploader("Upload your file here...")
retrievers = {}
# df = pd.read_csv('open_deals_min2.csv')
@st.cache_data
def initialize_data():
    # if uploaded_file:
    # doc =['']
    uploaded_df = pd.read_csv(uploaded_file, parse_dates=True)
    return uploaded_df



@st.cache_resource 
def intialize_agent():

    return auto_analyst(agents=agent_names,retrievers=retrievers)



# def initiatlize_retrievers():
@st.cache_data(hash_funcs={StringIO: StringIO.getvalue})
def initiatlize_retrievers(_styling_instructions, _doc):
    retrievers ={}
    style_index =  VectorStoreIndex.from_documents([Document(text=x) for x in _styling_instructions])
    retrievers['style_index'] = style_index
    retrievers['dataframe_index'] =  VectorStoreIndex.from_documents([Document(text=x) for x in _doc])

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
   
    # st.image('logo.png', width=150)

    # st.sidebar.text(" RevTech tools!")
    # st.logo('logo.jpg')



    # User input
    user_input = st.chat_input("Welcome to Auto-Analyst, How can I help you? Ask me about deals")
    # button = st.button("Submit Query")

    # Generate and display response
    if user_input and uploaded_file:
        # Append user input to messages

        st.session_state.messages.append('\n------------------------------------------------NEW QUERY------------------------------------------------\n')
        st.session_state.messages.append(f"User: {user_input}")

        # Generate response
        # conversation = Conversation(user_input)
        with st.chat_message("Auto-Anlyst Bot",avatar="🚀"):
            st.write("Responding to "+ user_input)
            output=st.session_state['agent_system_chat'](query=user_input)
            # fig = px.line(x=[1,1,1,1], y=[1,1,1,1])
            execution = output['code_combiner_agent'].refined_complete_code.split('```')[1].replace('#','####').replace('python','')
            st.markdown(output['code_combiner_agent'].refined_complete_code)
            
            try:
                
                with stdoutIO() as s:
                    exec(execution)
                    # if len(output['code_combiner_agent'].refined_complete_code.split('```'))>1:
                    #     exec(output['code_combiner_agent'].refined_complete_code.split('```')[1].replace('python','').replace('Python','').replace('```',''))
                    # elif len(output['code_combiner_agent'].refined_complete_code.split('```'))==0:
                    #     exec(output['code_combiner_agent'].refined_complete_code.split('```')[0].replace('python','').replace('Python','').replace('```',''))

                st.markdown(s.getvalue().replace('#','########'))
                if 'fig' in output['code_combiner_agent'].refined_complete_code:
                    st.plotly_chart(fig)
                

            except:
                # st.session_state['load'] =0

                e = traceback.format_exc()
                st.markdown("The code is giving an error on excution "+str(e)[:1500])
                st.write("Please help the code fix agent with human understanding")
                user_given_context = st.text_input("Help give additional context to guide the agent to fix the code", key='user_given_context')
                st.session_state.messages.append(user_given_context)


        with st.form('form'):
            streamlit_feedback(feedback_type="thumbs", optional_text_label="Do you like the response?", align="flex-start")
                # st.session_state.messages.append(str(st.session_state['thumbs']))
            # if feedback:
            #     st.write("Saving feedback")
            #     st.messages.append("This is user feedback"+str(feedback))
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



if uploaded_file:

    df = initialize_data()
    st.session_state['df'] = df
    st.write(df.head())
    desc = st.text_input("Write a description for the uploaded dataset")
    doc=['']
    if st.button("Upload Data"):
        dict_ = make_data(df,desc)
        doc = [str(dict_)]

    if doc[0]!='':
        # st.write(styling_instructions)
        retrievers = initiatlize_retrievers(styling_instructions,doc)
        
        st.write('Document Uploaded Successfully!')
        st.session_state['agent_system_chat'] = intialize_agent()
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



# st.write(st.session_state)


