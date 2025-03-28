def validate_query(parsed_query, table):
    errors = []

    if parsed_query["TABLE"].lower() != table.name.lower():
        errors.append(f"Table '{parsed_query['TABLE']}' does not exist. Available: {table.name}")

    if parsed_query["COLUMNS"] != "*":
        for col in parsed_query["COLUMNS"]:
            if col not in table.columns:
                errors.append(f"Column '{col}' not found in table. Available columns: {table.columns}")
                
    if parsed_query["WHERE"]:
        where_col = parsed_query["WHERE"]["column"]
        if where_col not in table.columns:
            errors.append(f"WHERE column '{where_col}' not found in table.")

    return errors