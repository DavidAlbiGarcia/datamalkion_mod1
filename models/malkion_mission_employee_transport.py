from odoo import models, fields

class MalkionMissionEmployeeTransport(models.Model):
    _name = 'malkion_mission_employee_transport'
    _description = 'Empleados Asignados al Transporte en Misión'

    mision_id = fields.Many2one('malkion_mission', string="Misión")
    empleado_id = fields.Many2one('hr.employee', string="Empleado")
    transporte_id = fields.Many2one('malkion_transport', string="Transporte")
