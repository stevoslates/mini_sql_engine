"""
Simple Query Engine to Handle SELECT Queries, we use same logic as in most SQL engines, we filter the rows based on the WHERE clause and then select the columns specified in the query.
"""

def execute_query(parsed_query, table):
    if parsed_query["WHERE"]:
        column = parsed_query["WHERE"]["column"]
        value = parsed_query["WHERE"]["value"]

        row_ids = table.select(column, value)
        row_ids = [row_ids] if isinstance(row_ids, int) else row_ids or []
        filtered_rows = [table.rows[i] for i in row_ids]
    else:
        filtered_rows = table.rows

    if parsed_query["COLUMNS"] == "*":
        return filtered_rows

    selected_cols = parsed_query["COLUMNS"]
    return [{col: row[col] for col in selected_cols} for row in filtered_rows]