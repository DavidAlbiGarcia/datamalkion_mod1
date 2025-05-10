from odoo import models, fields

class MalkionEquipo(models.Model):
    _name = 'malkion.equipo'  # Cambiado de malkion.equipo a malkion_equipo
    _description = 'Equipo'

    # Campos
    name = fields.Char(string="Nombre del Equipo", required=True)
    serial_number = fields.Char(string="Número de Serie")
    tipo = fields.Selection([
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
    ], string="Tipo de Equipo", required=True)
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('asignado', 'Asignado'),
        ('de_baja', 'De Baja')
    ], string="Estado", default='disponible', required=True)
    fecha_adquisicion = fields.Date(string="Fecha de Adquisición")
    observaciones = fields.Text(string="Observaciones")
    
    # Relación con almacenes
    almacen_id = fields.Many2one('malkion.almacenes', string="Almacén al que pertenece", required=True)
