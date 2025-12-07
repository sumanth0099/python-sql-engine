# storage.py
import csv
import os

class TableNotFound(Exception):
    pass

class Storage:
    def __init__(self):
        self.tables = {}

    def load_csv(self, path: str, table_name: str = None):
        if not os.path.exists(path):
            raise FileNotFoundError(f"CSV file not found: {path}")
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = [dict(r) for r in reader]
            cols = reader.fieldnames or []
        if table_name is None:
            base = os.path.basename(path)
            table_name = os.path.splitext(base)[0]
        self.tables[table_name] = {'columns': cols, 'rows': rows}
        return table_name, len(rows), len(cols)

    def get_table(self, name: str):
        if name not in self.tables:
            raise TableNotFound(f"Table '{name}' not found. Use .load <path> [name].")
        return self.tables[name]

    def list_tables(self):
        return list(self.tables.keys())

    def schema(self, name: str):
        t = self.get_table(name)
        return t['columns']
