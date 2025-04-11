from odoo import models, fields, api

class DataRequest(models.Model):
    _name = 'malkion.data.request'
    _description = 'Solicitud de Datos'

    name = fields.Char(string='Nombre', required=True)
    contract_id = fields.Many2one('malkion.contract', string='Contrato', required=True)
    request_date = fields.Date(string='Fecha de Solicitud', default=fields.Date.today)
    data_type = fields.Char(string='Tipo de Dato Requerido')
    request_type = fields.Selection([  
        ('type_1', 'Tipo 1'),
        ('type_2', 'Tipo 2'),
        ('type_3', 'Tipo 3')
    ], string="Tipo de Solicitud", required=True)

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('approved', 'Aprobada'),
        ('in_progress', 'En Proceso'),
        ('done', 'Finalizada')
    ], default='draft', string='Estado')
