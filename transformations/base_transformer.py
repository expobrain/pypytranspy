import astor


class BaseTransformer(astor.tree_walk.TreeWalk):

    # Minimum version where the transformed feature is supporter by the interpreter
    minimum_version = None
