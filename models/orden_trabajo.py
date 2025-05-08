from odoo import models, fields, api
import xml.etree.ElementTree as etree  # Importar etree
import logging
from odoo.exceptions import ValidationError

# Crear un logger
_logger = logging.getLogger(__name__)

class MalkionOrdenTrabajo(models.Model):
    _name = 'malkion.orden_trabajo'
    _description = 'Orden de trabajo'

    name = fields.Char(string="Nombre de la Orden de Trabajo", required=True)
    cliente_id = fields.Many2one('res.partner', string="Cliente", required=True)
    contrato_id = fields.Many2one('malkion.contract', string="Contrato", required=True, domain="[('client_id', '=', cliente_id)]")
    dato_requerido = fields.Char(string="Dato Requerido")
    jefe_datos_id = fields.Many2one('res.users', string="Jefe de Datos", default=lambda self: self.env.user)
    gestor_equipo_id = fields.Many2one('hr.employee', string="Gestor de Equipo", domain="[('active', '=', True)]")
    gestor_transporte_id = fields.Many2one('hr.employee', string="Gestor de Transporte", domain="[('active', '=', True)]")
    gestor_empleados_id = fields.Many2one('hr.employee', string="Gestor de Empleados", domain="[('active', '=', True)]")

    puntos_interes_ids = fields.Many2many('malkion.point_of_interest', string="Puntos de Interés")
    empleados_roles = fields.Many2many('hr.employee', string="Empleados por Rol")
    equipo_ids = fields.Many2many('malkion.equipo', string="Equipo Necesario")
    transporte_ids = fields.Many2many('malkion.transport', string="Transporte Necesario")

    responsable_equipo_id = fields.Many2one(
        'hr.employee', 
        string="Responsable de Equipo"
    )
    responsable_transporte_id = fields.Many2one(
        'hr.employee', 
        string="Responsable de Transporte"
    )

    #Solucion temporal, mostrar datos en pantalla en lugar de crear dinámicamente los campos
    # Campos nuevos para almacenar datos extraídos del XML
    roles_str = fields.Char(string="Roles Necesarios")  # Mostrar como texto
    equipo_str = fields.Char(string="Equipo Necesario Cantidad")  # Mostrar como texto
    transporte_str = fields.Char(string="Transporte Necesario Cantidad")  # Mostrar como texto

    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('mision_creada', 'Misión Creada')
    ], string="Estado", default='pendiente')

    # Campos para las cantidades (por ejemplo, cuántos coches, cuántos arqueros, etc.)
    cantidad_arquero = fields.Integer("Cantidad de Arqueros", default=0)
    cantidad_coche = fields.Integer("Cantidad de Coches", default=0)
    cantidad_guantes = fields.Integer("Cantidad de Guantes", default=0)

    # Campos para decidir los encargados de equipo y transporte
    encargado_equipo_id = fields.Many2one('hr.employee', string="Encargado de Equipo")
    encargado_transporte_id = fields.Many2one('hr.employee', string="Encargado de Transporte")

    @api.model
    def create_mission_from_order(self):
        for orden in self:
            mission_vals = {
                'name': orden.name,
                'responsable_equipo_id': orden.responsable_equipo_id.id,
                'responsable_transporte_id': orden.responsable_transporte_id.id,
                'estado': 'iniciada',
                'observaciones': orden.dato_requerido,
                'jefe_data_id': orden.jefe_datos_id.id,
                'gestor_hunters_id': orden.gestor_empleados_id.id,
                'gestor_equipo_id': orden.gestor_equipo_id.id,
                'gestor_transportes_id': orden.gestor_transporte_id.id,
                'roles_ids': [(6, 0, orden.empleados_roles.ids)],
                'equipo_ids': [(6, 0, orden.equipo_ids.ids)],
                'transporte_ids': [(6, 0, orden.transporte_ids.ids)],
                'puntos_interes_ids': [(6, 0, orden.puntos_interes_ids.ids)], 
            }
            # Crear la misión a partir de los datos de la orden de trabajo
            mission = self.env['malkion.mission'].create(mission_vals)

            # Crear relaciones ternarias: empleado - equipo
            if orden.responsable_equipo_id and orden.equipo_ids:
                for eq in orden.equipo_ids:
                    self.env['malkion.mission_employee_team'].create({
                        'mision_id': mission.id,
                        'empleado_id': orden.responsable_equipo_id.id,
                        'equipo_id': eq.id,
                    })

            # Crear relaciones ternarias: empleado - transporte
            if orden.responsable_transporte_id and orden.transporte_ids:
                for tr in orden.transporte_ids:
                    self.env['malkion.mission_employee_transport'].create({
                        'mision_id': mission.id,
                        'empleado_id': orden.responsable_transporte_id.id,
                        'transporte_id': tr.id,
                    })

            return mission

    @api.model
    def create(self, vals):
        # Llamamos al método para crear la misión al guardar la orden de trabajo
        res = super(MalkionOrdenTrabajo, self).create(vals)
        res.create_mission_from_order()  # Crear misión al guardar la orden de trabajo
        return res

    @api.onchange('contrato_id')
    def _onchange_contrato(self):
        if self.contrato_id:
            self.dato_requerido = self.contrato_id.data_required  # Rellenar el dato requerido
            self.cliente_id = self.contrato_id.client_id.id  # Obtener el cliente asociado
        else:
            self.dato_requerido = False
            self.cliente_id = False  # Restablecer el cliente

            
        # Buscar la plantilla asociada al contrato
        plantilla = self.env['malkion.plantilla'].search([
            ('contrato_id', '=', self.contrato_id.id)
        ], limit=1)

        # Verificar si se encontró la plantilla
        if plantilla:
            _logger.info("Plantilla encontrada: %s", plantilla.name)  # Log de depuración
        else:
            _logger.warning("No se encontró la plantilla para el cliente %s y contrato %s", self.cliente_id.name, self.contrato_id.name)
                    
        # Si se encuentra la plantilla, cargar los datos
        if plantilla:
            if plantilla:
                _logger.info("Plantilla encontrada: %s", plantilla.name)
                _logger.info("Contenido del XML: %s", plantilla.xml_data)

            # Cargar XML desde la plantilla
            if plantilla.xml_data:
                xml_root = etree.fromstring(plantilla.xml_data)
                
                # Asignar puntos de interés
                # puntos_interes = xml_root.findall('puntos_interes/punto_recogida')
                # self.puntos_interes_ids = [(6, 0, [p.id for p in self.env['malkion_point_of_interest'].search([('name', 'in', [p.text for p in puntos_interes])]).ids])]

            # Buscar los puntos de interés en el XML
            puntos_interes = xml_root.findall('puntos_interes/punto_recogida')

            # Extraer los nombres de los puntos de interés
            puntos_nombres = [punto.text for punto in puntos_interes if punto.text]

            # Realizar una única búsqueda para todos los puntos de interés a la vez
            puntos_encontrados = self.env['malkion.point_of_interest'].search([('name', 'in', puntos_nombres)])

            # Asignar los puntos de interés encontrados a self.puntos_interes_ids
            self.puntos_interes_ids = [(6, 0, puntos_encontrados.ids)]

            # Asignar roles con cantidad
            roles = xml_root.findall('roles_necesarios/role')
            roles_nombres = []
            for role in roles:
                rol_name = role.find('role_name').text
                cantidad = role.find('cantidad').text
                if rol_name and cantidad:
                    roles_nombres.append(f"{rol_name} ({cantidad})")  # Agregar cantidad junto al rol

            self.roles_str = ", ".join(roles_nombres)  # Mostrar como texto
       

            
            
            # Asignar equipo
            equipo = xml_root.findall('equipo_necesario/equipo')
            equipo_nombres = [equipo.text for equipo in equipo if equipo.text]
            self.equipo_str = ", ".join(equipo_nombres)  # Mostrar como text


            # Asignar transporte
            transporte = xml_root.findall('transporte_necesario/vehiculo')
            transporte_nombres = [vehiculo.text for vehiculo in transporte if vehiculo.text]
            self.transporte_str = ", ".join(transporte_nombres)  # Mostrar como texto

  

