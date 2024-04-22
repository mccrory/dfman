import os
import sys
import pandas as pd
import duckdb


class dfman:
	def __init__(self, db_name="dfman.duckdb", in_memory=False):
		self.db_path = ":memory:" if in_memory else os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), db_name)
		self.conn = None
		self.connect()

	def connect(self):
		"""Establishes a new database connection."""
		self.conn = duckdb.connect(database=self.db_path, read_only=False)

	def close(self):
		"""Closes the database connection."""
		if self.conn:
			self.conn.close()
			self.conn = None

	def table_exists(self, table_name):
		try:
			query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}');"
			return self.conn.execute(query).fetchone()[0]
		finally:
			self.close()

	def load_dataframe(self, table_name):
		try:
			if self.table_exists(table_name):
				return self.conn.table(table_name).df()
			else:
				raise ValueError(f"Table '{table_name}' does not exist in the database.")
		finally:
			self.close()

	def create_and_save_dataframe(self, df, table_name):
		try:
			self.conn.register('df_table', df)
			self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df_table")
			return df
		finally:
			self.close()

	def get_or_create_dataframe(self, data_source, table_name, force_create=False):
		try:
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
		finally:
			self.close()
