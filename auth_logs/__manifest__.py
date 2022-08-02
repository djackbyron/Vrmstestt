# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Access Logs",
    'summary': """Access Rights for logs""",
    'description': """
Access Rights for logs
    """,
    'version': '1.0',
    'depends': ['base','web'],
    'auto_install': True,
    'data': [
        'data/groups.xml'
    ],
    'assets': {
        'web.assets_qweb': [
            'auth_logs/static/src/xml/new_message_action_list.xml',
        ],
    'web.assets_backend': [
        'auth_logs/static/src/js/*.js',
    ],
    },
    'license': 'LGPL-3',
}
