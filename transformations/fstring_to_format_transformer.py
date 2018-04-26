import ast

import astor


class FStringToFormatTransformer(astor.tree_walk.TreeWalk):

    def pre_JoinedStr(self):
        # Collect string and args for format()
        str_value = ""
        str_args = []

        for value in self.cur_node.values:
            if isinstance(value, ast.Str):
                str_value += value.s
            elif isinstance(value, ast.FormattedValue):
                str_value += "{}"
                str_args.append(value.value)
            else:
                raise NotImplementedError(value)

        # Build Str.format() node
        str_format = ast.Call(
            func=ast.Attribute(value=ast.Str(s=str_value), attr="format"),
            args=str_args,
            keywords=[],
        )

        self.replace(str_format)
