from tables import Table
from sql_parser import safe_parse
from validator import validate_query
from query_engine import execute_query
import json


def main():
    with open("data/users.json") as f:
        data = json.load(f)

    table = Table("Users", data, index_column="email")

    print("Welcome to MiniSQL. Type 'exit' to quit.\n")

    while True:
        sql_query = input("<mini-sql>: ").strip()
        if sql_query.lower() in ("exit", "quit"):
            break
        if not sql_query:
            continue

        parsed_query = safe_parse(sql_query)

        if "error" in parsed_query:
            print("Parser Error:", parsed_query["error"])
            continue

        errors = validate_query(parsed_query, table)
        if errors:
            print("Validation Errors:")
            for error in errors:
                print("-", error)
            continue

        results = execute_query(parsed_query, table)
        for row in results:
            print(row)

if __name__ == "__main__":
    main()