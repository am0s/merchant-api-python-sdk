# -*- coding: utf-8 -*-
from functools import wraps

from voluptuous import Schema, Required, Any, All, Length, Range

from .six import string_types


validate_strings = Any(*string_types)


def validate_input(function):
    """Decorator that validates the kwargs of the function passed to it."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            name = function.__name__ + '_validator'  # find validator name
            globals()[name](kwargs)  # call validation function
            return function(*args, **kwargs)
        except KeyError:
            raise Exception("Could not find validation schema for the"
                            " function " + function.__name__)
    return wrapper

create_user_validator = Schema({
    Required('user_id'): validate_strings,
    'roles': [Any('user', 'superuser')],
    'netmask': validate_strings,
    'secret': All(validate_strings, Length(min=8, max=64)),
    'pubkey': validate_strings
})

update_user_validator = Schema({
    Required('user_id'): validate_strings,
    'roles': [Any('user', 'superuser')],
    'netmask': validate_strings,
    'secret': All(validate_strings, Length(min=8, max=64)),
    'pubkey': validate_strings
})

create_pos_validator = Schema({
    Required('name'): validate_strings,
    Required('pos_type'): validate_strings,
    Required('pos_id'): validate_strings,
    'location': {'latitude': float,
                 'longitude': float,
                 'accuracy': float}
})

create_shortlink_validator = Schema({
    'callback_uri': validate_strings,
    'description': validate_strings,
    'serial_number': validate_strings
})

update_pos_validator = Schema({
    Required('pos_id'): validate_strings,
    Required('name'): validate_strings,
    Required('pos_type'): validate_strings,
    'location': {'latitude': float,
                 'longitude': float,
                 'accuracy': float}
})

create_payment_request_validator = Schema({
    'ledger': validate_strings,
    'display_message_uri': validate_strings,
    'callback_uri': validate_strings,
    Required('customer'): All(validate_strings, Length(max=100)),
    Required('currency'): All(validate_strings, Length(min=3, max=3)),
    Required('amount'): validate_strings,
    'additional_amount': validate_strings,
    'required_scope': validate_strings,
    'required_scope_text': validate_strings,
    'additional_edit': bool,
    Required('allow_credit'): bool,
    Required('pos_id'): validate_strings,
    Required('pos_tid'): validate_strings,
    'text': validate_strings,
    Required('action'): Any('auth', 'sale', 'AUTH', 'SALE'),
    Required('expires_in'): All(int, Range(min=0, max=2592000)),
    'links': [{'uri': validate_strings, 'caption': validate_strings, 'show_on': [Any('pending', 'fail', 'ok')]}],
    'line_items': Any([{
        Required('product_id'): validate_strings,
        'vat': validate_strings,
        'metadata': Any([{'key': validate_strings, 'value': validate_strings}], None),
        'description': validate_strings,
        'vat_rate': validate_strings,
        Required('total'): validate_strings,
        'tags': [{
            Required('tag_id'): validate_strings,
            Required('label'): validate_strings,
        }],
        Required('item_cost'): validate_strings,
        Required('quantity'): validate_strings,
    }], None)
})

update_payment_request_validator = Schema({
    'tid': validate_strings,
    'ledger': validate_strings,
    'display_message_uri': validate_strings,
    'callback_uri': validate_strings,
    'currency': All(validate_strings, Length(min=3, max=3)),
    'amount': validate_strings,
    'additional_amount': validate_strings,
    'required_scope': validate_strings,
    'required_scope_text': validate_strings,
    'capture_id': validate_strings,
    'refund_id': validate_strings,
    'text': validate_strings,
    'action': Any('reauth', 'capture', 'abort', 'release', 'refund',
                  'REAUTH', 'CAPTURE', 'ABORT', 'RELEASE', 'REFUND'),
    'line_items': Any([{
        Required('product_id'): validate_strings,
        'vat': validate_strings,
        'metadata': Any([{'key': validate_strings, 'value': validate_strings}], None),
        'description': validate_strings,
        'vat_rate': validate_strings,
        Required('total'): validate_strings,
        'tags': [{
            Required('tag_id'): validate_strings,
            Required('label'): validate_strings,
        }],
        Required('item_cost'): validate_strings,
        Required('quantity'): validate_strings,
    }], None)
})

update_ticket_validator = Schema({
    Required('tid'): validate_strings,
    'tickets': list,
})

update_shortlink_validator = Schema({
    Required('shortlink_id'): validate_strings,
    'callback_uri': validate_strings,
    'description': validate_strings
})

create_ledger_validator = Schema({
    Required('currency'): validate_strings,
    'description': validate_strings
})

update_ledger_validator = Schema({
    Required('ledger_id'): validate_strings,
    'description': validate_strings
})

close_report_validator = Schema({
    Required('ledger_id'): validate_strings,
    Required('report_id'): validate_strings,
    'callback_uri': validate_strings,
})

create_permission_request_validator = Schema({
    'ledger': validate_strings,
    Required('customer'): All(validate_strings, Length(max=100)),
    Required('pos_id'): validate_strings,
    Required('pos_tid'): validate_strings,
    'text': validate_strings,
    'callback_uri': validate_strings,
    Required('scope'): validate_strings,
    'expires_in': All(int, Range(min=0, max=2592000)),
})
