from odoo import models, api

class WizardMissionReport(models.TransientModel):
    _name = 'wizard.mission.report'
    _description = 'Asistente para imprimir el informe de misiones'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        
        return res

    def action_print(self):
        # Obtener misiones
        missions = self.env['malkion.mission'].search([])

        return self.env.ref('malkion.report_malkion_mission').report_action(missions)
