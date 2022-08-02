from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    architect_id = fields.Many2one('res.partner', string='Architect')
    c_supervisor_id = fields.Many2one('res.partner', string='Bouwbegeleider')
    contractor = fields.Many2one('res.partner', string='Aannemer')
    standard_payment = fields.Boolean(string='Standaard betaling')
    anders = fields.Char(string='Anders')
    measure = fields.Boolean(string='Inmeten')
    size_appointment = fields.Boolean(string='Maat Afspraak')
    installation = fields.Boolean(string='Installatie')
    delivery = fields.Boolean(string='Bezorgen')
    additional_explanation = fields.Text(string='Extra Toelichting')
    is_hinges_locks = fields.Boolean(string='Hang en sluitwerk')
    rubber_color = fields.Selection([
        ('Zwart', 'Zwart'),
        ('Bruin', 'Bruin'),
        ('Wit', 'Wit')],
        string='Rubber [kleur]')
    type_of_finish = fields.Selection([
        ('Primer', 'Primer'),
        ('Primer en aflakken', 'Primer en aflakken'),
        ('Transparent', 'Transparent'),
        ('Stain en transparent', 'Stain en transparent'),
        ('Onbehandeld', 'Onbehandeld')],
        string='Type afwerking')
    finish_color = fields.Char(string='Afwerking [kleur]')
    is_glas = fields.Boolean(string='Glas')
    glass_type = fields.Char(string='Glas type')
    special_order = fields.Boolean(string='Speciale bestelling')
    materials = fields.Text(string='Materialen')
    particularities = fields.Text(string='Bijzonderheden')

    def print_extra_line(self):
        return 700 * '_'
