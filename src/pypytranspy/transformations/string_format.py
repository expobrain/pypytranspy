from typing import NamedTuple


__StringFormat = NamedTuple("StringFormat", field_name=str, conversion=str, format_spec=str)
__StringFormat.__new__.__defaults__ = (None, None, None)


class StringFormat(__StringFormat):
    def transform(self):
        return StringFormat(
            self.field_name,
            self.conversion,
            format_spec=(self.format_spec.replace("_", "") if self.format_spec else None),
        )

    def __str__(self):
        return (
            "{"
            + (self.field_name or "")
            + (f"!{self.conversion}" if self.conversion else "")
            + (f":{self.format_spec}" if self.format_spec else "")
            + "}"
        )
