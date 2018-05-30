from typing import Iterator, Tuple

from .string_format import StringFormat


def replace_node_field(node, replace_field: str, new_value: object):
    new_fields = {}

    for field in node._fields:
        value = new_value if field == replace_field else getattr(node, field)
        new_fields[field] = value

    new_node = node.__class__(**new_fields)

    return new_node


def parse_string_format_iter(s: str) -> Tuple[int, int, Iterator[StringFormat]]:
    """
    Parse the string to search for format string syntaxes and split them by
    field name, conversion and format spec
    """
    i = len(s) - 1

    while i > -1:
        if s[i] == "{" and (i > 0 or s[i - 1] != "\\"):
            try:
                end = s.index("}", i)
            except ValueError:
                raise ValueError("Format string is not terminated with `}`")

            format_def_str = s[i + 1 : end]

            has_conversion = "!" in format_def_str
            has_format_spec = ":" in format_def_str

            field_name = format_def_str.split("!" if has_conversion else ":")[0].strip()
            field_name = None if len(field_name) == 0 else field_name
            conversion = format_def_str.split("!")[1].split(":")[0] if has_conversion else None
            format_spec = format_def_str.split(":")[1] if has_format_spec else None

            string_format = StringFormat(field_name, conversion, format_spec)

            yield (i, end, string_format)

        i -= 1
