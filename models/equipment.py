from odoo import models, fields

class Equipment(models.Model):
    _name = 'malkion.equipment'
    _description = 'Equipo técnico'

    name = fields.Char(string='Nombre del equipo', required=True)
    description = fields.Text(string='Descripción')
    serial_number = fields.Char(string='Número de serie')
    state = fields.Selection([
        ('disponible', 'Disponible'),
        ('asignado', 'Asignado'),
        ('revisión', 'En revisión'),
        ('baja', 'De baja')
    ], string='Estado', default='disponible')

    fecha_adquisicion = fields.Date(string='Fecha de adquisición')
    observaciones = fields.Text(string='Observaciones')
