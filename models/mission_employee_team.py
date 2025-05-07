from odoo import models, fields

class MalkionMissionEmployeeTeam(models.Model):
    _name = 'malkion.mission_employee_team'
    _description = 'Empleados Asignados al Equipo en Misión'

    mision_id = fields.Many2one('malkion.mission', string="Misión")
    empleado_id = fields.Many2one('hr.employee', string="Empleado")
    equipo_id = fields.Many2one('malkion.equipo', string="Equipo")
