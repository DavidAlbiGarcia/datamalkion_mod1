from odoo import models, fields

class MalkionAlmacenes(models.Model):
    _name = 'malkion_almacenes'  # Aquí usamos el _name como malkion_almacenes
    _description = 'Almacenes'

    name = fields.Char(string="Nombre del Almacén", required=True)
    tipo_almacen = fields.Selection([('equipo', 'Equipo'),
                                     ('transporte', 'Transporte')], string="Tipo de Almacén", required=True)
    ubicacion_general = fields.Char(string="Ubicación General")
    ciudad = fields.Char(string="Ciudad")
    latitud = fields.Float(string="Latitud")  # Campo para la latitud
    longitud = fields.Float(string="Longitud")  # Campo para la longitud
