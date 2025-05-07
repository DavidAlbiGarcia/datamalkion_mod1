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
            mission = self.env['mission'].create(mission_vals)
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
        plantilla = self.env['plantilla'].search([
            ('contrato_id', '=', self.contrato_id.id)
        ], limit=1)

        # Verificar si se encontró la plantilla
        if plantilla:
            _logger.info("Plantilla encontrada: %s", plantilla.nombre)  # Log de depuración
        else:
            _logger.warning("No se encontró la plantilla para el cliente %s y contrato %s", self.cliente_id.name, self.contrato_id.name)
                    
        # Si se encuentra la plantilla, cargar los datos
        if plantilla:
            if plantilla:
                _logger.info("Plantilla encontrada: %s", plantilla.nombre)
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
            puntos_encontrados = self.env['point_of_interest'].search([('name', 'in', puntos_nombres)])

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
       
            ''' Funciona, pero sin cantidad
            # Asignar roles
            roles = xml_root.findall('roles_necesarios/role')
            roles_nombres = [role.find('role_name').text for role in roles if role.find('role_name').text]
            self.roles_str = ", ".join(roles_nombres)  # Mostrar como texto
            '''

            '''
            # Asignar roles
            roles = xml_root.findall('roles_necesarios/role')
            for role in roles:
                # Crear la relación de roles necesarios si no existe
                rol_id = self.env['hr.job'].search([('name', '=', role.text)], limit=1)
                if rol_id:
                    self.empleados_roles = [(4, rol_id.id)]
            '''
            
            
            # Asignar equipo
            equipo = xml_root.findall('equipo_necesario/equipo')
            equipo_nombres = [equipo.text for equipo in equipo if equipo.text]
            self.equipo_str = ", ".join(equipo_nombres)  # Mostrar como text
            '''
            for equipo_tipo in equipo:
                equipo_id = self.env['malkion_equipo'].search([('name', '=', equipo_tipo.text)], limit=1)
                if equipo_id:
                    self.equipo_ids = [(4, equipo_id.id)]
            '''

            # Asignar transporte
            transporte = xml_root.findall('transporte_necesario/vehiculo')
            transporte_nombres = [vehiculo.text for vehiculo in transporte if vehiculo.text]
            self.transporte_str = ", ".join(transporte_nombres)  # Mostrar como texto

            '''
            for vehiculo in transporte:
                transporte_id = self.env['malkion_transport'].search([('name', '=', vehiculo.text)], limit=1)
                if transporte_id:
                    self.transporte_ids = [(4, transporte_id.id)]
            '''
''' Restos de intentos como referencia:
            # Asignar roles y generar campos dinámicos
            roles = xml_root.findall('roles_necesarios/role')
            for role in roles:
                rol_name = role.find('role_name').text
                cantidad = int(role.find('cantidad').text)

                # Buscar el rol en la base de datos
                rol_id = self.env['hr.job'].search([('name', '=', rol_name)], limit=1)
                
                if rol_id:
                    # Crear los registros de empleados necesarios según la cantidad
                    for _ in range(cantidad):
                        self.empleados_roles = [(0, 0, {
                            'role_id': rol_id.id,
                            # El campo `empleado_id` puede dejarse vacío para selección posterior
                        })]
                else:
                    raise ValidationError(f"El rol '{rol_name}' no está registrado en la base de datos.")

            # Asignar equipo
            equipo = xml_root.findall('equipo_necesario/equipo')
            for equipo_tipo in equipo:
                equipo_id = self.env['malkion_equipo'].search([('name', '=', equipo_tipo.text)], limit=1)
                if equipo_id:
                    self.equipo_ids = [(4, equipo_id.id)]

    @api.model
    def cargar_plantilla(self, xml_data):
        # Parsear el XML
        xml_root = ET.fromstring(xml_data)

        # Leer los roles y cantidades del XML
        roles = xml_root.findall('roles_necesarios/role')
        for role in roles:
            rol_name = role.find('role_name').text
            cantidad = int(role.find('cantidad').text)

            # Buscar el rol en la base de datos
            rol_id = self.env['hr.job'].search([('name', '=', rol_name)], limit=1)
            
            if rol_id:
                # Crear los registros de empleados necesarios según la cantidad
                for _ in range(cantidad):
                    # Crear un registro en `roles_empleados` para cada rol y su correspondiente empleado
                    self.roles_empleados = [(0, 0, {
                        'role_id': rol_id.id,
                        # En este punto, el campo `empleado_id` puede dejarse vacío para seleccionar más tarde
                    })]
            else:
                # Si no se encuentra el rol, lanzar un error
                raise ValidationError(f"El rol '{rol_name}' no está registrado en la base de datos.")
        
        return True

    roles_empleados = fields.One2many('malkion.orden_trabajo.empleado', 'orden_trabajo_id', string="Empleados por Rol")

    @api.model
    def crear_roles_y_empleados(self, xml_data):
        # Parsear el XML
        xml_root = ET.fromstring(xml_data)

        # Procesar roles y cantidades
        roles = xml_root.findall('roles_necesarios/role')
        for role in roles:
            rol_name = role.find('role_name').text
            cantidad = int(role.find('cantidad').text)

            # Buscar el rol en la base de datos
            rol_id = self.env['hr.job'].search([('name', '=', rol_name)], limit=1)
            
            if rol_id:
                # Crear los registros de empleados necesarios
                for _ in range(cantidad):
                    self.roles_empleados = [(0, 0, {
                        'role_id': rol_id.id,
                        
                    })]
            else:
                raise ValidationError(f"El rol '{rol_name}' no está registrado en la base de datos.")

        return True

class EmpleadoRol(models.Model):
    _name = 'malkion.orden_trabajo.empleado'
    _description = 'Empleado por Rol'

    orden_trabajo_id = fields.Many2one('malkion_orden_trabajo', string="Orden de Trabajo")
    role_id = fields.Many2one('hr.job', string="Rol")

    empleado_id = fields.Many2one('hr.employee', string="Empleado", domain="[('job_id', '=', role_id)]")
                    <!-- Roles Necesarios -->
                    <group string="Roles Necesarios">
                        <field name="roles_empleados">
                            <form>
                                <group>
                                    <field name="role_id" string="Rol"/>
                                    <field name="empleado_id" string="Empleado"/>
                                </group>
                            </form>
                        </field>
                    </group>

'''

