# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class TaskInherit(models.Model):
    _inherit = "project.task"

    order_type_explanation = fields.Char(string="Type order (Toelichting)")
    levering_explanation = fields.Char(string="Levering (Toelichting)")
    finish_ral = fields.Char(string="Afwerking (RAL)")
    particularities = fields.Char(string="Particularities")
    order_type = fields.Selection(
        [('measure', 'Measure'), ('size', 'Size Appointment'), ('combination', 'Combination')],
        string='Type order')
    project_type = fields.Selection(
        [('renovation', 'Renovation'), ('new_construction', 'New Construction')],
        string='Type project')
    levering_type = fields.Selection(
        [('installation', 'Installation'), ('deliver', 'Deliver'), ('deduct', 'Deduct'),
         ('combination', 'Combination')],
        string='Levering Type')
    hinge_locks = fields.Selection(
        [('and_sure', 'And - Sure'), ('no_customer', 'No - Customer'), ('combination', 'Combination')],
        string='Hang en sluit werk')
    color_rubber = fields.Selection(
        [('black', 'Black'), ('white', 'White'), ('brown', 'Brown')],
        string='Kleur rubber')
    finishing_type = fields.Selection(
        [('primer', 'primer'), ('priming_varnishing', 'Priming and Varnishing'), ('transparent', 'Transparent'),
         ('stain_transparent', 'Stain and Transparent'), ('untreated', 'Untreated'), ('combination', 'Combination')],
        string='Type afwerking')

    def print_extra_line(self):
        return 700 * '_'