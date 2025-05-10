from odoo import models, fields, api
import logging
from odoo.exceptions import ValidationError
from odoo.exceptions import AccessError

# Crear un logger
_logger = logging.getLogger(__name__)

class MalkionMission(models.Model):
    _name = 'malkion.mission'
    _description = 'Misión'

    name = fields.Char(string="Nombre de la Misión", required=True)
    puntos_interes_ids = fields.Many2many('malkion.point_of_interest', string="Puntos de Interés")
    
    jefe_data_id = fields.Many2one('hr.employee', string="Jefe de Datos")
    
    gestor_hunters_id = fields.Many2one('hr.employee', string="Gestor de Hunters")
    gestor_equipo_id = fields.Many2one('hr.employee', string="Gestor de Equipo")
    gestor_transportes_id = fields.Many2one('hr.employee', string="Gestor de Empleados")
    
    roles_ids = fields.Many2many('hr.employee', string="Roles")  # Relación muchos a muchos con empleados
    
    equipo_ids = fields.Many2many('malkion.equipo', string="Equipo")
    transporte_ids = fields.Many2many('malkion.transport', string="Transporte")

    # Relaciones ternarias: empleado - equipo / transporte
    empleados_equipo_ids = fields.One2many('malkion.mission_employee_team', 'mision_id', string="Empleados Asignados a Equipo")
    empleados_transporte_ids = fields.One2many('malkion.mission_employee_transport', 'mision_id', string="Empleados Asignados a Transporte")

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
        ('incidencia_encurso', 'Incidencia en curso'),
        ('dato_obtenido', 'Dato obtenido'),
        ('incidencia_datoobtenido', 'Incidencia al obtener dato'),
        ('dato_entregado', 'Dato entregado'),
        ('incidencia_datoentregado', 'Incidencia en entrega'),
        ('dato_procesando', 'Dato en procesamiento'),
        ('incidencia_datoprocesando', 'Incidencia en procesamiento'),
        ('finalizada', 'Finalizada'),
    ], default='iniciada', string="Estado")


    observaciones = fields.Text(string="Observaciones")


    def write(self, vals):
        if 'estado' in vals:
            if self.env.user.has_group('malkion.group_AGENTESCAMPO'):
                estados_prohibidos = ['finalizada', 'incidencia_datoprocesando', 'dato_procesando']
                if vals['estado'] in estados_prohibidos:
                    raise ValidationError("No tienes permiso para cambiar a este estado. Estados restringidos: Dato en procesamiento, Incidencia en procesamiento y Finalizada")
            elif self.env.user.has_group('malkion.group_ASCLEPIOS'):
                estados_permitidos = ['finalizada', 'incidencia_datoprocesando', 'dato_procesando']
                if vals['estado'] not in estados_permitidos:
                    raise ValidationError("Solo puedes cambiar el estado a Dato en procesamiento, Incidencia en procesamiento o Finalizada.")

            # código preparado por si decido liberar recursos en indicencia_datoprocesando, añadirlo a estados cierre y ya
            estados_cierre = ['finalizada']
            if vals['estado'] in estados_cierre:
                for empleado in self.roles_ids:
                    empleado.disponible = 'disponible'
                for equipo in self.equipo_ids:
                    equipo.estado = 'disponible'
                for transporte in self.transporte_ids:
                    transporte.estado = 'disponible'

        return super().write(vals)

