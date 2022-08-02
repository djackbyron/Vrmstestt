# -*- coding: utf-8 -*-

{
    "name": "External Worker Enhancement",
    "summary": """""",
    "category": "",
    "version": "15.0.0.1.0.0",
    "sequence": 1,
    "author": "",
    "license": "LGPL-3",
    "website": "",
    "description": """External Worker Enhancement""",
    "live_test_url": "",
    "depends": ['hr', 'project', 'website', 'contacts', 'portal', 'web'
                ],
    "data": [
        # Security
        'views/hr_employee_view.xml',
        'views/project_task_view.xml',
    ],
    "images": [],
    'assets': {
        'web._assets_primary_variables': [
        ],
        'web._assets_frontend_helpers': [
            'external_worker_so/static/src/js/portal_chatter.js',
        ],
        'web.assets_frontend': [
        ],
        'web.assets_tests': [
        ],
        'web.assets_qweb': [
            'external_worker_so/static/src/xml/portal_chatter.xml',
        ],
    },
    "application": False,
    "installable": True,
    "auto_install": False,
}
