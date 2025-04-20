from odoo import models, fields

class MalkionEquipo(models.Model):
    _name = 'malkion_equipo'  # Cambiado de malkion.equipo a malkion_equipo
    _description = 'Equipo'

    # Campos
    name = fields.Char(string="Nombre del Equipo", required=True)
    _rec_name = 'name'  # Esto indica que Odoo usará 'name' como el campo principal para mostrar en las relaciones, bufff, la leche
    serial_number = fields.Char(string="Número de Serie")
    tipo = fields.Selection([
        ('guantes', 'Guantes'),
        ('recipienteA', 'Recipiente A'),
        ('traje', 'Traje'),
        ('cuerda', 'Cuerda')
    ], string="Tipo de Equipo", required=True)
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('asignado', 'Asignado'),
        ('de_baja', 'De Baja')
    ], string="Estado", default='disponible', required=True)
    fecha_adquisicion = fields.Date(string="Fecha de Adquisición")
    observaciones = fields.Text(string="Observaciones")
    
    # Relación con almacenes
    almacen_id = fields.Many2one('malkion_almacenes', string="Almacén al que pertenece", required=True)
