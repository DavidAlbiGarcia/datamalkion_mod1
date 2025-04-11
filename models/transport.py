from odoo import models, fields

class Transport(models.Model):
    _name = 'malkion.transport'
    _description = 'Vehículo de transporte'

    name = fields.Char(string='Nombre o identificador del vehículo', required=True)
    license_plate = fields.Char(string='Matrícula', required=True)
    tipo = fields.Selection([
        ('coche', 'Coche'),
        ('furgoneta', 'Furgoneta'),
        ('camion', 'Camión'),
        ('otro', 'Otro')
    ], string='Tipo de vehículo', default='coche')

    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('asignado', 'Asignado'),
        ('revisión', 'En revisión'),
        ('baja', 'De baja')
    ], string='Estado', default='disponible')

    capacity = fields.Integer(string='Capacidad (kg o volumen)')
    fecha_adquisicion = fields.Date(string='Fecha de adquisición')
    observaciones = fields.Text(string='Observaciones')
