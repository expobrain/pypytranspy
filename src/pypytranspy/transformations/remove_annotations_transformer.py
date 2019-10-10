import ast

from pypytranspy.transformations.base_transformer import BaseTransformer
from pypytranspy.transformations.utils import replace_node_field


class RemoveAnnotationsTransformer(BaseTransformer):
    minimum_version = [3]

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
            if name.name == "typing":
                self.replace(None)
                break

    def pre_ImportFrom(self):
        """
        Remove import from `typing` package
        """
        if self.cur_node.module == "typing":
            self.replace(None)
