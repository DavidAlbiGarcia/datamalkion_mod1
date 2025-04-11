from odoo import models, fields

class MalkionMissionEquipment(models.Model):
    _name = 'malkion.mission.equipment'
    _description = 'Asignación de equipo a misión y empleado'

    mission_id = fields.Many2one('malkion.mission', string='Misión', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Empleado asignado', required=True)
    equipment_id = fields.Many2one('stock.production.lot', string='Equipo asignado', required=True)  # o stock.quant si lo prefieres

    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('asignado', 'Asignado'),
        ('usado', 'Usado'),
        ('devuelto', 'Devuelto')
    ], string='Estado del equipo', default='pendiente')
