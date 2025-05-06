from odoo import models, fields

class MalkionPlantillaRol(models.Model):
    _name = 'malkion.plantilla_rol'
    _description = 'Plantilla de Roles'

    plantilla_id = fields.Many2one('malkion.plantilla', string="Plantilla")
    rol_id = fields.Many2one('hr.job', string="Rol")
    cantidad = fields.Integer("Cantidad")
