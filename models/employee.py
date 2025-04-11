from odoo import models, fields

class Employee(models.Model):
    _inherit = 'hr.employee'

    is_field_worker = fields.Boolean(string="Empleado operativo")
    role_type = fields.Selection([
        ('archer', 'Arquero'),
        ('hunter', 'Cazador'),
        ('gatherer', 'Recolector'),
    ], string="Rol operativo")

    can_be_team_manager = fields.Boolean(string="Puede ser gestor de empleados")
    can_be_equipment_manager = fields.Boolean(string="Puede ser gestor de equipos")
    can_be_transport_manager = fields.Boolean(string="Puede ser gestor de transporte")
    is_mission_supervisor = fields.Boolean(string="Es jefe de gestoría")
