from odoo import models, fields

class MalkionTransport(models.Model):
    _name = 'malkion.transport'
    _description = 'Transportes'

    name = fields.Char(string="Nombre", required=True)
    matricula = fields.Char(string="Matrícula", required=True)
    tipo = fields.Selection([
        ('coche', 'Coche'),
        ('moto', 'Moto'),
        ('furgoneta', 'Furgoneta'),
        ('camion', 'Camión'),
        ('otro', 'Otro'),
    ], string="Tipo", required=True)
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('asignado', 'Asignado'),
        ('de_baja', 'De baja'),
    ], string="Estado", required=True)
    capacidad = fields.Integer(string="Capacidad", required=True)
    fecha_adquisicion = fields.Date(string="Fecha de Adquisición")
    observaciones = fields.Text(string="Observaciones")
    fecha_itv = fields.Date(string="Fecha ITV")
    almacen_id = fields.Many2one('malkion.almacenes', string="Almacén al que pertenece", required=True)
