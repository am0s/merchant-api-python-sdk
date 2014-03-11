from functools import wraps
from apimodels.url import URL
from voluptuous import Schema, Required, Any, All, Length, Range


def validate_input(function):
    """Decorator that validates the kwargs of the function passed to it."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            endpoint = args[1]
            name = function.__name__ + '_' + endpoint + '_validator'
            globals()[name](kwargs)
            return function(*args, **kwargs)
        except KeyError:
            raise Exception("Could not find validation schema for the"
                            " function " + function.__name__)
    return wrapper

create_shortlink_validator = Schema({
    'callback_uri': str,
    'description': str,
    'serial_number': str
})

update_shortlink_validator = Schema({
    'callback_uri': str,
    'description': str
})

create_user_validator = Schema({
    Required('id'): str,
    'roles': [Any('user', 'superuser')],
    'netmask': str,
    'secret': All(str, Length(min=8, max=64)),
    'pubkey': str
})

create_payment_request_validator = Schema({
    'ledger': str,
    'display_message_uri': URL,
    'callback_uri': str,
    Required('customer'): All(str, Length(max=100)),
    Required('currency'): All(str, Length(min=3, max=3)),
    Required('amount'): str,
    'additional_amount': All(float, Range(min=0)),
    'additional_edit': bool,
    Required('allow_credit'): bool,
    Required('pos_id'): str,
    Required('pos_tid'): str,
    'text': str,
    Required('action'): Any('auth', 'sale', 'AUTH', 'SALE'),
    'expires_in': All(int, Range(min=0, max=2592000)),
})

create_point_of_sale_validator = Schema({
    Required('name'): str,
    Required('type'): str,
    Required('id'): str,
    'location': str,
})

update_payment_request_validator = Schema({
    'ledger': str,
    'display_message_uri': URL,
    'callback_uri': str,
    'currency': All(str, Length(min=3, max=3)),
    'amount': str,
    'additional_amount': All(float, Range(min=0)),
    'capture_id': str,
    'action': Any('auth', 'sale', 'AUTH', 'SALE'),
})

create_permission_request_validator = Schema({
    'ledger': str,
    Required('customer'): All(str, Length(max=100)),
    Required('pos_id'): str,
    Required('pos_tid'): str,
    'text': str,
    'callback_uri': str,
    Required('scope'): str,
    'expires_in': All(int, Range(min=0, max=2592000)),
})
