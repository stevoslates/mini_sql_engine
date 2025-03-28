"""
Controls the creation of tables, the indexes and handles the data.
"""
from btree import BTree

class Table:
    def __init__(self, name, rows, index_column=None):
        self.name = name
        self.rows = rows
        self.columns = list(rows[0].keys()) if rows else []
        self.index_column = index_column
        self.index = BTree()

        if self.index_column:
            for i, row in enumerate(rows):
                key = row[self.index_column]
                self.index.insert(key, i)  # store row index as value

    def select():
        pass

    def select_where():
        pass

