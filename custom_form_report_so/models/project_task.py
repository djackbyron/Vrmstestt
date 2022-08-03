# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class TaskInherit(models.Model):
    _inherit = "project.task"

    order_type_explanation = fields.Char(string="Type order (Toelichting):")
    levering_explanation = fields.Char(string="Levering (Toelichting):")
    finish_ral = fields.Char(string="Afwerking (RAL):")
    particularities = fields.Char(string="Bijzonderheden:")
    order_type = fields.Selection(
        [('Inmeten', 'Inmeten'), ('Maat afspraak', 'Maat afspraak'), ('Combinatie', 'Combinatie')],
        string='Type order:')
    project_type = fields.Selection(
        [('Renovatie', 'Renovatie'), ('Nieuwbouw', 'Nieuwbouw')],
        string='Type project:')
    levering_type = fields.Selection(
        [('Installatie', 'Installatie'), ('Bezorgen', 'Bezorgen'), ('Afhalen', 'Afhalen'),
         ('Combinatie', 'Combinatie')],
        string='Levering Type:')
    hinge_locks = fields.Selection(
        [('Ja - Vermaas', 'Ja - Vermaas'), ('Nee - Klant', 'Nee - Klant'), ('Combinatie', 'Combinatie')],
        string='Hang en sluit werk:')
    color_rubber = fields.Selection(
        [('Zwart', 'Zwart'), ('Wit', 'Wit'), ('Bruin', 'Bruin')],
        string='Kleur rubber:')
    finishing_types = fields.Selection(
        [('Primer', 'Primer'), ('Primer en aflakken', 'Primer en aflakken'), ('Transparent', 'Transparent'),
         ('Stain en transparent', 'Stain en transparent'), ('Onbehandeld', 'Onbehandeld'), ('Combinatie', 'Combinatie')],
        string='Type afwerking:')

    def print_extra_line(self):
        return 700 * '_'