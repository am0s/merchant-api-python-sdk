# -*- coding: utf-8 -*-
from functools import wraps

from voluptuous import Schema, Required, Any, All, Length, Range

from .six import string_types


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
    Required('user_id'): string_types,
    'roles': [Any('user', 'superuser')],
    'netmask': string_types,
    'secret': All(string_types, Length(min=8, max=64)),
    'pubkey': string_types
})

update_user_validator = Schema({
    Required('user_id'): string_types,
    'roles': [Any('user', 'superuser')],
    'netmask': string_types,
    'secret': All(string_types, Length(min=8, max=64)),
    'pubkey': string_types
})

create_pos_validator = Schema({
    Required('name'): string_types,
    Required('pos_type'): string_types,
    Required('pos_id'): string_types,
    'location': {'latitude': float,
                 'longitude': float,
                 'accuracy': float}
})

create_shortlink_validator = Schema({
    'callback_uri': string_types,
    'description': string_types,
    'serial_number': string_types
})

update_pos_validator = Schema({
    Required('pos_id'): string_types,
    Required('name'): string_types,
    Required('pos_type'): string_types,
    'location': {'latitude': float,
                 'longitude': float,
                 'accuracy': float}
})

create_payment_request_validator = Schema({
    'ledger': string_types,
    'display_message_uri': string_types,
    'callback_uri': string_types,
    Required('customer'): All(string_types, Length(max=100)),
    Required('currency'): All(string_types, Length(min=3, max=3)),
    Required('amount'): string_types,
    'additional_amount': string_types,
    'required_scope': string_types,
    'required_scope_text': string_types,
    'additional_edit': bool,
    Required('allow_credit'): bool,
    Required('pos_id'): string_types,
    Required('pos_tid'): string_types,
    'text': string_types,
    Required('action'): Any('auth', 'sale', 'AUTH', 'SALE'),
    Required('expires_in'): All(int, Range(min=0, max=2592000)),
    'links': [{'uri': string_types, 'caption': string_types, 'show_on': [Any('pending', 'fail', 'ok')]}],
    'line_items': Any([{
        Required('product_id'): string_types,
        'vat': string_types,
        'metadata': Any([{'key': string_types, 'value': string_types}], None),
        'description': string_types,
        'vat_rate': string_types,
        Required('total'): string_types,
        'tags': [{
            Required('tag_id'): string_types,
            Required('label'): string_types,
        }],
        Required('item_cost'): string_types,
        Required('quantity'): string_types,
    }], None)
})

update_payment_request_validator = Schema({
    'tid': string_types,
    'ledger': string_types,
    'display_message_uri': string_types,
    'callback_uri': string_types,
    'currency': All(string_types, Length(min=3, max=3)),
    'amount': string_types,
    'additional_amount': string_types,
    'required_scope': string_types,
    'required_scope_text': string_types,
    'capture_id': string_types,
    'refund_id': string_types,
    'text': string_types,
    'action': Any('reauth', 'capture', 'abort', 'release', 'refund',
                  'REAUTH', 'CAPTURE', 'ABORT', 'RELEASE', 'REFUND'),
    'line_items': Any([{
        Required('product_id'): string_types,
        'vat': string_types,
        'metadata': Any([{'key': string_types, 'value': string_types}], None),
        'description': string_types,
        'vat_rate': string_types,
        Required('total'): string_types,
        'tags': [{
            Required('tag_id'): string_types,
            Required('label'): string_types,
        }],
        Required('item_cost'): string_types,
        Required('quantity'): string_types,
    }], None)
})

update_ticket_validator = Schema({
    Required('tid'): string_types,
    'tickets': list,
})

update_shortlink_validator = Schema({
    Required('shortlink_id'): string_types,
    'callback_uri': string_types,
    'description': string_types
})

create_ledger_validator = Schema({
    Required('currency'): string_types,
    'description': string_types
})

update_ledger_validator = Schema({
    Required('ledger_id'): string_types,
    'description': string_types
})

close_report_validator = Schema({
    Required('ledger_id'): string_types,
    Required('report_id'): string_types,
    'callback_uri': string_types,
})

create_permission_request_validator = Schema({
    'ledger': string_types,
    Required('customer'): All(string_types, Length(max=100)),
    Required('pos_id'): string_types,
    Required('pos_tid'): string_types,
    'text': string_types,
    'callback_uri': string_types,
    Required('scope'): string_types,
    'expires_in': All(int, Range(min=0, max=2592000)),
})
