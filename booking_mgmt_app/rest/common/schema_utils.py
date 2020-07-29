#!/usr/bin/env python

"""
Schema Utils to reduce code duplication
"""

import re
from marshmallow import ValidationError
from validate_email import validate_email
from flask_restplus import abort
from rest.common.constants import BAD_REQUEST, META, IS_DELETED, ENTITY_TYPE, FIELDS
from rest.utils.db_service import Base


def validate_filters(obj, filters):
    errors = []
    for key in filters:
        if not key in obj.__table__.columns:
            errors.append({key: ['Invalid Filter']})
    return errors


def email_format_validation(email, user_id=None):
    if not email:
        return
    if not validate_email(email):
        raise ValidationError('Email is not valid', ['email'])
        # if email.split('@')[1] in free_email_domains:
        #     raise ValidationError('Please signup with corporate email', ['email'])


def password_format_validation(password):
    r = r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,16})'
    if not re.match(r, password):
        raise ValidationError('Password length should be between 8 and 16 amd must contains one digit,\
 one lowercase and one uppercase character.', ['passsword'])


def phone_number_validation(phone_number):
    # Cleanup -, space, (, )
    number = re.sub(r'[ \-\(\)]', '', phone_number)
    if not re.match(r'^\d{10}$', number):
        raise ValidationError('Invalid phone number.', ['phone_number'])


def zipcode_format_validation(zip_code):
    r = r'(?:\d*[\-,\s])?\d+'
    if not re.match(r, zip_code):
        raise ValidationError('Invalid zip code.i.e 12345, 12345-6789', ['zip_code'])

def must_not_be_none(data, field=None):
    if data is None:
        raise abort(BAD_REQUEST, message=f"can't be blank {field}", status=BAD_REQUEST)


def must_not_be_blank(data, field=None):
    if not data or len(data.strip()) == 0:
        raise abort(BAD_REQUEST, message=f"can't be blank {field}", status=BAD_REQUEST)


def must_be_positive_int(data, field=None):
    if data < 1:
        raise abort(BAD_REQUEST, message=f"Must be a positive integer {field}", status=BAD_REQUEST)


def must_be_true(terms):
    if not terms:
        raise abort(BAD_REQUEST, message=f'You must agree with the terms and conditions {terms}', status=400)


def must_not_be_duplicate_value_for_field(collection, entity_type, field, value):
    if value.strip() != "":
        _count, _asset = Base().get(collection,
                                           {f"{META}.{IS_DELETED}": False,
                                            f"{FIELDS}.{field}": value,
                                            ENTITY_TYPE: entity_type})
        if _count >= 1 and _asset:
            abort(BAD_REQUEST, message=f"Entity already exists with {field} {value}",
                  status=BAD_REQUEST)
