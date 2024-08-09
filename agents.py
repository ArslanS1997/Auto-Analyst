import dspy
import streamlit as st
import memory_agents as m


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

The generated Python code should be concise, readable, and follow best practices for data preprocessing and introductory analysis. 
The code should be written using NumPy and Pandas libraries, and should not read the CSV file into the dataframe (it is already loaded as df).
When splitting numerical and categorical use this script:

categorical_columns = df.select_dtypes(include=[object, 'category']).columns.tolist()
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

DONOT 

Use this to handle conversion to Datetime
def safe_to_datetime(date):
    try:
        return pd.to_datetime(date,errors='coerce', cache=False)
    except (ValueError, TypeError):
        return pd.NaT

df['datetime_column'] = df['datetime_column'].apply(safe_to_datetime)

You may be give recent agent interactions as a hint!



    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df, column_names  set df as copy of df")
    goal = dspy.InputField(desc="The user defined goal could ")
    commentary = dspy.OutputField(desc="The comments about what analysis is being performed")
    code = dspy.OutputField(desc ="The code that does the data preprocessing and introductory analysis")


class statistical_analytics_agent(dspy.Signature):
    """ 
    You are a statistical analytics agent. Your task is to take a dataset and a user-defined goal and output Python code that performs the appropriate statistical analysis to achieve that goal. Follow these guidelines:

Data Handling:

    Always handle strings as categorical variables in a regression using statsmodels C(string_column).
    Do not change the index of the DataFrame.
    Convert X and y into float when fitting a model.
Error Handling:

    Always check for missing values and handle them appropriately.
    Ensure that categorical variables are correctly processed.
    Provide clear error messages if the model fitting fails.
Regression:

    For regression, use statsmodels and ensure that a constant term is added to the predictor using sm.add_constant(X).
    Handle categorical variables using C(column_name) in the model formula.
    Fit the model with model = sm.OLS(y.astype(float), X.astype(float)).fit().
Seasonal Decomposition:

    Ensure the period is set correctly when performing seasonal decomposition.
    Verify the number of observations works for the decomposition.
Output:

    Ensure the code is executable and as intended.
    Also choose the correct type of model for the problem
    Avoid adding data visualization code.

Use code like this to prevent failing:
import pandas as pd
import numpy as np
import statsmodels.api as sm

def statistical_model(X, y, goal, period=None):
    try:
        # Check for missing values and handle them
        X = X.dropna()
        y = y.loc[X.index].dropna()

        # Ensure X and y are aligned
        X = X.loc[y.index]

        # Convert categorical variables
        for col in X.select_dtypes(include=['object', 'category']).columns:
            X[col] = X[col].astype('category')

        # Add a constant term to the predictor
        X = sm.add_constant(X)

        # Fit the model
        if goal == 'regression':
            # Handle categorical variables in the model formula
            formula = 'y ~ ' + ' + '.join([f'C({col})' if X[col].dtype.name == 'category' else col for col in X.columns])
            model = sm.OLS(y.astype(float), X.astype(float)).fit()
            return model.summary()

        elif goal == 'seasonal_decompose':
            if period is None:
                raise ValueError("Period must be specified for seasonal decomposition")
            decomposition = sm.tsa.seasonal_decompose(y, period=period)
            return decomposition

        else:
            raise ValueError("Unknown goal specified. Please provide a valid goal.")

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage:
result = statistical_analysis(X, y, goal='regression')
print(result)


    You may be give recent agent interactions as a hint! With the first being the latest

    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df,columns  set df as copy of df")
    goal = dspy.InputField(desc="The user defined goal for the analysis to be performed")
    code = dspy.OutputField(desc ="The code that does the statistical analysis using statsmodel")
    commentary = dspy.OutputField(desc="The comments about what analysis is being performed")
    

class sk_learn_agent(dspy.Signature):
    """You are a machine learning agent. 
    Your task is to take a dataset and a user-defined goal, and output Python code that performs the appropriate machine learning analysis to achieve that goal. 
    You should use the scikit-learn library.


    Make sure your output is as intended!

    You may be give recent agent interactions as a hint! With the first being the latest

    
    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df,columns. set df as copy of df")
    goal = dspy.InputField(desc="The user defined goal ")
    code = dspy.OutputField(desc ="The code that does the Exploratory data analysis")
    commentary = dspy.OutputField(desc="The comments about what analysis is being performed")
    
    
    
class story_teller_agent(dspy.Signature):
    """ You are a story teller agent, taking output from different data analytics agents, you compose a compelling story for what was done """
    agent_analysis_list =dspy.InputField(desc="A list of analysis descriptions from every agent")
    story = dspy.OutputField(desc="A coherent story combining the whole analysis")

class code_combiner_agent(dspy.Signature):
    """ You are a code combine agent, taking Python code output from many agents and combining the operations into 1 output
    You also fix any errors in the code. 


    Double check column_names/dtypes using dataset, also check if applied logic works for the datatype
    df.copy = df.copy()
    Change print to st.write
    Also add this to display Plotly chart
    st.plotly_chart(fig, use_container_width=True)



    Make sure your output is as intended!
        You may be give recent agent interactions as a hint! With the first being the latest


    """
    dataset = dspy.InputField(desc="Use this double check column_names, data types")
    agent_code_list =dspy.InputField(desc="A list of code given by each agent")
    refined_complete_code = dspy.OutputField(desc="Refined complete code base")
    
    
class data_viz_agent(dspy.Signature):
    """
    You are AI agent who uses the goal to generate data visualizations in Plotly.
    You have to use the tools available to your disposal
    If row_count of dataset > 50000, use sample while visualizing 
    use this
    if len(df)>50000:
        .......
    Only this agent does the visualization
    Also only use x_axis/y_axis once in update layout
    {dataset}
    {styling_index}

    You must give an output as code, in case there is no relevant columns, just state that you don't have the relevant information
    
    Make sure your output is as intended! DO NOT OUTPUT THE DATASET/STYLING INDEX 
    ONLY OUTPUT THE CODE AND COMMENTARY. ONLY USE ONE OF THESE 'K','M' or 1,000/1,000,000. NOT BOTH

    You may be give recent agent interactions as a hint! With the first being the latest
    DONT INCLUDE GOAL/DATASET/STYLING INDEX IN YOUR OUTPUT!
    You can add trendline into a scatter plot to show it changes,only if user mentions for it in the query!
    """
    goal = dspy.InputField(desc="user defined goal which includes information about data and chart they want to plot")
    dataset = dspy.InputField(desc=" Provides information about the data in the data frame. Only use column names and dataframe_name as in this context")
    styling_index = dspy.InputField(desc='Provides instructions on how to style your Plotly plots')
    code= dspy.OutputField(desc="Plotly code that visualizes what the user needs according to the query & dataframe_index & styling_context")

    commentary = dspy.OutputField(desc="The comments about what analysis is being performed, this should not include code")
    
    

class code_fix(dspy.Signature):
    """
    You are an AI which fixes the data analytics code from another agent, your fixed code should only fix the faulty part of the code, rest should remain the same
    You take the faulty code, and the error generated and generate the fixed code that performs the exact analysis the faulty code intends to do
    You are also give user given context that guides you how to fix the code!


    please reflect on the errors of the AI agent and then generate a 
   correct step-by-step solution to the problem.

    """
    faulty_code = dspy.InputField(desc="The faulty code that did not work")
    previous_code_fixes = dspy.InputField(desc="User adds additional context that might help solve the problem")
    error = dspy.InputField(desc="The error generated")

    faulty_code = dspy.OutputField(desc="Only include the faulty code here")
    fixed_code= dspy.OutputField(desc="The fixed code")


class auto_analyst_ind(dspy.Module):
    def __init__(self,agents,retrievers):
       

        self.agents = {}
        self.agent_inputs ={}
        self.agent_desc =[]
        i =0
        for a in agents:
            name = a.__pydantic_core_schema__['schema']['model_name']
            self.agents[name] = dspy.ChainOfThoughtWithHint(a)
            self.agent_inputs[name] ={x.strip() for x in str(agents[i].__pydantic_core_schema__['cls']).split('->')[0].split('(')[1].split(',')}
            self.agent_desc.append(str(a.__pydantic_core_schema__['cls']))
            i+=1
            

        self.planner = dspy.ChainOfThoughtWithHint(analytical_planner)
        self.refine_goal = dspy.ChainOfThoughtWithHint(goal_refiner_agent)
        self.code_combiner_agent = dspy.ChainOfThoughtWithHint(code_combiner_agent)
        self.story_teller = dspy.ChainOfThoughtWithHint(story_teller_agent)
        self.memory_summarize_agent = dspy.ChainOfThought(m.memory_summarize_agent)
        
        self.dataset = retrievers['dataframe_index'].as_retriever(k=1)
        self.styling_index = retrievers['style_index'].as_retriever(similarity_top_k=1)


    def forward(self, query, specified_agent):
        
        # output_dict 
        dict_ ={}
        
        dict_['dataset'] = self.dataset.retrieve(query)[0].text
        dict_['styling_index'] = self.styling_index.retrieve(query)[0].text
        dict_['hint'] = st.session_state.st_memory
        dict_['goal']=query
        dict_['Agent_desc'] = str(self.agent_desc)
        st.write(f"User choose this {specified_agent} to answer this ")


        inputs = {x:dict_[x] for x in self.agent_inputs[specified_agent.strip()]}
        inputs['hint'] = str(dict_['hint']).replace('[','').replace(']','')
        # st.write(inputs['hint'])
        output_dict ={}
        output_dict[specified_agent.strip()]=self.agents[specified_agent.strip()](**inputs)
        for x in dict(output_dict[specified_agent.strip()]).keys():
            if x!='rationale':
                st.code(f"{specified_agent.strip()}[{x}]: {str(dict(output_dict[specified_agent.strip()])[x]).replace('#','#######')}")
                st.session_state.messages.append(f"{specified_agent.strip()}[{x}]: {str(dict(output_dict[specified_agent.strip()])[x])}")
        
        output_dict['memory_'+specified_agent.strip()] = str(self.memory_summarize_agent(agent_response=specified_agent+' '+output_dict[specified_agent.strip()]['code']+'\n'+output_dict[specified_agent.strip()]['commentary'], user_goal=query).summary)
        st.session_state.st_memory.insert(0,f"{'memory_'+specified_agent.strip()} : {output_dict['memory_'+specified_agent.strip()]}")


        return output_dict






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
        self.story_teller = dspy.ChainOfThought(story_teller_agent)
        self.memory_summarize_agent = dspy.ChainOfThought(m.memory_summarize_agent)
        
        self.dataset = retrievers['dataframe_index'].as_retriever(k=1)
        self.styling_index = retrievers['style_index'].as_retriever(similarity_top_k=1)
        
    def forward(self, query):
        dict_ ={}
        
        dict_['dataset'] = self.dataset.retrieve(query)[0].text
        dict_['styling_index'] = self.styling_index.retrieve(query)[0].text
        dict_['goal']=query
        dict_['Agent_desc'] = str(self.agent_desc)
        dict_['hint'] = st.session_state.st_memory
        percent_complete =0
        output_dict ={}
        my_bar = st.progress(0, text="**Planner Agent Working on devising a plan**")
        plan = self.planner(goal =dict_['goal'], dataset=dict_['dataset'], Agent_desc=dict_['Agent_desc'] )
        st.write("**This is the proposed plan**")
        st.session_state.messages.append(f"planner['plan']: {plan['plan']}")
        st.session_state.messages.append(f"planner['plan_desc']: {plan['plan_desc']}")

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
            st.session_state.messages.append(f"refined_goal: {refined_goal.refined_goal}")

            self.forward(query=refined_goal.refined_goal)

        for p in plan_list:
            inputs = {x:dict_[x] for x in self.agent_inputs[p.strip()]}
            output_dict[p.strip()]=self.agents[p.strip()](**inputs)
            # st.write("This is the "+p.strip())
            code = output_dict[p.strip()].code
            
            # st.write("This is the generated Code"+ code)
            commentary = output_dict[p.strip()].commentary
            st.write('**'+p.strip().capitalize().replace('_','  ')+' -  is working on this analysis....**')
            st.session_state.messages.append(f"{p.strip()}['code']: {output_dict[p.strip()].code}")
            st.session_state.messages.append(f"{p.strip()}['commentary']: {output_dict[p.strip()].commentary}")


            st.write(commentary.replace('#',''))
            st.code(code)
            percent_complete += 1/len_
            my_bar.progress(percent_complete)
            code_list.append(code)
            analysis_list.append(commentary)
        st.write("Combining all code into one")
        output_dict['code_combiner_agent'] = self.code_combiner_agent(agent_code_list = str(code_list), dataset=dict_['dataset'])
        st.session_state.messages.append(f"code_combiner_agent: {output_dict['code_combiner_agent']}")
        my_bar.progress(percent_complete + 1/len_, text=" Combining WorkFlow")
        # st.markdown(output_dict)
        # output_dict['story_teller_agent'] = self.story_teller(agent_analysis_list = str(analysis_list))
        # st.session_state.messages.append(f"story_teller_agent: {output_dict['story_teller_agent']}")
        my_bar.progress(100, text=" Compiling the story")
        output_dict['memory_combined'] = str(self.memory_summarize_agent(agent_response='code_combiner_agent'+'\n'+str(output_dict['code_combiner_agent'].refined_complete_code), user_goal=query).summary)
        st.session_state.st_memory.insert(0,f"{'memory_'+specified_agent.strip()} : {output_dict['memory_'+specified_agent.strip()]}")

        return output_dict
