from lark import Lark, Transformer

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
"""

class SQLTransformer(Transformer):
    def select_stmt(self, args):
        return {
            "ACTION": "SELECT",
            "COLUMNS": args[0],
            "TABLE": args[1],
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
        return {"column": str(args[0]), "value": args[1][1:-1]}  # strip quotes

    def value(self, val):
        return val[0]

parser = Lark(sql_grammar, parser="lalr", transformer=SQLTransformer())
