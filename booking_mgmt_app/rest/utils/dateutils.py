#!/usr/bin/env python
import datetime
import time


def get_current_time():
    return datetime.datetime.utcnow()


def get_current_time_ms():
    return round(datetime.datetime.utcnow().timestamp() * 1000)


def date_from_string(date, _format):
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(date, _format)))


def reformat(date, _format):
    return date.strftime(_format)


def curr_time_delta(**kwargs):
    return (datetime.datetime.utcnow(), datetime.datetime.utcnow() - datetime.timedelta(**kwargs))


def epoch_to_utctime(date, _format):
    return datetime.datetime.strftime(datetime.datetime.utcfromtimestamp(date), _format)


def get_updated_time(**kwargs):
    return datetime.datetime.utcnow() + datetime.timedelta(**kwargs)
