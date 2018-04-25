import os
import ast

import astor


class FStringToFormatTransformer(astor.tree_walk.TreeWalk):

    def pre_JoinedStr(self):
        # Collect string and args for format()
        str_value = ''
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
            func=ast.Attribute(value=ast.Str(s=str_value), attr='format'),
            args=str_args,
            keywords=[]
        )

        self.replace(str_format)


if __name__ == "__main__":
    cwd = os.path.abspath(os.path.dirname(__file__))
    in_ = os.path.join(cwd, "f-strings.in.py")
    out = os.path.join(cwd, "f-strings.out.py")

    source_ast = astor.parse_file(in_)
    print(astor.dump_tree(source_ast))

    FStringToFormatTransformer(source_ast)

    print('-' * 10)
    print(astor.dump_tree(source_ast))

    source = astor.to_source(source_ast)

    with open(out, 'w') as f:
        f.write(source)
