from odoo import models

class ReportEquiposAntiguos(models.AbstractModel):
    _name = 'report.malkion.report_equipos_antiguos_template'
    _description = 'Informe de equipos antiguos (parser)'

    def _get_report_values(self, docids, data=None):
        # Si no llega data, prevenir error
        if not data:
            data = {}

        return {
            'doc_ids': docids,
            'doc_model': 'wizard.equipo.antiguo',
            'docs': self.env['wizard.equipo.antiguo'].browse(docids),
            'data': data,
        }
