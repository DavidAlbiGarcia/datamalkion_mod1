from odoo import models, fields

class PointOfInterest(models.Model):
    _name = 'malkion_point_of_interest'
    _description = 'Punto de Interés'

    name = fields.Char(string="Nombre", required=True)
    _rec_name = 'name'  # Esto indica que Odoo usará 'name' como el campo principal para mostrar en las relaciones, bufff, la leche
    point_type = fields.Selection([
        ('recogida', 'Recogida'),
        ('medicion', 'Medición'),
        ('entrega', 'Entrega')
    ], string="Tipo de Punto", required=True)
    general_location = fields.Char(string="Lugar General", required=True)
    city = fields.Char(string="Ciudad", required=True)
    latitude = fields.Float(string="Latitud")
    longitude = fields.Float(string="Longitud")

