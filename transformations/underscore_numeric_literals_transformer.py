import ast

from .base_transformer import BaseTransformer
from .utils import replace_node_field, parse_string_format_iter


class UnderscoreNumericLiteralsTransformer(BaseTransformer):
    """
    Note: this transformation must be applied after FStringToFormatTransformer
    """

    minimum_version = [3, 6]

    def pre_Call(self):
        """
        Converts call to formatting with underscores `{:_}` into call to format
        pre-formatted values with `pypytranspy.runtime.underscore_literal_format()`
        """
        attribute = self.cur_node.func

        if not isinstance(attribute.value, ast.Str):
            return

        string_literal = attribute.value.s
        string_format_iter = parse_string_format_iter(string_literal)
        new_args = list(self.cur_node.args)

        for i, item in enumerate(string_format_iter):
            start, end, string_format = item

            if string_format.format_spec and "_" in string_format.format_spec:
                # Replace string format
                string_literal = string_literal[:start] + "{}" + string_literal[end + 1 :]

                # Replace argument with call
                current_arg = self.cur_node.args[i]

                transformed_string_format = string_format.transform()
                format_spec = transformed_string_format.format_spec

                if transformed_string_format.conversion == "r":
                    conversion = "repr"
                elif transformed_string_format.conversion == "a":
                    conversion = "ascii"
                else:
                    conversion = "str"

                new_arg = ast.Call(
                    func=ast.Attribute(
                        value=ast.Attribute(value=ast.Name(id="pypytranspy"), attr="runtime"),
                        attr="underscore_literal_format",
                    ),
                    args=[current_arg, ast.Name(id=conversion), ast.Str(s=format_spec)],
                    keywords=[],
                )

                new_args[i] = new_arg

        new_attribute = replace_node_field(self.cur_node.func, "value", ast.Str(s=string_literal))

        new_call = self.cur_node
        new_call = replace_node_field(new_call, "func", new_attribute)
        new_call = replace_node_field(new_call, "args", new_args)

        self.replace(new_call)
