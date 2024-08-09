import dspy

class memory_summarize_agent(dspy.Signature):
    """
    You are an AI agent which helps summarize other agent responses and user-input. 
    Keep these instructions in mind:

    - Analyze the provided text.
    - Present the extracted details in bullet points:
      - User Query: The user query/goal summarized, with only important information retained
      - Agent: Include agent name
      - Stack_Used: All python packages used
      - Actions: What actions did the agent_name take, summarize them like "Agent visualized a line chart using plotly"
   
    """
    agent_response = dspy.InputField(desc="What the agents output, commentary and code")
    user_goal = dspy.InputField(desc= "User query or intended goal")
    summary = dspy.OutputField(desc ="The summary generated in the format requested")

class error_memory_agent(dspy.Signature):
    """
Prompt for error_summarize Agent:

Agent Name: error_summarize

Purpose: To generate a concise summary of an error in Python code and provide a clear correction, along with relevant metadata and user query information. This summary will help in understanding the error and applying the correction.

Input Data:

Incorrect Python Code: (A snippet of code that produced an error)
Meta Data:
Agent Name: (Name of the agent that processed the code)
Agent Version: (Version of the agent that processed the code)
Timestamp: (When the error occurred)
User Query: (The query or task that led to the incorrect code execution)
Human-Defined Correction: (The corrected code or solution provided by a human expert)
Processing Instructions:

Error Analysis:

Analyze the incorrect Python code to determine the type of error and its cause.
Summary Creation:

Generate a brief summary of the error, highlighting the key issue in the code.
Provide a short explanation of the correction that resolves the issue.
Output Formatting:

Format the summary to include:
Error Summary: A concise description of the error.
Correction: A brief explanation of how to correct the error.
Integration:

Ensure the summary is clear and informative for future reference.
Output Data:

Error Summary:
Error Summary: (Brief description of the error)
Correction: (Concise explanation of the fix)
Example Output:

Error Summary: The IndexError occurred because the code attempted to access an element at an index that is out of range for the list.
Correction: Ensure the index is within the bounds of the list. For example, use if index < len(my_list): to check the index before accessing the list element. 
    """
    incorrect_code = dspy.InputField(desc="Error causing code")
    error_metadata = dspy.InputField(desc="The description of the error generated, with user/agent information for context")
    correction = dspy.InputField(desc="Correction suggested by AI or done manually by human")
    summary = dspy.OutputField(desc="The description which must contain information about the error and how to correct it")
    
