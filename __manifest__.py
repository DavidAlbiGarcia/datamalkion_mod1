# -*- coding: utf-8 -*-
{
    'name': "malkion",

    'summary': """
        Módulo para la gestión de toma de datos para la aplicación Asclepio""",

    'description': """
        Módulo que simplifica el trabajo de gestores de data.

        Características principales:
        - Gestión de contratos con sus datos requeridos.
        - Gestión de empleados, almacenes, equipo, puntos de interés y demas elementos implicados.
        - Gestión de plantillas de misión para la obtención de los datos requeridos.
        - Gestión de misiones hasta la entrega de datos a los gestores de Asclepios.
    """,

    'author': "David Albi Garcia",
    'website': "github.com/DavidAlbiGarcia/malkion",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Malkion',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'hr'],

    # always loaded
    'data': [
        # 'security/groups.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/dashboard_views.xml', # primero, copón!
        'views/contract_views.xml',
        'views/point_of_interest_views.xml',
        'views/almacenes_views.xml',
        'views/employee_views.xml',
        'views/transport_views.xml',
        'views/equipo_views.xml',
        'views/plantilla_views.xml',
        'views/orden_trabajo_views.xml',
        'views/mission_views.xml',
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
