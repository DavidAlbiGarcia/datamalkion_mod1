from odoo import models, fields, api

class MalkionOrdenTrabajo(models.Model):
    _name = 'malkion_orden_trabajo'
    _description = 'Orden de trabajo'

    cliente_id = fields.Many2one('res.partner', string="Cliente", required=True)
    contrato_id = fields.Many2one('malkion_contract', string="Contrato", required=True, domain="[('client_id', '=', cliente_id)]")
    dato_requerido = fields.Char(string="Dato Requerido")
    jefe_datos_id = fields.Many2one('res.users', string="Jefe de Datos", default=lambda self: self.env.user)
    gestor_equipo_id = fields.Many2one('res.users', string="Gestor de Equipo", domain="[('active', '=', True)]")
    gestor_transporte_id = fields.Many2one('res.users', string="Gestor de Transporte", domain="[('active', '=', True)]")
    gestor_empleados_id = fields.Many2one('res.users', string="Gestor de Empleados", domain="[('active', '=', True)]")

    puntos_interes_ids = fields.Many2many('malkion_point_of_interest', string="Puntos de Interés")
    empleados_roles = fields.Many2many('hr.employee', string="Empleados por Rol")
    equipo_ids = fields.Many2many('malkion_equipo', string="Equipo Necesario")
    transporte_ids = fields.Many2many('malkion_transporte', string="Transporte Necesario")

    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('mision_creada', 'Misión Creada')
    ], string="Estado", default='pendiente')
    
    @api.onchange('contrato_id')
    def _onchange_contrato(self):
        if self.contrato_id:
            self.dato_requerido = self.contrato_id.data_required
            # Aquí puedes actualizar los campos adicionales, como puntos de interés, roles, etc.

    def crear_mision(self):
        # Método que crea la misión y la asigna al estado "Iniciada".
        mision = self.env['malkion_mision'].create({
            'orden_trabajo_id': self.id,
            'estado': 'iniciada',
            # Rellenar más campos según sea necesario
        })
        self.estado = 'mision_creada'
        return mision

