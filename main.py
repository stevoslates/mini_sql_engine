from tables import Table
from sql_parser import parser
import json


if __name__ == "__main__":
    with open("data/users.json") as f:
        data = json.load(f)

    # Create table with B-tree index on 'email'
    table = Table("Users", data, index_column="email")

    sql_query = input("<mini-sql>: ")
    parsed_query = parser.parse(sql_query)
    print(parsed_query)
    