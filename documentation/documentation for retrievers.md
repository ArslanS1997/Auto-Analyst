
## `retrievers`

The `retrievers` file provides functions and styling instructions used for data preprocessing and visualization in your data analysis pipeline.

### Functions

#### `return_vals(df, c)`

- **Purpose**: Extracts useful statistical information from a DataFrame column.

- **Parameters**:
  - `df` (`pandas.DataFrame`): The DataFrame containing the data.
  - `c` (`str`): The column name for which statistics are to be computed.

- **Returns**: A dictionary with statistical details:
  - For numeric columns:
    - `max_value`: Maximum value in the column.
    - `min_value`: Minimum value in the column.
    - `mean_value`: Mean value of the column.
  - For datetime columns:
    - Returns maximum and minimum dates as strings, and the mean date as a string.
  - For categorical columns:
    - `top_10_values`: The top 10 most frequent values.
    - `total_category_count`: The total number of unique categories.

- **Usage Example**:
  ```python
  stats = return_vals(df, 'column_name')
  ```

#### `correct_num(df, c)`

- **Purpose**: Cleans and converts numeric columns in the DataFrame by removing commas and converting to float.

- **Parameters**:
  - `df` (`pandas.DataFrame`): The DataFrame containing the data.
  - `c` (`str`): The column name to be cleaned and converted.

- **Returns**: The cleaned and converted column.

- **Usage Example**:
  ```python
  df['cleaned_column'] = correct_num(df, 'column_with_commas')
  ```

#### `make_data(df, desc)`

- **Purpose**: Performs preprocessing on the DataFrame, including cleaning numeric columns and summarizing column details.

- **Parameters**:
  - `df` (`pandas.DataFrame`): The DataFrame to preprocess.
  - `desc` (`str`): A description of the data.

- **Returns**: A dictionary containing:
  - `df_name`: Name of the DataFrame.
  - `Description`: Description of the data.
  - `dataframe_head_view`: A Markdown-formatted preview of the first 5 rows of the DataFrame.
  - `all_column_names`: A list of all column names in the DataFrame.
  - For each column:
    - `column_name`: The column name.
    - `type`: The type of data in the column.
    - `column_information`: Statistical information about the column, if applicable.

- **Usage Example**:
  ```python
  data_summary = make_data(df, 'Data description')
  ```

### Styling Instructions

The following styling instructions are used for generating Plotly charts. They ensure consistency and clarity in visualizations.

1. **Line Chart**:
   ```plaintext
   Dont ignore any of these instructions.
   For a line chart always use plotly_white template, reduce x axes & y axes line to 0.2 & x & y grid width to 1. 
   Always give a title and make bold using html tag axis label and try to use multiple colors if more than one line
   Annotate the min and max of the line
   Display numbers in thousand(K) or Million(M) if larger than 1000/100000 
   Show percentages in 2 decimal points with '%' sign
   Default size of chart should be height =1200 and width =1000
   ```

2. **Bar Chart**:
   ```plaintext
   Dont ignore any of these instructions.
   For a bar chart always use plotly_white template, reduce x axes & y axes line to 0.2 & x & y grid width to 1. 
   Always give a title and make bold using html tag axis label 
   Always display numbers in thousand(K) or Million(M) if larger than 1000/100000. 
   Annotate the values of the bar chart
   If variable is a percentage show in 2 decimal points with '%' sign.
   Default size of chart should be height =1200 and width =1000
   ```

3. **Histogram Chart**:
   ```plaintext
   For a histogram chart choose a bin_size of 50
   Do not ignore any of these instructions
   always use plotly_white template, reduce x & y axes line to 0.2 & x & y grid width to 1. 
   Always give a title and make bold using html tag axis label 
   Always display numbers in thousand(K) or Million(M) if larger than 1000/100000. Add annotations x values
   If variable is a percentage show in 2 decimal points with '%'
   Default size of chart should be height =1200 and width =1000
   ```

4. **Pie Chart**:
   ```plaintext
   For a pie chart only show top 10 categories, bundle rest as others
   Do not ignore any of these instructions
   always use plotly_white template, reduce x & y axes line to 0.2 & x & y grid width to 1. 
   Always give a title and make bold using html tag axis label 
   Always display numbers in thousand(K) or Million(M) if larger than 1000/100000. Add annotations x values
   If variable is a percentage show in 2 decimal points with '%'
   Default size of chart should be height =1200 and width =1000
   ```

5. **General Instructions**:
   ```plaintext
   Do not ignore any of these instructions
   always use plotly_white template, reduce x & y axes line to 0.2 & x & y grid width to 1. 
   Always give a title and make bold using html tag axis label 
   Always display numbers in thousand(K) or Million(M) if larger than 1000/100000. Add annotations x values
   Don't add K/M if number already in , or value is not a number
   If variable is a percentage show in 2 decimal points with '%'
   Default size of chart should be height =1200 and width =1000
   ```

6. **Heat Map**:
   ```plaintext
   For a heat map
   Use the 'plotly_white' template for a clean, white background. 
   Set a chart title 
   Style the X-axis with a black line color, 0.2 line width, 1 grid width, format 1000/1000000 as K/M
   Do not format non-numerical numbers 
   Style the Y-axis with a black line color, 0.2 line width, 1 grid width format 1000/1000000 as K/M
   Do not format non-numerical numbers 
   Set the figure dimensions to a height of 1200 pixels and a width of 1000 pixels.
   ```

7. **Histogram for Returns/Distribution**:
   ```plaintext
   For a Histogram, used for returns/distribution plotting
   Use the 'plotly_white' template for a clean, white background. 
   Set a chart title 
   Style the X-axis  1 grid width, format 1000/1000000 as K/M
   Do not format non-numerical numbers 
   Style the Y-axis, 1 grid width format 1000/1000000 as K/M
   Do not format non-numerical numbers 
   Use an opacity of 0.75
   Set the figure dimensions to a height of 1200 pixels and a width of 1000 pixels.
   ```

### Usage

- **`return_vals(df, c)`**: Use this function to obtain statistical information about a DataFrame column, including top values and summary statistics.

- **`correct_num(df, c)`**: Use this function to clean numeric columns by removing commas and converting them to float.

- **`make_data(df, desc)`**: Use this function to preprocess a DataFrame and summarize column details.

- **Styling Instructions**: Apply these instructions when generating various types of Plotly charts to ensure consistency and clarity in visualizations.

