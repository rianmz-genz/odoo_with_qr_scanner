# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    petty_cash_method = fields.Selection([
        ('imprest', 'Imprest'),
        ('fluctuation', 'Fluctuation'),
    ], string='Method', default='imprest', config_parameter='petty_cash.petty_cash_method')

