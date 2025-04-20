from odoo import models, fields, api
from odoo.exceptions import ValidationError
import xml.etree.ElementTree as ET

class MalkionPlantilla(models.Model):
    _name = 'malkion_plantilla'
    _description = 'Plantillas para Contratos'

    nombre = fields.Char("Nombre de la Plantilla", required=True)
    client_id = fields.Many2one('res.partner', string="Cliente", required=True)
    contrato_id = fields.Many2one(
        'malkion_contract', 
        string="Contrato", 
        required=True,
        domain="[('client_id', '=', client_id)]"  # Filtrar por cliente
    )
    data_required = fields.Char(string="Dato Requerido")
    
    puntos_interes_ids = fields.Many2many('malkion_point_of_interest', string="Puntos de Interés")
    
    # Relación Many2many con los modelos intermedios para roles
    roles_necesarios_ids = fields.One2many('malkion_plantilla_rol', 'plantilla_id', string="Roles Necesarios")

    # Relación Many2many con los modelos intermedios
    equipo_necesario_ids = fields.One2many('malkion_plantilla_equipo', 'plantilla_id', string="Equipo Necesario")
    transporte_necesario_ids = fields.One2many('malkion_plantilla_transport', 'plantilla_id', string="Transporte Necesario")
    
    xml_data = fields.Text("XML de la Plantilla")

    # Método onchange para actualizar el campo data_required
    @api.onchange('contrato_id')
    def _onchange_contrato(self):
        if self.contrato_id:
            self.data_required = self.contrato_id.data_required

    def generar_xml(self):
        # Crear el elemento raíz del XML
        plantilla = ET.Element("plantilla")
        
        # Agregar el cliente y datos generales
        cliente = ET.SubElement(plantilla, "cliente")
        cliente.text = self.cliente_id.name
        dato_requerido = ET.SubElement(plantilla, "dato_requerido")
        dato_requerido.text = self.dato_requerido if self.dato_requerido else ''
        
        contrato = ET.SubElement(plantilla, "contrato")
        contrato_id = ET.SubElement(contrato, "id_contrato")
        contrato_id.text = str(self.contrato_id.id)

        # Puntos de interés
        puntos_interes = ET.SubElement(plantilla, "puntos_interes")
        for punto in self.puntos_interes_ids:
            punto_recogida = ET.SubElement(puntos_interes, "punto_recogida")
            punto_recogida.text = punto.name

        # Roles necesarios
        roles_necesarios = ET.SubElement(plantilla, "roles_necesarios")
        for rol in self.roles_necesarios_ids:
            role = ET.SubElement(roles_necesarios, "role")
            role_name = ET.SubElement(role, "role_name")
            role_name.text = rol.rol_id.name  # 'rol_id' hace referencia al campo Many2one hacia 'hr.job'
            
            cantidad = ET.SubElement(role, "cantidad")
            cantidad.text = str(rol.cantidad)  # Aquí tomas la cantidad de roles necesarios

        # Equipo necesario (con tipos y cantidades)
        equipo_necesario = ET.SubElement(plantilla, "equipo_necesario")
        for equipo in self.equipo_necesario_ids:
            equipo_item = ET.SubElement(equipo_necesario, "equipo")
            equipo_item.text = f"{equipo.equipo_tipo} ({equipo.cantidad})"  # Tipo de equipo y cantidad

        # Transporte necesario (con tipos y cantidades)
        transporte_necesario = ET.SubElement(plantilla, "transporte_necesario")
        for transporte in self.transporte_necesario_ids:
            transport_item = ET.SubElement(transporte_necesario, "vehiculo")
            transport_item.text = f"{transporte.transporte_tipo} ({transporte.cantidad})"  # Tipo de transporte y cantidad

        # Generar y almacenar el XML
        tree = ET.ElementTree(plantilla)
        xml_str = ET.tostring(plantilla, encoding="unicode", method="xml")
        self.xml_data = xml_str
        return xml_str
