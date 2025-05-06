from odoo import models, fields

class MalkionPlantillaEquipo(models.Model):
    _name = 'malkion.plantilla_equipo'
    _description = 'Equipo Necesario para Plantilla'

    plantilla_id = fields.Many2one('malkion.plantilla', string="Plantilla")
    equipo_tipo = fields.Selection([
        ('guantes', 'Guantes'),
        ('recipienteA', 'Recipiente A'),
        ('traje', 'Traje'),
        ('cuerda', 'Cuerda'),
        ('otro', 'Otro'),
    ], string="Tipo de Equipo")
    cantidad = fields.Integer("Cantidad Necesaria", default=1)