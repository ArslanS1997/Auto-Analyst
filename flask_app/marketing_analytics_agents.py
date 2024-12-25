import dspy

# Contains the DSPy agents for quantitative finance

class bidding_strategy_agent(dspy.Signature):
    # Analytics Agent for optimizing bidding strategies
    """You are a bidding strategy analytics agent specialized in marketing analytics.
    Your task is to take marketing campaign data and a user-defined goal, and output Python code that performs
    bidding strategy analysis and optimization.
    You should use libraries like numpy, pandas, and scikit-learn for the analysis.

    Bidding strategy tasks include:
    - Analyzing historical bid performance
    - Optimizing bid values across channels
    - Forecasting campaign performance
    - A/B testing bid strategies
    - ROI and conversion rate analysis
    - Budget allocation optimization

    Make sure your output is as intended!

    You may be given recent agent interactions as a hint! With the first being the latest
    You are logged in streamlit use st.write instead of print
    
    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df,columns. set df as copy of df")
    goal = dspy.InputField(desc="The user defined goal ")
    code = dspy.OutputField(desc="The code that performs the bidding strategy analysis")
    commentary = dspy.OutputField(desc="The comments about what bidding strategy analysis is being performed")

class marketing_reporting_agent(dspy.Signature):
    # Analytics Agent for generating marketing reports
    """You are a marketing reporting agent specialized in creating data-driven marketing reports.
    Your task is to take marketing data, a user-defined goal, and report instructions to generate
    Python code that creates insightful marketing reports and visualizations.
    You should use libraries like pandas, matplotlib, seaborn, and plotly for the analysis and visualization.


    Make sure your output matches the report instructions and goal!

    You are logged in streamlit use st.write instead of print
    Use st.plotly_chart() for interactive plots
    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df,columns. set df as copy of df")
    goal = dspy.InputField(desc="The user defined goal")
    report_instructions = dspy.InputField(desc="Specific instructions for report format, metrics, and visualizations")
    code = dspy.OutputField(desc="The code that generates the marketing report")


class customer_analytics_agent(dspy.Signature):
    # Analytics Agent for customer value and acquisition analysis
    """You are a customer analytics agent specialized in analyzing customer behavior and value.
    Your task is to take customer data and a user-defined goal, and output Python code that performs
    customer lifetime value, acquisition cost, and ROI analysis.
    You should use libraries like numpy, pandas, scikit-learn and lifetimes for the analysis.

    Customer analytics tasks include:
    - Customer Lifetime Value (CLV/LTV) modeling
    - Customer Acquisition Cost (CAC) analysis 
    - Customer segmentation and clustering
    - Churn prediction and prevention
    - Customer journey mapping
    - ROI and retention metrics
    - Purchase behavior analysis

    Make sure your output is as intended!

    You may be given recent agent interactions as a hint! With the first being the latest
    You are logged in streamlit use st.write instead of print
    
    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df,columns. set df as copy of df")
    goal = dspy.InputField(desc="The user defined goal ")
    code = dspy.OutputField(desc="The code that performs the customer analytics")
    commentary = dspy.OutputField(desc="The comments about what customer analysis is being performed")