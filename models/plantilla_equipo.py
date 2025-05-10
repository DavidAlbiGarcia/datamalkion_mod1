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
        ('sonda_agua', 'Sonda de agua'),
        ('kit_ph', 'Kit medidor de pH'),
        ('traje_bioseguridad', 'Traje de bioseguridad'),
        ('linterna', 'Linterna frontal'),
        ('medidor_gas', 'Medidor de gases'),
        ('sonda_lodo', 'Sonda para lodo'),
        ('georradar', 'Georradar portátil'),
        ('dosimetro', 'Dosímetro de radiación'),
        ('recipiente_biologico', 'Recipiente biológico'),
        ('filtro_agua', 'Filtro de agua portátil'),
        ('sensor_temperatura', 'Sensor de temperatura'),
        ('sensor_humedad', 'Sensor de humedad'),
        ('equipo_muestreo_aire', 'Equipo de muestreo de aire'),
        ('equipo_video', 'Equipo de grabación subterránea'),
        ('muestra_suelo', 'Kit para toma de muestras de suelo'),
        ('kit_quimico', 'Kit químico portátil'),
        ('herramienta_multifuncion', 'Herramienta multifunción')
    ], string="Tipo de Equipo")
    cantidad = fields.Integer("Cantidad Necesaria", default=1)