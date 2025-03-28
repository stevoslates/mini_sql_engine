from tables import Table
import json


if __name__ == "__main__":
    with open("data/users.json") as f:
        data = json.load(f)

    # Create table with B-tree index on 'email'
    table = Table("Users", data, index_column="email")

    row_id = table.index.search("eve@example.com")
    print(table.rows[row_id])