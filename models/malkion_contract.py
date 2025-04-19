from odoo import models, fields

class MalkionContract(models.Model):
    _name = 'malkion_contract' # _ pero da igual que se llame como archivo pues busca name? ¿no es convención . en names y _ en archivos? repreguntar, nah, recambiado
    _description = 'Contrato con el cliente'

    name = fields.Char(string="Nombre del contrato", required=True)
    client_id = fields.Many2one('res.partner', string="Cliente", required=True)
    contract_type = fields.Selection([
        ('standard', 'Estándar'),
        ('premium', 'Premium')
    ], string="Tipo de contrato", default='standard', required=True)
    start_date = fields.Date(string="Fecha de inicio", required=True)
    end_date = fields.Date(string="Fecha de fin")
    periodicity = fields.Selection([
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
        ('on_demand', 'Bajo demanda')
    ], string="Periodicidad", default='weekly', required=True)
    active = fields.Boolean(default=True)
    
    # Dato requerido: se describe manualmente
    # Empleado habla con cliente y crea entrada única en el XML para este contrato
    data_required = fields.Char(string="Dato Requerido", required=False, null=True) # cambiado de required=True por conflicto con db, solución temporal
