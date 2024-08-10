

## Documentation for `agents.py`

The `agents.py` file contains the definitions for various DSPy agents used in the Auto-Analyst system. Each agent is responsible for a specific aspect of data analysis or processing. The agents are implemented using DSPy signatures, which define their inputs and outputs.

### Agents

#### `analytical_planner`

- **Description**: The `analytical_planner` agent is responsible for routing queries to appropriate agents based on the user-defined goal, available datasets, and descriptions of available agents. It creates a comprehensive plan to achieve the goal by determining the sequence of agents to be used.

- **Inputs**:
  - `dataset`: The datasets available in the system. It should be used as a copy of the DataFrame.
  - `Agent_desc`: Descriptions of the agents available in the system.
  - `goal`: The user-defined goal that needs to be achieved.

- **Outputs**:
  - `plan`: A string representing the sequence of agents to be used (e.g., "Agent1->Agent2->Agent3").
  - `plan_desc`: A description of the reasoning behind the chosen plan, explaining why each agent was selected.

- **Purpose**: Develops a detailed plan for achieving the user-defined goal using the available agents and datasets. The output format includes a plan and an explanation for why each agent is included.

#### `goal_refiner_agent`

- **Description**: The `goal_refiner_agent` refines a user-defined goal to make it more detailed and actionable. It uses the available datasets and agent descriptions to enhance the goal, making it easier for the `analytical_planner` to create an effective plan.

- **Inputs**:
  - `dataset`: The datasets available in the system, used as a copy of the DataFrame.
  - `Agent_desc`: Descriptions of the agents available in the system.
  - `goal`: The initial user-defined goal.

- **Outputs**:
  - `refined_goal`: A more detailed and refined version of the user-defined goal, which aids the planning process.

- **Purpose**: Enhances the clarity and detail of the user-defined goal to improve the effectiveness of the planning process.

#### `preprocessing_agent`

- **Description**: The `preprocessing_agent` performs data preprocessing tasks such as cleaning, creating new columns, and handling null values. It generates Python code for exploratory data analysis using NumPy and Pandas.

- **Inputs**:
  - `dataset`: The dataset loaded in the system. It should be used as a copy of the DataFrame.
  - `goal`: The user-defined goal related to data preprocessing.

- **Outputs**:
  - `code`: Python code for data preprocessing and introductory analysis.
  - `commentary`: Comments about the analysis being performed and the preprocessing steps.

- **Purpose**: Simplifies and performs preprocessing tasks on the dataset based on the user-defined goal. The generated code handles tasks like separating numeric and categorical columns, handling null values, and converting dates to datetime format.

- **Notes**:
  - **Numeric and Categorical Columns**: Identifies and separates numeric and categorical columns.
  - **Null Values**: Handles null values appropriately for different column types.
  - **Date Conversion**: Uses a safe conversion method for datetime columns.
  - **Correlation Matrix**: Creates a correlation matrix for numeric columns.
  - **Best Practices**: The code should follow best practices and use NumPy and Pandas libraries. It should not include CSV reading as the DataFrame is already loaded.



#### `statistical_analytics_agent`

- **Description**: The `statistical_analytics_agent` performs statistical analysis on a dataset based on a user-defined goal. It uses the `statsmodels` package to build and fit statistical models, handling tasks such as regression and seasonal decomposition.

- **Inputs**:
  - `dataset`: The dataset available in the system, used as a copy of the DataFrame.
  - `goal`: The user-defined goal for the analysis (e.g., 'regression' or 'seasonal_decompose').

- **Outputs**:
  - `code`: Python code that performs the statistical analysis using the `statsmodels` library.
  - `commentary`: Comments describing the analysis being performed and any relevant details.

- **Purpose**: Generates code for statistical analysis tasks. For regression, it adds a constant term and handles categorical variables. For seasonal decomposition, it ensures that the period is correctly set.

- **Guidelines**:
  - **Data Handling**: Strings should be treated as categorical variables, and indices should not be changed.
  - **Error Handling**: Check for missing values and handle them appropriately. Provide clear error messages if model fitting fails.
  - **Regression**: Use `sm.add_constant(X)` for adding a constant term and handle categorical variables with `C(column_name)`.
  - **Seasonal Decomposition**: Ensure the period is specified and verify the number of observations.
  - **Code Execution**: Avoid including data visualization code and ensure the output is executable.

#### `sk_learn_agent`

- **Description**: The `sk_learn_agent` performs machine learning tasks using the `scikit-learn` library based on the user-defined goal. It generates Python code for machine learning analyses.

- **Inputs**:
  - `dataset`: The dataset available in the system, used as a copy of the DataFrame.
  - `goal`: The user-defined goal for the machine learning task.

- **Outputs**:
  - `code`: Python code that performs the machine learning analysis using `scikit-learn`.
  - `commentary`: Comments describing the machine learning analysis being performed and any relevant details.

- **Purpose**: Generates code for machine learning tasks using `scikit-learn`. The code should be executable and tailored to the specified goal.

#### `story_teller_agent`

- **Description**: The `story_teller_agent` creates a coherent narrative or story from the outputs of various data analytics agents. It combines the results and analyses into a comprehensive and engaging summary.

- **Inputs**:
  - `agent_analysis_list`: A list of analysis descriptions from various data analytics agents.

- **Outputs**:
  - `story`: A coherent and compelling story that integrates all the analyses performed by the different agents.

- **Purpose**: Composes a narrative that synthesizes the outputs from different agents, providing a cohesive story about the overall analysis.



#### `code_combiner_agent`

- **Description**: The `code_combiner_agent` combines Python code from multiple agents into a single script. It also refines and fixes any errors in the combined code.

- **Inputs**:
  - `dataset`: The dataset used for double-checking column names and data types.
  - `agent_code_list`: A list of code snippets provided by different agents.

- **Outputs**:
  - `refined_complete_code`: The refined and complete code that combines operations from all agents.

- **Purpose**: Integrates and refines code from various agents into a unified script. It ensures that the code is executable and correct, including necessary adjustments such as replacing `print` with `st.write` and adding Plotly chart display commands.

- **Guidelines**:
  - **Data Handling**: Verify column names and data types.
  - **Code Refinement**: Ensure combined code is executable and correct. Make necessary adjustments for Streamlit compatibility and Plotly visualization.
  - **Error Fixing**: Address any errors found in the code and refine it accordingly.

#### `data_viz_agent`

- **Description**: The `data_viz_agent` generates data visualizations using Plotly based on the user-defined goal. It creates plots and charts that meet the specified requirements.

- **Inputs**:
  - `goal`: The user-defined goal that describes the type of visualization needed.
  - `dataset`: Information about the data in the DataFrame, including column names.
  - `styling_index`: Instructions on how to style the Plotly plots.

- **Outputs**:
  - `code`: Python code for Plotly visualizations based on the user's request and provided data.
  - `commentary`: Comments explaining the visualization and the analysis performed, excluding the code.

- **Purpose**: Produces Plotly visualizations according to the user’s specifications. Handles large datasets by sampling if necessary and ensures that the code adheres to the styling instructions provided.

- **Guidelines**:
  - **Visualization**: Use Plotly to create visualizations. If the dataset has more than 50,000 rows, use sampling.
  - **Code Output**: Provide only the visualization code and commentary. Avoid including dataset or styling index details in the output.
  - **Plot Customization**: Add trendlines to scatter plots if requested.

#### `code_fix`

- **Description**: The `code_fix` agent addresses and corrects errors in faulty data analytics code. It generates fixed code based on the error messages and user-provided context.

- **Inputs**:
  - `faulty_code`: The code that failed to execute.
  - `previous_code_fixes`: User-provided context to assist in fixing the code.
  - `error`: The error message generated by the faulty code.

- **Outputs**:
  - `faulty_code`: Reproduces the faulty code for reference.
  - `fixed_code`: The corrected version of the code that resolves the issues.

- **Purpose**: Fixes errors in data analytics code, ensuring that the corrected code performs the intended analysis correctly. Reflects on error messages and context provided to produce a functional solution.

- **Guidelines**:
  - **Error Handling**: Analyze and address errors in the provided code.
  - **Code Correction**: Provide a fixed version of the code, making necessary adjustments to ensure proper execution.



## `auto_analyst_ind`

The `auto_analyst_ind` module is designed to handle queries directed towards specific agents by their names. This module processes requests where an agent is explicitly mentioned in the query and interacts with the corresponding agent to generate a response. It is part of the broader Auto-Analyst system and facilitates specialized, agent-specific analysis.

### Overview

The `auto_analyst_ind` class:

- Initializes various data science agents.
- Uses retrievers to fetch relevant data and styling information.
- Routes queries to specified agents and collects their outputs.
- Summarizes and stores agent outputs and relevant details.

### Initialization

#### `__init__(self, agents, retrievers)`

- **Parameters**:
  - `agents`: A list of DSPy agent signatures that will be initialized and used.
  - `retrievers`: A dictionary containing retrievers for datasets and styling indices.

- **Attributes**:
  - `self.agents`: A dictionary mapping agent names to their respective DSPy ChainOfThought objects.
  - `self.agent_inputs`: A dictionary mapping agent names to their required inputs.
  - `self.agent_desc`: A list of descriptions for each agent.
  - `self.memory_summarize_agent`: An agent responsible for summarizing memory and agent actions.
  - `self.dataset`: A retriever for fetching dataset information.
  - `self.styling_index`: A retriever for fetching styling instructions.

### Methods

#### `forward(self, query, specified_agent)`

- **Parameters**:
  - `query`: The user query that specifies what analysis is needed.
  - `specified_agent`: The name of the agent explicitly mentioned in the query.

- **Returns**:
  - A dictionary containing the output from the specified agent and a summary of the agent's action.

- **Functionality**:
  - **Retrieves Data**: Uses `self.dataset` and `self.styling_index` to fetch relevant information based on the query.
  - **Prepares Inputs**: Constructs input parameters for the specified agent from the retrieved data.
  - **Interacts with Agent**: Calls the specified agent with the prepared inputs and collects the output.
  - **Displays Output**: Shows the agent's output in the Streamlit interface and appends it to session messages.
  - **Updates Memory**: Summarizes the agent's output and updates short-term memory with this summary.

### Usage

The `auto_analyst_ind` module is utilized when a query explicitly mentions an agent by name. It routes the query to the specified agent, manages the agent's inputs and outputs, and provides detailed feedback to the user through the Streamlit interface. It also ensures that relevant data and styling information are considered during agent interactions.



## `auto_analyst`

The `auto_analyst` module is a comprehensive solution for automating data analysis tasks. It leverages multiple agents to plan, execute, and synthesize data analyses based on user queries. This module integrates planning, goal refinement, code combination, and storytelling to provide a coherent and actionable analysis output.

### Overview

The `auto_analyst` class:

- Initializes various data science agents, including planning, goal refinement, code combination, and storytelling agents.
- Uses retrievers to fetch relevant data and styling information.
- Routes queries to a planning agent to devise a plan, which is then executed by the designated agents.
- Combines the output from multiple agents into a single script and generates a summary of the entire analysis.

### Initialization

#### `__init__(self, agents, retrievers)`

- **Parameters**:
  - `agents`: A list of DSPy agent signatures that will be initialized and used.
  - `retrievers`: A dictionary containing retrievers for datasets and styling indices.

- **Attributes**:
  - `self.agents`: A dictionary mapping agent names to their respective DSPy ChainOfThought objects.
  - `self.agent_inputs`: A dictionary mapping agent names to their required inputs.
  - `self.agent_desc`: A list of descriptions for each agent.
  - `self.planner`: An agent responsible for devising an analysis plan.
  - `self.refine_goal`: An agent used to refine the query if the planner fails.
  - `self.code_combiner_agent`: An agent for combining code from different agents.
  - `self.story_teller`: An agent for creating a summary story of the analysis.
  - `self.memory_summarize_agent`: An agent for summarizing the memory and actions of other agents.
  - `self.dataset`: A retriever for fetching dataset information.
  - `self.styling_index`: A retriever for fetching styling instructions.

### Methods

#### `forward(self, query)`

- **Parameters**:
  - `query`: The user query specifying the desired analysis.

- **Returns**:
  - A dictionary containing the output from various agents and a summary of the analysis.

- **Functionality**:
  - **Retrieves Data**: Uses `self.dataset` and `self.styling_index` to fetch relevant information based on the query.
  - **Prepares Inputs**: Constructs input parameters for the agents from the retrieved data.
  - **Planner Agent**: Sends the query to the planning agent to devise a plan. Displays the plan and its description.
  - **Goal Refinement**: If the planner fails to route the query, refines the goal using the `goal_refiner_agent` and retries.
  - **Agent Execution**: Executes each agent in the plan, collects their outputs, and displays the code and commentary.
  - **Code Combination**: Combines code from all agents using the `code_combiner_agent`.
  - **Storytelling**: Creates a summary story of the entire analysis using the `story_teller` agent.
  - **Progress Tracking**: Uses a progress bar to indicate the completion status of various steps.

### Usage

The `auto_analyst` module automates the process of planning, executing, and synthesizing data analyses. It takes a user query, devises a plan using the planning agent, executes the plan with various data science agents, combines the outputs into a single script, and generates a coherent summary of the analysis. This module is ideal for scenarios where complex data analyses need to be automated and streamlined.

