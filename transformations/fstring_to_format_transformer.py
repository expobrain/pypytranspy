import ast

from .base_transformer import BaseTransformer


class FStringToFormatTransformer(BaseTransformer):

    minimum_version = [3, 6]

    def pre_JoinedStr(self):
        # Collect string and args for format()
        str_value = ""
        str_args = []

        for value in self.cur_node.values:
            if isinstance(value, ast.Str):
                str_value += value.s
            elif isinstance(value, ast.FormattedValue):
                if value.format_spec is None:
                    str_value += "{}"
                else:
                    str_value += "{:" + "".join(v.s for v in value.format_spec.values) + "}"

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
