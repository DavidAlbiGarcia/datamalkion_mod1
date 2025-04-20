# -*- coding: utf-8 -*-
{
    'name': "datamalkion",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/malkion_dashboard_views.xml', # primero, copón!
        'views/malkion_contract_views.xml',
        'views/malkion_point_of_interest_views.xml',
        'views/malkion_almacenes_views.xml',
        'views/malkion_employee_views.xml',
        'views/malkion_transport_views.xml',
        'views/malkion_equipo_views.xml',
        'views/malkion_plantilla_views.xml',
        'views/malkion_orden_trabajo_views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
