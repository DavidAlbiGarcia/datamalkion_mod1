from odoo import models, fields

class MalkionMissionEmployeeTeam(models.Model):
    _name = 'malkion_mission_employee_team'
    _description = 'Empleados Asignados al Equipo en Misión'

    mision_id = fields.Many2one('malkion_mission', string="Misión")
    empleado_id = fields.Many2one('hr.employee', string="Empleado")
    equipo_id = fields.Many2one('malkion_equipo', string="Equipo")
