from marshmallow import fields


class Categorical(fields.Field):
    def __init__(
        self,
        *,
        categories: list = [],
        missing: str = "missing",
        default: int = -1,
        **kwargs
    ):
        self._categories: list = categories
        self._dict_serialize: dict = {cat: idx for idx, cat in enumerate(categories)}
        self._dict_deserialize: dict = {idx: cat for idx, cat in enumerate(categories)}

        self.missing = missing
        self.default = default

        self.metadata = {"categories": categories}

        super().__init__(**kwargs)

    def _serialize(self, value, attr, obj, **kwargs) -> int:
        return self._dict_serialize.get(value, self.default)

    def _deserialize(self, value, attr, data, **kwargs) -> str:
        return self._dict_deserialize.get(value, self.missing)


class Multinomial(fields.Field):
    def __init__(
        self,
        *,
        categories: list = [],
        missing: str = "missing",
        default: int = -1,
        **kwargs
    ):
        self._categories: list = categories
        self._dict_serialize: dict = {cat: idx for idx, cat in enumerate(categories)}
        self._dict_deserialize: dict = {idx: cat for idx, cat in enumerate(categories)}

        self.missing = missing
        self.default = default

        self.metadata = {"categories": categories}

        super().__init__(**kwargs)

    def _serialize(self, value, attr, obj, **kwargs) -> set[int]:
        return {self._dict_serialize.get(v, self.default) for v in value}

    def _deserialize(self, value, attr, data, **kwargs) -> set[str]:
        return {self._dict_deserialize.get(v, self.missing) for v in value}
