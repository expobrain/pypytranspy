import ast

import astor


def replace_node_field(node, replace_field: str, new_value: object):
    new_fields = {}

    for field in node._fields:
        value = new_value if field == replace_field else getattr(node, field)
        new_fields[field] = value

    new_node = node.__class__(**new_fields)

    return new_node


class RemoveAnnotationsTransformer(astor.tree_walk.TreeWalk):

    def pre_arg(self):
        """
        Remove annotations from function's arguments
        """
        node = replace_node_field(self.cur_node, "annotation", None)

        self.replace(node)

    def post_FunctionDef(self):
        """
        Remove return type from functions
        """
        node = replace_node_field(self.cur_node, "returns", None)

        self.replace(node)

    def pre_AnnAssign(self):
        """
        Remove type from assignments
        """
        node = ast.Assign(targets=[self.cur_node.target], value=self.cur_node.value)

        self.replace(node)

    def pre_Import(self):
        """
        Remove import of `typing` package
        """
        for name in self.cur_node.names:
            if name.name == 'typing':
                self.replace(None)
                break


    def pre_ImportFrom(self):
        """
        Remove import from `typing` package
        """
        if self.cur_node.module == 'typing':
            self.replace(None)
