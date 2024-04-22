# dfman - DataFrameManager

dfman if a simple caching solution when running and re-running computationally intensive pandas dataframes (or others with slight modifications - such as polars).
The dataframe is built and kept in both pandas and duckdb, then when re-run, it can be pulled directly from duckdb (the default is to store/cache everything on disk, this can be changed to memory if desired).


## Example usage

from dfman import dfman

def generate_data():
    # Simulate data generation process
    return pd.DataFrame({'A': range(50), 'B': range(50, 100)})


### Using an in-memory database
manager_memory = dfman(in_memory=True)
df_from_func_memory = manager_memory.get_or_create_dataframe(generate_data, 'example_table_memory', force_create=True)
print(df_from_func_memory.head())

### Using a file-based database
manager_file = dfman()
df_from_func_file = manager_file.get_or_create_dataframe(generate_data, 'example_table_file', force_create=True)
print(df_from_func_file.head())


**How it works:**

- **Database Connection**: The connection is established using DuckDB, which can operate in memory or on disk.
- **Checking Table Existence**: This is done to determine whether to load the data or recreate it.
- **Data Loading and Creation**: Depending on the user's choice, it either loads the existing data or runs the data creation function and stores the result in DuckDB.
- **User Control**: The `get_or_create_dataframe` function provides a simple interface to either fetch the existing table or recreate it based on the `force_create` flag.


