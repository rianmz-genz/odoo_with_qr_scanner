from odoo import api, fields, models

class InheritAccountJournal(models.Model):
    _inherit = 'account.journal'

    my_account_id = fields.Many2one(
        string='Account',
        comodel_name='account.account',
    )

    