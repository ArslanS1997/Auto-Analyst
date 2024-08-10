## Docs for `new_frontend.py`

The `new_frontend.py` file is responsible for the Streamlit frontend of the Auto-Analyst system, which is an AI-driven analytical tool. This file includes various functions and variables to manage data initialization, agent setup, and output handling within the Streamlit application.

### Functions and Variables

#### `stdoutIO(stdout=None)`

- **Description**: A context manager that captures standard output (stdout) generated on the console and redirects it to a `StringIO` object. This is used to display console output within the Streamlit app.
- **Arguments**:
  - `stdout` (optional): A `StringIO` object to capture output. If not provided, a new `StringIO` object is created.
- **Yields**: A `StringIO` object containing the captured output.

#### `initialize_data(button_pressed=False)`

- **Description**: Initializes and returns a DataFrame based on the file uploaded by the user or a sample CSV file. This function is cached for performance to avoid reloading the data unnecessarily.
- **Arguments**:
  - `button_pressed` (boolean): If `True`, loads a sample dataset ("Housing.csv"). If `False`, loads data from an uploaded file.
- **Returns**: A Pandas DataFrame containing the loaded data.

#### `intialize_agent()`

- **Description**: Initializes and returns the main Auto-Analyst system, configured with the specified agents and retrievers. This function is cached for performance.
- **Returns**: An instance of the `auto_analyst` system.

#### `initial_agent_ind()`

- **Description**: Initializes and returns an independent Auto-Analyst system, configured with the specified agents and retrievers. This function is cached for performance.
- **Returns**: An instance of the `auto_analyst_ind` system.

#### `initialtize_retrievers(_styling_instructions, _doc)`

- **Description**: Initializes and returns retrievers for handling styling instructions and document data. These retrievers are used by the visualization agent to manage data and styling information. This function is cached for performance.
- **Arguments**:
  - `_styling_instructions` (list of strings): List of styling instructions used for data visualization.
  - `_doc` (list of strings): List of documents used for data retrieval.
- **Returns**: A dictionary containing the initialized retrievers, including `style_index` and `dataframe_index`.

#### `run_chat()`

- **Description**: Manages the chat interaction between the user and the Auto-Analyst system. This function handles user queries, routes them to the appropriate agents, and displays responses and outputs within the Streamlit app.

- **Functionality**:
  1. **Display DataFrame**: If a DataFrame is available in the session state (`st.session_state['df']`), it displays the first five rows of the DataFrame.
  
  2. **User Input**: Prompts the user to enter a query via a chat input box. The query can either mention specific agents or be routed through the planner if no agents are specified.
  
  3. **Agent Identification**: Checks if any of the agents are mentioned in the user query and compiles a list of specified agents. 
  
  4. **Planner-based Routing**: If no specific agents are mentioned, the query is routed through the planner-based system, which generates and executes code based on the query.
  
  5. **Code Execution**: Executes the generated code using `exec()` and displays the output or errors. If an error occurs, the user can provide additional context to help fix the code.
  
  6. **Specified Agent Handling**: If specific agents are mentioned, the query is sent to those agents, and their responses are processed and displayed. Code is executed as provided by the agents, with error handling for any issues.
  
  7. **Feedback Form**: Provides a feedback form for users to rate the response and submit additional feedback. This feedback is saved to the session state.

- **User Inputs**:
  - `user_input`: The query or command entered by the user.

- **Outputs**:
  - Displays DataFrame preview, agent responses, code execution results, error messages, and feedback form.


### Variables and Additional Details

- **`agent_names`**: A list of agents used in the Auto-Analyst system. The agents include:
  - `data_viz_agent`: For data visualization tasks.
  - `sk_learn_agent`: For machine learning tasks using scikit-learn.
  - `statistical_analytics_agent`: For statistical analysis.
  - `preprocessing_agent`: For data preprocessing.


#### Streamlit Session State Initialization

The following variables are initialized in the Streamlit session state (`st.session_state`) to manage data and interactions throughout the session:

- **`messages`**: Stores the list of messages exchanged between the user and the system, including user queries and agent responses. Initialized as an empty list if not present in the session state.
  
- **`thumbs`**: Stores user feedback in the form of thumbs-up or thumbs-down ratings. Initialized as an empty string if not present in the session state.
  
- **`df`**: Stores the DataFrame containing the uploaded or sample data. Initialized as `None` if not present in the session state.
  
- **`st_memory`**: Stores short-term memory, which tracks recent interactions. Initialized as an empty list if not present in the session state.

#### Data Initialization and Retrieval

- **File Upload or Sample Data Handling**:
  - If a file is uploaded or sample data is selected, the DataFrame (`st.session_state['df']`) is initialized using the `initialize_data()` function.
  - The first five rows of the DataFrame are displayed.

- **Sample Data**:
  - If sample data is requested, a description ("Housing Dataset") is generated, and data is prepared for processing.
  
- **Uploaded Data**:
  - Users can provide a description for the uploaded dataset. Upon clicking "Start The Analysis", data is prepared with the provided description.

- **Retriever Initialization**:
  - If the document (`doc`) is not empty, retrievers are initialized using `initialtize_retrievers()`.
  - The agent systems (`agent_system_chat` and `agent_system_chat_ind`) are initialized and stored in the session state.
  - A success message is displayed to indicate successful document upload.

#### Feedback Handling

- **Feedback Saving**:
  - If user feedback (`st.session_state['thumbs']`) is provided, it is saved to a file (`output2.txt`).
  - Feedback and a separator line are appended to the file, and a confirmation message is displayed.
  
#### Chat Management

- **Running the Chat**:
  - The `run_chat()` function is called to handle user interactions, process queries, and display responses.

#### Short-term Memory Management

- **Memory Trimming**:
  - The short-term memory (`st.session_state.st_memory`) is truncated to the last 10 interactions to manage memory usage and maintain relevance.

