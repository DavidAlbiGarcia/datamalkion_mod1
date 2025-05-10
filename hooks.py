from odoo import api, SUPERUSER_ID

def post_init_hook_regenerar_xml(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    plantillas = env['malkion.plantilla'].search([])
    for plantilla in plantillas:
        plantilla.xml_data = plantilla.generar_xml()

# def post_init_hook(cr, registry):

    # No hace falta crear la misión: se generará automáticamente al cargar la orden 
   #  pass

   #  env = api.Environment(cr, SUPERUSER_ID, {})
# orden = env['malkion.orden_trabajo'].with_context(no_auto_mission=True).search([('name', '=', 'Orden Demo ACME')], limit=1)
  #  if orden:
   #     orden.create_mission_from_order()

"""
   



"""