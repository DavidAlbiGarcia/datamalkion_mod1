from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MalkionEmployee(models.Model):
    _inherit = 'hr.employee'

    # Campos adicionales
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ], string="Estado", default='activo', required=True)

    disponible = fields.Selection([
        ('disponible', 'Disponible'),
        ('no_disponible', 'No Disponible'),
    ], string="Disponibilidad", default='disponible', required=True)

    # Roles de los empleados
    roles = fields.Many2many('hr.job', string="Roles")

    # uso esta para que afecte no solo cambios formulario(por si le ponen inactivo desde código u otro formulario), sino usaría api.onchange
    def write(self, vals):
        if 'estado' in vals and vals['estado'] == 'inactivo':
            vals['disponible'] = 'no_disponible'
        return super().write(vals)
    
    @api.constrains('roles')
    def _check_roles(self):
        for employee in self:
            # Si el empleado tiene un rol exclusivo, no puede tener otros roles
            if any(role.name in ['Jefe Data', 'Gestor Equipo', 'Gestor Transporte', 'Gestor Hunters'] for role in employee.roles):
                if len(employee.roles) > 1:
                    raise ValidationError("Si el empleado tiene un rol exclusivo, no puede tener otros roles.")
                

