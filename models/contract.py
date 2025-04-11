# models/contract.py
# INFIERNO PRUEBA
from odoo import models, fields, api

class MalkionContract(models.Model):
    _name = 'malkion.contract'
    _description = 'Contrato con el cliente'

    name = fields.Char(string="Nombre del contrato", required=True)
    client_id = fields.Many2one('res.partner', string="Cliente", required=True)
    contract_type = fields.Selection([
        ('standard', 'Estándar'),
        ('premium', 'Premium')
    ], string="Tipo de contrato", default='standard', required=True)
    start_date = fields.Date(string="Fecha de inicio", required=True)
    end_date = fields.Date(string="Fecha de fin")
    periodicity = fields.Selection([
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
        ('on_demand', 'Bajo demanda')
    ], string="Periodicidad", default='weekly', required=True)
    active = fields.Boolean(default=True)

    data_request_ids = fields.One2many('malkion.data.request', 'contract_id', string="Solicitudes de datos")
