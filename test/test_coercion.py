import pytest
from pydantic import BaseModel, ValidationError

from ed318_pydantic.types import CodeYesNoType, TextLongType, TextShortType


def test_text_short_type_from_str():
    text_short = TextShortType.model_validate("Hello, world!")
    assert isinstance(text_short, TextShortType)
    assert text_short.text == "Hello, world!"
    assert text_short.lang is None


def test_text_long_type_from_str():
    text_long = TextLongType.model_validate("Hello, world!")
    assert isinstance(text_long, TextLongType)
    assert text_long.text == "Hello, world!"
    assert text_long.lang is None


def test_text_type_in_model():
    class MyModel(BaseModel):
        text_short: TextShortType
        text_long: TextLongType

    my_model = MyModel.model_validate_json('{"text_short": "Hello, world!", "text_long": "Very long text"}')
    assert isinstance(my_model.text_short, TextShortType)
    assert isinstance(my_model.text_long, TextLongType)
    assert my_model.text_short.text == "Hello, world!"
    assert my_model.text_long.text == "Very long text"

    assert MyModel.model_validate({"text_short": "Hello, world!", "text_long": "Very long text"}) == MyModel(
        text_short=TextShortType(text="Hello, world!"),
        text_long=TextLongType(text="Very long text"),
    )


def test_code_yes_no_type_from_str():
    class MyModel(BaseModel):
        yes_no: CodeYesNoType

    assert MyModel.model_validate({"yes_no": "YES"}) == MyModel(yes_no="YES")
    assert MyModel.model_validate_json('{"yes_no": "NO"}') == MyModel(yes_no="NO")

    assert MyModel.model_validate({"yes_no": "yes"}) == MyModel(yes_no="YES")
    assert MyModel.model_validate_json('{"yes_no": "No"}') == MyModel(yes_no="NO")

    with pytest.raises(ValidationError):
        MyModel.model_validate({"yes_no": "maybe"})
