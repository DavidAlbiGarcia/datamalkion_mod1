from odoo import models, fields

class MalkionMissionEmployeeTransport(models.Model):
    _name = 'malkion.mission_employee_transport'
    _description = 'Empleados Asignados al Transporte en Misión'

    mision_id = fields.Many2one('malkion.mission', string="Misión")
    empleado_id = fields.Many2one('hr.employee', string="Empleado")
    transporte_id = fields.Many2one('malkion.transport', string="Transporte")
