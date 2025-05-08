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

    jefe_datos_id = fields.Many2one('hr.employee', string="Jefe de Datos", default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1))


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
        res = super(MalkionOrdenTrabajo, self).create(vals)
        if not self.env.context.get('no_auto_mission'):
            res.create_mission_from_order()
        return res

    
    def crear_mision_automatica_desde_plantilla(self):
        for orden in self:
            # usar create_mission_from_order directamente
            orden.create_mission_from_contract()
            # orden.estado = 'mision_creada'  # O
        return True

    @api.model
    def create_mission_from_contract(self):
        for contrato in self:
            # Buscar plantilla asociada al contrato
            plantilla = self.env['malkion.plantilla'].search([
            ('contrato_id', '=', self.contrato_id.id)
            ], limit=1)

            if not plantilla:
                raise ValidationError("No se encontró una plantilla para este contrato.")

            if not plantilla.xml_data:
                raise ValidationError("La plantilla no tiene datos XML.")

            import xml.etree.ElementTree as ET
            xml_root = ET.fromstring(plantilla.xml_data)

            # Obtener puntos de interés
            puntos_nombres = [p.text for p in xml_root.findall('puntos_interes/punto_recogida')]
            puntos_ids = self.env['malkion.point_of_interest'].search([('name', 'in', puntos_nombres)]).ids

            # Equipo necesario
            equipo_tipo_cant = [
                (e.text.split(" (")[0], int(e.text.split(" (")[1][:-1]))
                for e in xml_root.findall('equipo_necesario/equipo')
            ]
            equipo_ids = []
            for tipo, _ in equipo_tipo_cant:
                eq = self.env['malkion.equipo'].search([('tipo', '=', tipo)], limit=1)
                if eq:
                    equipo_ids.append(eq.id)

            # Transporte necesario
            transporte_tipo_cant = [
                (t.text.split(" (")[0], int(t.text.split(" (")[1][:-1]))
                for t in xml_root.findall('transporte_necesario/vehiculo')
            ]
            transporte_ids = []
            for tipo, _ in transporte_tipo_cant:
                tr = self.env['malkion.transport'].search([('tipo', '=', tipo)], limit=1)
                if tr:
                    transporte_ids.append(tr.id)

            # Leer roles desde el XML
            roles_info = []
            for role in xml_root.findall('roles_necesarios/role'):
                rol_name = role.find('role_name').text
                cantidad = int(role.find('cantidad').text)
                if rol_name and cantidad:
                    roles_info.append((rol_name.strip(), cantidad))

            empleado_por_rol = {}
            empleados_roles_ids = []

            for rol_name, cantidad in roles_info:
                empleados = self.env['hr.employee'].search(
                    [('roles.name', '=', rol_name)],
                    limit=cantidad
                )
                if empleados:
                    empleado_por_rol[rol_name] = empleados[0]  # uno para asignaciones
                    empleados_roles_ids += empleados.ids
                else:
                    raise ValidationError(f"No se encontraron empleados con el rol '{rol_name}'.")

            # Validar que 'Jefe de datos' tenga user_id
            # jefe_datos = empleado_por_rol.get('Jefe de datos')
            # _logger.info("Roles encontrados: %s", list(empleado_por_rol.keys()))
            # _logger.info("Jefe de datos: %s", jefe_datos and jefe_datos.name)            if not jefe_datos or not jefe_datos.user_id:
                 # raise ValidationError("El empleado con rol 'Jefe de datos' no tiene un usuario asignado (user_id).")
            # _logger.info("Tiene user_id: %s", jefe_datos and jefe_datos.user_id)

            # Obtener lista de empleados disponibles para roles variables
            empleados_disponibles = list(empleado_por_rol.values())


            
            jefe_datos = self.env['hr.employee'].search([('job_id.name', '=', 'Jefe de datos')], limit=1)
            if not jefe_datos:
                raise ValidationError("No se encontró un empleado con el rol obligatorio 'Jefe de datos'.")

            gestor_equipo = self.env['hr.employee'].search([('job_id.name', '=', 'Gestor de equipo')], limit=1)
            gestor_transportes = self.env['hr.employee'].search([('job_id.name', '=', 'Gestor de transportes')], limit=1)
            gestor_hunters = self.env['hr.employee'].search([('job_id.name', '=', 'Gestor de hunters')], limit=1)

            # Obtener lista de empleados disponibles para roles variables
            empleados_disponibles = list(empleado_por_rol.values())

            # Si hay al menos un empleado, usar el primero para ambos responsables (o usar dos distintos si quieres)
            if not empleados_disponibles:
                raise ValidationError("No hay empleados disponibles en los roles de la plantilla para asignar como responsables.")

            responsable_equipo = empleados_disponibles[0]
            responsable_transporte = empleados_disponibles[0] 

            orden_vals = {
                'name': f"Orden auto de {contrato.name}",
                'estado': 'iniciada',
                'observaciones': f"AutoGenerada desde contrato {contrato.name} el {fields.Date.today()}",
                'puntos_interes_ids': [(6, 0, puntos_ids)],
                'equipo_ids': [(6, 0, equipo_ids)],
                'transporte_ids': [(6, 0, transporte_ids)],
                'empleados_roles': [(6, 0, empleados_roles_ids)],
                'jefe_datos_id': jefe_datos.user_id.id,
                'gestor_equipo_id': gestor_equipo.id,
                'gestor_transporte_id': gestor_transportes.id,
                'gestor_empleados_id': gestor_hunters.id,
                'responsable_equipo_id': responsable_equipo.id,
                'responsable_transporte_id': responsable_transporte.id,
            }


            # Crear la orden de trabajo, lo que creará automáticamente la misión vía create()
            mission = self.env['malkion.mission'].with_context(no_auto_mission=True).create(orden_vals)


            return mission


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

  

