#!/usr/bin/env python
"""
This is a utility class used as factory to perform repetitive reports
across project to avoid code duplication.
"""

import random
import string

import jinja2
import requests
from flask_mail import Message
from flask_restplus import marshal
from jinja2 import Environment, FileSystemLoader

from rest import entity_mgmt_app, logger
from rest.utils.dateutils import get_current_time, reformat


def gen_pbook_yml(ip, role):
    r_text = ''
    template_loader = jinja2.FileSystemLoader(searchpath="/")
    template_env = jinja2.Environment(loader=template_loader)

    # Jinja template file location
    TEMPLATE_FILE = "/opt/ansible/playbook.jinja"
    template = template_env.get_template(TEMPLATE_FILE)

    # Make Role as an array if Multiple Roles are mentioned in the POST request
    role = role.split(',')

    r_text = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    temp_file = "/tmp/" + "ans-" + r_text + ".yml"  # Crating a unique playbook yml file
    template_vars = {
        "hst": ip,
        "roles": role
    }
    # Rendering template
    output_text = template.render(template_vars)
    text_file = open(temp_file, "w")

    # Saving the template output to the temp file
    text_file.write(output_text)
    text_file.close()
    return temp_file


def send_mail(mail_data, mail_type, content_type=""):
    if not isinstance(mail_data['recipients'], list):
        mail_data['recipients'] = [mail_data['recipients']]
    notification_path = f"{entity_mgmt_app.config.get('NOTIFICATION_MAIL_URL')}?type={mail_type}&content_type={content_type}"
    logger.info(notification_path)
    logger.info(mail_data)
    requests.post(notification_path, json=mail_data)


def send_mail_with_attachments(mail_data, mail_type, files, content_type=""):
    if isinstance(mail_data['recipients'], list):
        mail_data['recipients'] = ",".join(mail_data['recipients'])
    notification_path = f"{entity_mgmt_app.config.get('NOTIFICATION_MAIL_URL')}?type={mail_type}&content_type={content_type}"
    requests.post(notification_path, files=files, data=mail_data)


def send_mail_html(mail_id, sub, body, html_file):
    try:
        env = Environment(loader=FileSystemLoader(entity_mgmt_app.config['TEMPLATES_PATH']))
        tmpl = env.get_template(html_file)
        html = tmpl.render(body)
        msg = Message(sub, sender=entity_mgmt_app.config['MAIL_DEFAULT_SENDER'], recipients=mail_id, html=html)
        mail.send(msg)
    except Exception as e:
        print('Exception occure while sending mail', e)


def get_application_url():
    return f"{entity_mgmt_app.config.get('SCHEMA')}://{entity_mgmt_app.config.get('HOST')}:{entity_mgmt_app.config.get('PORT')}"


def custom_marshal(data, model, **kwargs):
    result = marshal(data, model, **kwargs)
    if "meta" in result:
        result['meta']['created'] = get_current_time().isoformat()
        result['meta']['updated'] = get_current_time().isoformat()
    return result


def get_dynamic_dir_name(backup_name):
    return f"{backup_name}-{reformat(get_current_time(),'%d-%m-%Y-%H:%M:%S')}"
