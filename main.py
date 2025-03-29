from tables import Table
from sql_parser import safe_parse
from validator import validate_query
import json


if __name__ == "__main__":
    with open("data/users.json") as f:
        data = json.load(f)

    # Create table with B-tree index on 'email'
    table = Table("Users", data, index_column="email")

    sql_query = input("<mini-sql>: ")
    parsed_query = safe_parse(sql_query)
    errors = validate_query(parsed_query, table)

    if errors:
        print("Errors:")
        for error in errors:
            print(error)
        # Skip executing the query
        exit()

    #Execute the query
    # Should do the WHERE clause first, then the SELECT clause
    if parsed_query["WHERE"]:
        column = parsed_query["WHERE"]["column"]
        value = parsed_query["WHERE"]["value"]

        # Filter rows using index or linear scan
        row_ids = [table.select(column, value)]
        filtered_rows = [table.rows[i] for i in row_ids]
    else:
        # No WHERE clause = return all rows
        filtered_rows = table.rows


    if parsed_query["COLUMNS"] == "*":
        results = filtered_rows
    else:
        selected_cols = parsed_query["COLUMNS"]
        results = [{col: row[col] for col in selected_cols} for row in filtered_rows]

    # Print or return results
    for row in results:
        print(row)