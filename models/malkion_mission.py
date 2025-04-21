from odoo import models, fields, api
import logging
from odoo.exceptions import ValidationError

# Crear un logger
_logger = logging.getLogger(__name__)

class MalkionMission(models.Model):
    _name = 'malkion_mission'
    _description = 'Misión'

    name = fields.Char(string="Nombre de la Misión", required=True)
    puntos_interes_ids = fields.Many2many('malkion_point_of_interest', string="Puntos de Interés")
    
    jefe_data_id = fields.Many2one('hr.employee', string="Jefe de Datos")
    gestor_hunters_id = fields.Many2one('hr.employee', string="Gestor de Hunters")
    gestor_equipo_id = fields.Many2one('hr.employee', string="Gestor de Equipo")
    gestor_transportes_id = fields.Many2one('hr.employee', string="Gestor de Empleados")
    
    roles_ids = fields.Many2many('hr.employee', string="Roles")  # Relación muchos a muchos con empleados
    
    equipo_ids = fields.Many2many('malkion_equipo', string="Equipo")
    transporte_ids = fields.Many2many('malkion_transport', string="Transporte")

    # Relaciones ternarias: empleado - equipo / transporte
    empleados_equipo_ids = fields.One2many('malkion_mission_employee_team', 'mision_id', string="Empleados Asignados a Equipo")
    empleados_transporte_ids = fields.One2many('malkion_mission_employee_transport', 'mision_id', string="Empleados Asignados a Transporte")

    # 
    # Dejo el filtrado por el momento
    #
    responsable_equipo_id = fields.Many2one(
        'hr.employee', 
        string="Responsables de Equipo",
        help="Empleados asignados como responsables de equipo"
    )

    responsable_transporte_id = fields.Many2one(
        'hr.employee', 
        string="Responsables de Transporte",
        help="Empleados asignados como responsables de transporte"
    )

    estado = fields.Selection([
        ('iniciada', 'Iniciada'),
        ('en_curso', 'En Curso'),
        ('finalizada', 'Finalizada'),
    ], default='iniciada', string="Estado")

    observaciones = fields.Text(string="Observaciones")




''' why falla esto? whyyyy? ok, domain de un many to many en un one2many que es la ternaria
        # Nuevos campos para responsables (lógica no de código (de negocio, vamos) no clara del todo pero bueno)
    responsables_equipo_ids = fields.Many2many(
        'hr.employee', 
        string="Responsables de Equipo", 
        domain="[('id', 'in', empleados_equipo_ids)]"
    )
    

    responsables_transporte_ids = fields.Many2many( 
        'hr.employee', 
        string="Responsables de Transporte", 
        domain="[('id', 'in', empleados_transporte_ids)]"
    )



    extra:
        @api.onchange('empleados_equipo_ids')
    def _onchange_empleados_equipo_ids(self):
        if self.empleados_equipo_ids:
            empleados_ids = self.empleados_equipo_ids.mapped('empleado_id').ids
            self.responsable_equipo_id = empleados_ids[0] if empleados_ids else False  # Asignar el primer empleado

    @api.onchange('empleados_transporte_ids')
    def _onchange_empleados_transporte_ids(self):
        if self.empleados_transporte_ids:
            empleados_ids = self.empleados_transporte_ids.mapped('empleado_id').ids
            self.responsable_transporte_id = empleados_ids[0] if empleados_ids else False


Con este casi iba el filtrado:

    @api.onchange('roles_ids')
    def _onchange_roles_ids(self):
        """
        Filtrar empleados en roles_ids para ser seleccionados como responsables de equipo o transporte.
        Este método actualizará los campos responsables según los empleados en roles_ids.
        """
        if self.roles_ids:
            empleados_ids = self.roles_ids.ids  # Obtener los IDs de los empleados en roles_ids
            _logger.info("Empleados en roles_ids: %s", empleados_ids)  # Verifica los IDs de empleados
            # Limpiar responsables antes de asignar nuevos valores
            self.responsable_equipo_id = False
            self.responsable_transporte_id = False
            # Ahora puedes elegir empleados para cada campo
            # Actualizamos el responsable de equipo con el primer empleado de roles_ids (solo si hay empleados)
            if empleados_ids:
                self.responsable_equipo_id = empleados_ids[0]
                self.responsable_transporte_id = empleados_ids[0]  # Usamos el primer empleado también para transporte si es necesario
'''