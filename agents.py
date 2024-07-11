import dspy
import streamlit as st



class analytical_planner(dspy.Signature):
    """ You are data analytics planner agent. You have access to three inputs
    1. Datasets
    2. Data Agent descriptions
    3. User-defined Goal
    You take these three inputs to develop a comprehensive plan to achieve the user-defined goal from the data & Agents available.
    In case you think the user-defined goal is infeasible you can ask the user to redefine or add more description to the goal.

    Give your output in this format:
    plan: Agent1->Agent2->Agent3
    plan_desc = Use Agent 1 for this reason, then agent2 for this reason and lastly agent3 for this reason.

    You don't have to use all the agents in response of the query
    
    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df,columns  set df as copy of df")
    Agent_desc = dspy.InputField(desc= "The agents available in the system")
    goal = dspy.InputField(desc="The user defined goal ")
    plan = dspy.OutputField(desc="The plan that would achieve the user defined goal", prefix='Plan:')
    plan_desc= dspy.OutputField(desc="The reasoning behind the chosen plan")

class goal_refiner_agent(dspy.Signature):
    """You take a user-defined goal given to a AI data analyst planner agent, 
    you make the goal more elaborate using the datasets available and agent_desc"""
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df,columns  set df as copy of df")
    Agent_desc = dspy.InputField(desc= "The agents available in the system")
    goal = dspy.InputField(desc="The user defined goal ")
    refined_goal = dspy.OutputField(desc='Refined goal that helps the planner agent plan better')

class preprocessing_agent(dspy.Signature):
    """ Given a user-defined analysis goal and a pre-loaded dataset df, 
    I will generate Python code using NumPy and Pandas to build an exploratory analytics pipeline.
      The goal is to simplify the preprocessing and introductory analysis of the dataset.

Task Requirements:

Identify and separate numeric and categorical columns into two lists: numeric_columns and categorical_columns.
Handle null values in the dataset, applying the correct logic for numeric and categorical columns.
Convert string dates to datetime format.
Create a correlation matrix that only includes numeric columns.
Use the correct column names according to the dataset.
Output:

The generated Python code should be concise, readable, and follow best practices for data preprocessing and introductory analysis. 
The code should be written using NumPy and Pandas libraries, and should not read the CSV file into the dataframe (it is already loaded as df).



    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df, column_names  set df as copy of df")
    goal = dspy.InputField(desc="The user defined goal could ")
    commentary = dspy.OutputField(desc="The comments about what analysis is being performed")
    code = dspy.OutputField(desc ="The code that does the data preprocessing and introductory analysis")


class statistical_analytics_agent(dspy.Signature):
    """ You are a statistical analytics agent. 
    Your task is to take a dataset and a user-defined goal, and output 
    Do not add data visualization code
    Always handle strings as categorical variables in a regression
    use statsmodel C(string_column) in the line equation
    Python code that performs the appropriate statistical analysis to achieve that goal.
    You should use the Python statsmodel library
    You must also set period x while doing seasonal decompose, also make sure observation numbers work
    Convert X, Y into float when fitting model using something similar to this
    sm.MODEL(y.astype(float), X.astype(float))
    Use, categorical when dealing with strings

    Make sure your output is as intended!

    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df,columns  set df as copy of df")
    goal = dspy.InputField(desc="The user defined goal for the analysis to be performed")
    commentary = dspy.OutputField(desc="The comments about what analysis is being performed")
    code = dspy.OutputField(desc ="The code that does the statistical analysis using statsmodel")

class sk_learn_agent(dspy.Signature):
    """You are a machine learning agent. 
    Your task is to take a dataset and a user-defined goal, and output Python code that performs the appropriate machine learning analysis to achieve that goal. 
    You should use the scikit-learn library.


    Make sure your output is as intended!
    
    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df,columns. set df as copy of df")
    goal = dspy.InputField(desc="The user defined goal ")
    commentary = dspy.OutputField(desc="The comments about what analysis is being performed")
    code = dspy.OutputField(desc ="The code that does the Exploratory data analysis")
    
    
class story_teller_agent(dspy.Signature):
    """ You are a story teller agent, taking output from different data analytics agents, you compose a compelling story for what was done """
    agent_analysis_list =dspy.InputField(desc="A list of analysis descriptions from every agent")
    story = dspy.OutputField(desc="A coherent story combining the whole analysis")

class code_combiner_agent(dspy.Signature):
    """ You are a code combine agent, taking Python code output from many agents and combining the operations into 1 output
    You also fix any errors in the code. Also handle if a column has more than 10 categories, by combining the rest into one called `other`

    Double check column_names/dtypes using dataset, also check if applied logic works for the datatype

    Make sure your output is as intended!
    
    """
    dataset = dspy.InputField(desc="Use this double check column_names, data types")
    agent_code_list =dspy.InputField(desc="A list of code given by each agent")
    refined_complete_code = dspy.OutputField(desc="Refined complete code base")
    
    
class data_viz_agent(dspy.Signature):
    """
    You are AI agent who uses the goal to generate data visualizations in Plotly.
    You have to use the tools available to your disposal
    If row_count of dataset > 50000, use sample while visualizing 
    Only this agent does the visualization
    Also only use x_axis/y_axis once in update layout
    {dataset}
    {styling_index}

    You must give an output as code, in case there is no relevant columns, just state that you don't have the relevant information

    Make sure your output is as intended!
    """
    goal = dspy.InputField(desc="user defined goal which includes information about data and chart they want to plot")
    dataset = dspy.InputField(desc=" Provides information about the data in the data frame. Only use column names and dataframe_name as in this context")
    styling_index = dspy.InputField(desc='Provides instructions on how to style your Plotly plots')
    commentary = dspy.OutputField(desc="The comments about what analysis is being performed")
    
    code= dspy.OutputField(desc="Plotly code that visualizes what the user needs according to the query & dataframe_index & styling_context")

class code_fix(dspy.Signature):
    """
    You are an AI which fixes the data analytics code from another agent, your fixed code should only fix the faulty part of the code, rest should remain the same
    You take the faulty code, and the error generated and generate the fixed code that performs the exact analysis the faulty code intends to do
    You are also give user given context that guides you how to fix the code!
    Return not just the fixed code but the fixed code base! Do not ignore this!

    please reflect on the errors of the AI agent and then generate a 
   correct step-by-step solution to the problem.

    """
    faulty_code = dspy.InputField(desc="The faulty code that did not work")
    user_provided_context = dspy.InputField(desc="User adds additional context that might help solve the problem")
    error = dspy.InputField(desc="The error generated")

    faulty_code = dspy.OutputField(desc="Only include the faulty code here")
    fixed_code= dspy.OutputField(desc="The fixed code")


class auto_analyst(dspy.Module):
    def __init__(self,agents,retrievers):
       

        self.agents = {}
        self.agent_inputs ={}
        self.agent_desc =[]
        i =0
        for a in agents:
            name = a.__pydantic_core_schema__['schema']['model_name']
            self.agents[name] = dspy.ChainOfThought(a)
            self.agent_inputs[name] ={x.strip() for x in str(agents[i].__pydantic_core_schema__['cls']).split('->')[0].split('(')[1].split(',')}
            self.agent_desc.append(str(a.__pydantic_core_schema__['cls']))
            i+=1
            

        self.planner = dspy.ChainOfThought(analytical_planner)
        self.refine_goal = dspy.ChainOfThought(goal_refiner_agent)
        self.code_combiner_agent = dspy.ChainOfThought(code_combiner_agent)
        self.story_telleer = dspy.ChainOfThought(story_teller_agent)
        
        self.dataset = retrievers['dataframe_index'].as_retriever(k=1)
        self.styling_index = retrievers['style_index'].as_retriever(similarity_top_k=1)
        
    def forward(self, query):
        dict_ ={}
        
        dict_['dataset'] = self.dataset.retrieve(query)[0].text
        dict_['styling_index'] = self.styling_index.retrieve(query)[0].text
        dict_['goal']=query
        dict_['Agent_desc'] = str(self.agent_desc)
        percent_complete =0
        output_dict ={}
        my_bar = st.progress(0, text="**Planner Agent Working on devising a plan**")
        plan = self.planner(goal =dict_['goal'], dataset=dict_['dataset'], Agent_desc=dict_['Agent_desc'] )
        st.write("**This is the proposed plan**")
        # st.write(plan.plan)
        len_ = len(plan.plan.split('->'))+2
        percent_complete += 1/len_
        my_bar.progress(percent_complete, text=" Delegating to Agents")


        output_dict['analytical_planner'] = plan
        plan_list =[]
        code_list =[]
        analysis_list = [plan.plan,plan.plan_desc]
        # arrow_count = len(plan.plan.split('->'))
        if plan.plan.split('->'):
            plan_text = plan.plan
            plan_text = plan.plan.replace('Plan','').replace(':','').strip()
            st.write(plan_text)
            st.write(plan.plan_desc)
            plan_list = plan_text.split('->')
        else:
            refined_goal = self.refine_goal(dataset=dict_['dataset'], goal=dict_['goal'], Agent_desc= dict_['Agent_desc'])
            forward(query=refined_goal)

        for p in plan_list:
            inputs = {x:dict_[x] for x in self.agent_inputs[p.strip()]}
            output_dict[p.strip()]=self.agents[p.strip()](**inputs)
            # st.write("This is the "+p.strip())
            code = output_dict[p.strip()].code
            # st.write("This is the generated Code"+ code)
            commentary = output_dict[p.strip()].commentary
            st.write('**'+p.strip().capitalize().replace('_','  ')+' -  is working on this analysis....**')
            st.write(commentary.replace('#',''))
            percent_complete += 1/len_
            my_bar.progress(percent_complete)
            code_list.append(code)
            analysis_list.append(commentary)
        output_dict['code_combiner_agent'] = self.code_combiner_agent(agent_code_list = str(code_list), dataset=dict_['dataset'])
        my_bar.progress(percent_complete + 1/len_, text=" Combining WorkFlow")
        # st.markdown(output_dict)
        output_dict['story_teller_agent'] = self.story_telleer(agent_analysis_list = str(analysis_list))
        my_bar.progress(100, text=" Compiling the story")
        
        return output_dict
        