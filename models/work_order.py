from odoo import models, fields

class WorkOrder(models.Model):
    _name = 'malkion.work.order'
    _description = 'Orden de Trabajo'

    name = fields.Char(string='Nombre', required=True)
    data_request_id = fields.Many2one('malkion.data.request', string='Solicitud de Datos', required=True)
    contract_id = fields.Many2one('malkion.contract', string='Contrato', related='data_request_id.contract_id', store=True)
    creation_date = fields.Date(string='Fecha de Creación', default=fields.Date.today)

    assigned_manager_id = fields.Many2one('hr.employee', string='Jefe de Gestoría')
    team_manager_id = fields.Many2one('hr.employee', string='Gestor de Equipo')
    transport_managers_ids = fields.Many2many('hr.employee', string='Gestores de Transporte')
    hr_manager_id = fields.Many2one('hr.employee', string='Gestor de Empleados')

    mission_id = fields.One2many('malkion.mission', 'work_order_id', string='Misiones Generadas')  # futura relación
