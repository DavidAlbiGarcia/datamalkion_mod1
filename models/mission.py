from odoo import models, fields

class MalkionMission(models.Model):
    _name = 'malkion.mission'
    _description = 'Misión de recogida de datos'

    name = fields.Char(string='Nombre', required=True)
    work_order_id = fields.Many2one('malkion.work.order', string='Orden de Trabajo', required=True)

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('pending', 'Pendiente'),
        ('assigned', 'Asignada'),
        ('in_progress', 'En curso'),
        ('delivered', 'Entregada'),
        ('done', 'Finalizada'),
        ('failed', 'Fallida')
    ], string='Estado', default='draft')

    # Nuevos campos para fecha de inicio y fin
    start_date = fields.Datetime(string='Fecha de Inicio', required=True)
    end_date = fields.Datetime(string='Fecha de Fin', required=True)

    # Relaciones ternarias
    employee_equipment_ids = fields.One2many('malkion.mission.equipment', 'mission_id', string='Asignaciones de equipo')
    employee_transport_ids = fields.One2many('malkion.mission.transport', 'mission_id', string='Asignaciones de transporte')

    equipment_pickup_date = fields.Datetime(string='Fecha recogida equipo')
    equipment_return_date = fields.Datetime(string='Fecha devolución equipo')

    transport_pickup_date = fields.Datetime(string='Fecha recogida transporte')
    transport_return_date = fields.Datetime(string='Fecha devolución transporte')

    # Relaciones 1:1 con los managers y jefe
    manager_jefe_id = fields.Many2one('hr.employee', string='Jefe de Misión', domain=[('job_id.name', '=', 'Jefe de Misión')])
    manager_team_id = fields.Many2one('hr.employee', string='Manager de Equipo', domain=[('job_id.name', '=', 'Manager de Equipo')])
    manager_transport_ids = fields.Many2one('hr.employee', string='Manager de Transporte', domain=[('job_id.name', '=', 'Manager de Transporte')])

    # Asignación de empleados de la misión
    employee_assignments_ids = fields.Many2many('hr.employee', string='Empleados Asignados')

