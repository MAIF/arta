from pydantic.version import VERSION
import pydantic as __pydantic

if VERSION.startswith('1.'):

    ValidationError = __pydantic.ValidationError
    _oldBaseModel = __pydantic.BaseModel
    class BaseModel(_oldBaseModel):
        model_validate = _oldBaseModel.parse_obj

    class RootModel(_oldBaseModel):
        pass
    field_validator = __pydantic.validator
    model_validator = __pydantic.root_validator

else:

    ValidationError = __pydantic.ValidationError
    BaseModel = __pydantic.BaseModel
    RootModel = __pydantic.RootModel
    StringConstraints = __pydantic.StringConstraints
    field_validator = __pydantic.field_validator
    model_validator = __pydantic.model_validator

