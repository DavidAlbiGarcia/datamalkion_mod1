from odoo import models, fields, api
import xml.etree.ElementTree as etree  # Importar etree
import logging
from odoo.exceptions import ValidationError

# Crear un logger
_logger = logging.getLogger(__name__)

class MalkionOrdenTrabajo(models.Model):
    _name = 'malkion_orden_trabajo'
    _description = 'Orden de trabajo'

    name = fields.Char(string="Nombre de la Orden de Trabajo", required=True)
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
    transporte_ids = fields.Many2many('malkion_transport', string="Transporte Necesario")

    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('mision_creada', 'Misión Creada')
    ], string="Estado", default='pendiente')

    # Campos para las cantidades (por ejemplo, cuántos coches, cuántos arqueros, etc.)
    cantidad_arquero = fields.Integer("Cantidad de Arqueros", default=0)
    cantidad_coche = fields.Integer("Cantidad de Coches", default=0)
    cantidad_guantes = fields.Integer("Cantidad de Guantes", default=0)

    @api.onchange('contrato_id')
    def _onchange_contrato(self):
        if self.contrato_id:
            self.dato_requerido = self.contrato_id.data_required  # Rellenar el dato requerido
            self.cliente_id = self.contrato_id.client_id.id  # Obtener el cliente asociado
        else:
            self.dato_requerido = False
            self.cliente_id = False  # Restablecer el cliente

            
        # Buscar la plantilla asociada al contrato
        plantilla = self.env['malkion_plantilla'].search([
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
            puntos_encontrados = self.env['malkion_point_of_interest'].search([('name', 'in', puntos_nombres)])

            # Asignar los puntos de interés encontrados a self.puntos_interes_ids
            self.puntos_interes_ids = [(6, 0, puntos_encontrados.ids)]
       
            # Asignar roles
            roles = xml_root.findall('roles_necesarios/role')
            for role in roles:
                # Crear la relación de roles necesarios si no existe
                rol_id = self.env['hr.job'].search([('name', '=', role.text)], limit=1)
                if rol_id:
                    self.empleados_roles = [(4, rol_id.id)]
            
            # Asignar equipo
            equipo = xml_root.findall('equipo_necesario/equipo')
            for equipo_tipo in equipo:
                equipo_id = self.env['malkion_equipo'].search([('name', '=', equipo_tipo.text)], limit=1)
                if equipo_id:
                    self.equipo_ids = [(4, equipo_id.id)]

            # Asignar transporte
            transporte = xml_root.findall('transporte_necesario/vehiculo')
            for vehiculo in transporte:
                transporte_id = self.env['malkion_transport'].search([('name', '=', vehiculo.text)], limit=1)
                if transporte_id:
                    self.transporte_ids = [(4, transporte_id.id)]

