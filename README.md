

# Auto-Analyst 



![auto-analyst logo.png](https://github.com/ArslanS1997/Auto-Analyst/blob/main/auto-analyst%20logo.png)




## Description

**Auto-Analyst** is an AI-driven data analytics agentic system designed to simplify and enhance the data science process. By integrating various specialized AI agents, this tool aims to make complex data analysis tasks more accessible and efficient for data analysts and scientists. Auto-Analyst provides a streamlined approach to data preprocessing, statistical analysis, machine learning, and visualization, all within an interactive Streamlit interface.

![UI Banner](https://github.com/ArslanS1997/Auto-Analyst/blob/main/Auto-Analyst%20Banner.png)

### Key Features:

1. **Plug and Play Streamlit UI**: 
   - An intuitive and interactive web interface powered by Streamlit that makes it easy to use and visualize data without extensive setup.

2. **Agents with Data Science Speciality**:
   - **Data Visualization Agent**: Generates a wide range of Plotly charts and visualizations.
   - **Statistical Analytics Agent**: Performs comprehensive statistical analyses and generates descriptive statistics.
   - **Scikit-Learn Agent**: Integrates with Scikit-Learn to build and evaluate machine learning models.
   - **Preprocessing Agent**: Handles data cleaning, transformation, and preparation tasks.

3. **Completely Automated, LLM Agnostic**:
   - The system operates with full automation and is agnostic to large language models (LLMs), making it adaptable to various AI models and technologies.

4. **Built Using Lightweight Frameworks**:
   - Constructed with efficient frameworks like DSPy, ensuring a lightweight and responsive application.

## How to Run Locally

To run the Streamlit app locally, follow these steps:

### 1. Clone the Repository

First, clone the repository to your local machine using Git:

```bash
git clone https://github.com/ArslanS1997/Auto-Analyst.git
cd your-repository
```

### 2. Install Dependencies

Create a virtual environment and install the required Python packages. The required packages are listed in the `requirements.txt` file. Make sure you have `pip` installed, and then run:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

You need to set up the `OPENAI_API_KEY` environment variable for the app to function. You can do this by adding the following line to your `.env` file or by exporting the variable in your terminal:

#### Using `.env` file:
Create a file named `.env` in the root of your project and add:

```plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

#### Exporting in Terminal:
```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

### 4. Run the Streamlit App

Start the Streamlit app using the following command:

```bash
streamlit run new_frontend.py
```



## Files in the System

The project consists of several key files, each serving a distinct purpose:

1. **`agents.py`**:
   - **Description**: Contains the definitions for various AI agents used in the system.
   - **Key Agents**:
     - `auto_analyst_ind`: Routes queries to the appropriate agent based on user input and provides a detailed response.
     - `auto_analyst`: Integrates a planner agent for routing queries and a code combiner agent for synthesizing outputs from multiple agents.
     - `memory_summarize_agent`: Summarizes agent responses and user queries.
     - `error_memory_agent`: Creates summaries of code errors and their corrections.

2. **`memory_agents.py`**:
   - **Description**: Defines agents that help summarize memory and errors.
   - **Key Agents**:
     - `memory_summarize_agent`: Provides summaries of agent responses and user goals.
     - `error_memory_agent`: Analyzes and summarizes code errors and suggested corrections.

3. **`retrievers.py`**:
   - **Description**: Contains functions and configurations for retrieving and processing data.
   - **Key Functions**:
     - `return_vals`: Collects useful information about data columns, such as statistics and top categories.
     - `correct_num`: Cleans numeric columns by removing commas and converting to float.
     - `make_data`: Pre-processes data and generates a description of the dataset.
   - **Styling Instructions**: Provides instructions for styling Plotly charts for different types of visualizations, including line charts, bar charts, histograms, pie charts, and heat maps.

4. **`new_frontend.py`**:
   - **Description**: The main Streamlit script that runs the application and integrates all the agents and functionalities provided in the other files. 


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

