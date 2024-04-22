import os
import sys
import pandas as pd
import duckdb


class dfman:
	def __init__(self, db_name="dfman.duckdb", in_memory=False):
		# Determine the directory of the calling script
		caller_path = os.path.dirname(os.path.abspath(sys.argv[0]))
		db_path = os.path.join(caller_path, db_name)

		if in_memory:
			self.conn = duckdb.connect(database=":memory:", read_only=False)
		else:
			self.conn = duckdb.connect(database=db_path, read_only=False)

	def table_exists(self, table_name):
		"""Check if the table exists in the DuckDB database."""
		query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}');"
		return self.conn.execute(query).fetchone()[0]

	def load_dataframe(self, table_name):
		"""Load the DataFrame from DuckDB."""
		if self.table_exists(table_name):
			return self.conn.table(table_name).df()
		else:
			raise ValueError(f"Table '{table_name}' does not exist in the database.")

	def create_and_save_dataframe(self, df, table_name):
		"""Save the DataFrame to DuckDB."""
		self.conn.register('df_table', df)
		self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df_table")
		return df

	def get_or_create_dataframe(self, data_source, table_name, force_create=False):
		"""Get or create DataFrame from a callable data source or existing DataFrame."""
		if not force_create and self.table_exists(table_name):
			print(f"Loading '{table_name}' from DuckDB.")
			return self.load_dataframe(table_name)
		else:
			if callable(data_source):
				print(f"Data source is a function, creating new DataFrame for '{table_name}'.")
				df = data_source()  # Call the function to generate DataFrame
			elif isinstance(data_source, pd.DataFrame):
				print(f"Data source is a DataFrame, saving it as '{table_name}'.")
				df = data_source
			else:
				raise TypeError("Data source must be a callable that returns a DataFrame or a DataFrame instance.")

			return self.create_and_save_dataframe(df, table_name)