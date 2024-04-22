**dfman - DataFrameManager**

dfman if a simple caching solution when running and re-running computationally intensive pandas dataframes (or others with slight modifications - such as polars). The dataframe is built and kept in both pandas and duckdb, then when re-run, it can be pulled directly from duckdb (the default is to store/cache everything in memory, this can be changed to persist to disk if desired).



***Example:***

from dfman import dfman

def generate_data():
    # Your data generation function here
    return pd.DataFrame({'A': range(50), 'B': range(50, 100)})

manager = dfman()
df = manager.get_or_create_dataframe(generate_data, 'example_table', force_create=False)
print(df.head())



**How it works:**

- **Database Connection**: The connection is established using DuckDB, which can operate in memory or on disk.
- **Checking Table Existence**: This is done to determine whether to load the data or recreate it.
- **Data Loading and Creation**: Depending on the user's choice, it either loads the existing data or runs the data creation function and stores the result in DuckDB.
- **User Control**: The `get_or_create_dataframe` function provides a simple interface to either fetch the existing table or recreate it based on the `force_create` flag.


