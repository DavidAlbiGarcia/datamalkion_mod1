from odoo import models, fields
from datetime import date, timedelta


class WizardEquipoAntiguo(models.TransientModel):
    _name = 'wizard.equipo.antiguo'
    _description = 'Asistente para informe de equipos antiguos'

    tipo = fields.Selection([
        ('guantes', 'Guantes'),
        ('recipienteA', 'Recipiente A'),
        ('traje', 'Traje'),
        ('cuerda', 'Cuerda'),
        ('sonda_agua', 'Sonda de agua'),
        ('kit_ph', 'Kit medidor de pH'),
        ('traje_bioseguridad', 'Traje de bioseguridad'),
        ('linterna', 'Linterna frontal'),
        ('medidor_gas', 'Medidor de gases'),
        ('sonda_lodo', 'Sonda para lodo'),
        ('georradar', 'Georradar portátil'),
        ('dosimetro', 'Dosímetro de radiación'),
        ('recipiente_biologico', 'Recipiente biológico'),
        ('filtro_agua', 'Filtro de agua portátil'),
        ('sensor_temperatura', 'Sensor de temperatura'),
        ('sensor_humedad', 'Sensor de humedad'),
        ('equipo_muestreo_aire', 'Equipo de muestreo de aire'),
        ('equipo_video', 'Equipo de grabación subterránea'),
        ('muestra_suelo', 'Kit para toma de muestras de suelo'),
        ('kit_quimico', 'Kit químico portátil'),
        ('herramienta_multifuncion', 'Herramienta multifunción')
    ], string="Tipo de equipo", required=True)
    # limite = fields.Date(string="Fecha límite", default=lambda self: date.today() - timedelta(days=730))


    def generate_report(self):
        tipo = self.tipo
        limite = (date.today() - timedelta(days=730)).isoformat()
        return self.env.ref('malkion.report_equipos_antiguos').report_action(
            self, data={'tipo': tipo, 'limite': limite}
        )

"""
    def generate_report(self):
        data = {
            'tipo':'guantes',
            'limite': '2025-12-12'
        }
        return self.env.ref('malkion.report_equipos_antiguos').report_action(self, data = data)



        def generate_report(self):
        data = {
            'tipo': self.tipo,
            'limite': (date.today() - timedelta(days=730)).isoformat(),
        }
        return {
            'type': 'ir.actions.report',
            'report_name': 'malkion.report_equipos_antiguos_template',
            'report_type': 'qweb-pdf',
            'data': data,
        }
"""
