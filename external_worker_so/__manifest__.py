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
    "depends": ['hr', 'project', 'website', 'contacts', 'portal', 'web', 'timesheet_grid', 'timer', 'industry_fsm'
                ],
    "data": [
        # Security
        'views/hr_employee_view.xml',
        'views/project_task_view.xml',
        'views/project_task_portal_templates.xml',
        # 'views/field_service_portal_templates.xml',
        'views/portal_field_service_templates.xml',
    ],
    "images": [],
    'assets': {
        'web._assets_primary_variables': [
        ],
        'web._assets_frontend_helpers': [
            'external_worker_so/static/src/js/portal_chatter.js',
        ],
        'web.assets_frontend': [
            'external_worker_so/static/src/js/portal_project_task.js',
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
