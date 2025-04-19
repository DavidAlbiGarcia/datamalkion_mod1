# -*- coding: utf-8 -*-
# from odoo import http


# class Datamalkion(http.Controller):
#     @http.route('/datamalkion/datamalkion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/datamalkion/datamalkion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('datamalkion.listing', {
#             'root': '/datamalkion/datamalkion',
#             'objects': http.request.env['datamalkion.datamalkion'].search([]),
#         })

#     @http.route('/datamalkion/datamalkion/objects/<model("datamalkion.datamalkion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('datamalkion.object', {
#             'object': obj
#         })
