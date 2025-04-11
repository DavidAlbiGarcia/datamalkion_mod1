from odoo import models, fields

class MalkionMissionTransport(models.Model):
    _name = 'malkion.mission.transport'
    _description = 'Asignación de transporte a misión y empleado'

    mission_id = fields.Many2one('malkion.mission', string='Misión', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Transportista', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo asignado', required=True)

    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('recogido', 'Recogido'),
        ('en ruta', 'En ruta'),
        ('devuelto', 'Devuelto')
    ], string='Estado del vehículo', default='pendiente')
