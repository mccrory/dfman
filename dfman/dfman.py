import pandas as pd
import duckdb


class dfman:
	def __init__(self, db_path=":memory:"):
		self.conn = duckdb.connect(database=db_path, read_only=False)

	def table_exists(self, table_name):
		query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}');"
		return self.conn.execute(query).fetchone()[0]

	def load_dataframe(self, table_name):
		if self.table_exists(table_name):
			return self.conn.table(table_name).df()
		else:
			raise ValueError(f"Table '{table_name}' does not exist in the database.")

	def create_and_save_dataframe(self, data_function, table_name):
		df = data_function()
		self.conn.register('df_table', df)
		self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df_table")
		return df

	def get_or_create_dataframe(self, data_function, table_name, force_create=False):
		if not force_create and self.table_exists(table_name):
			print(f"Loading '{table_name}' from DuckDB.")
			return self.load_dataframe(table_name)
		else:
			print(f"Creating new DataFrame and saving as '{table_name}'.")
			return self.create_and_save_dataframe(data_function, table_name)
