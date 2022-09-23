from jsonschema import validate, FormatChecker
from jsonschema.exceptions import ValidationError, SchemaError

user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 2
        }
    },
    "required": ["email", "password"],
}


def validate_user(data):
    e = _validate(data, user_schema)
    if (e['ok'] and not data["password"].endswith("gg")):
        return {'ok': False, 'message': 'Something went wrong!'}

    return e


chat_schema = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string",
        },
    },
    "required": ["text"],
}


def validate_chat(data):
    return _validate(data, chat_schema)


def _validate(data, schema):
    try:
        print("validating", data)
        validate(data, schema, format_checker=FormatChecker())
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
