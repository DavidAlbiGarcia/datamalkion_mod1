from odoo import models, api

class WizardRecursosReport(models.TransientModel):
    _name = 'wizard.recursos.report'
    _description = 'Asistente para imprimir el informe de recursos asignados'

    def action_print(self):
        missions = self.env['malkion.mission'].search([])
        return self.env.ref('malkion.report_malkion_recursos').report_action(missions)
