from odoo import api, fields, models

class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    @api.model_create_multi
    def create(self, vals_list):
        moves = super(InheritAccountMove, self).create(vals_list)

        # Filter out only moves related to the petty cash account
        petty_cash_moves = moves.filtered(lambda move: move.line_ids.filtered(lambda line: line.account_id.code == '11110010'))

        # Trigger an event for each petty cash move
        for petty_cash_move in petty_cash_moves:
            self.env['petty_cash.accounting'].sudo().process_journal_entry(petty_cash_move)

        return moves