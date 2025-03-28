from lark import Lark, Transformer
from lark.exceptions import UnexpectedToken

sql_grammar = r"""
    start: select_stmt

    select_stmt: "SELECT" columns "FROM" NAME where_clause?

    columns: "*" -> all_columns
           | column ("," column)* -> column_list

    column: NAME

    where_clause: "WHERE" condition

    condition: NAME "=" value

    value: ESCAPED_STRING

    %import common.CNAME -> NAME
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
    %ignore ";" // ignore semicolons in the grammar
"""

class SQLTransformer(Transformer):
    def start(self, items):
        return items[0]
        
    def select_stmt(self, args):
        table_token = args[1]
        return {
            "ACTION": "SELECT",
            "COLUMNS": args[0],
            "TABLE": str(table_token),
            "WHERE": args[2] if len(args) > 2 else None
        }

    def all_columns(self, _):
        return "*"

    def column_list(self, cols):
        return [col for col in cols]

    def column(self, col):
        return str(col[0])

    def where_clause(self, cond):
        return cond[0]

    def condition(self, args):
        return {"column": str(args[0]), "value": str(args[1]).strip("'\"")}  # strip quotes

    def value(self, val):
        return val[0]

parser = Lark(sql_grammar, parser="lalr", transformer=SQLTransformer())

def safe_parse(query: str):
    try:
        return parser.parse(query)
    except UnexpectedToken as e:
        return {"error": f"Syntax error at token '{e.token.value}' (expected one of: {', '.join(e.expected)})"}
    except Exception as e:
        return {"error": f"Unknown parsing error: {str(e)}"}
    
