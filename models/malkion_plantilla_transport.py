from odoo import models, fields

class MalkionPlantillaTransporte(models.Model):
    _name = 'malkion_plantilla_transport'
    _description = 'Transporte Necesario para Plantilla'

    plantilla_id = fields.Many2one('malkion_plantilla', string="Plantilla")
    transporte_tipo = fields.Selection([
        ('coche', 'Coche'),
        ('moto', 'Moto'),
        ('camion', 'Camión'),
        ('furgoneta', 'Furgoneta'),
        ('otro', 'Otro'),
    ], string="Tipo de Transporte")
    cantidad = fields.Integer("Cantidad Necesaria", default=1)