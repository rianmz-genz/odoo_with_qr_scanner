from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger("*___INI LAGI TESTING___*")

class PettyCashReplenishment(models.TransientModel):
    _name = "petty_cash.replenishment"

    date =  fields.Date(string='Date', required=True)
    amount =  fields.Float(string='Amount', required=True)
    
    @api.model
    def _add_data(self):
        AccountJournal = self.env['account.journal'].sudo()
        try:
            account_id = self.env['account.account'].sudo().search([('code', '=', '11110010')]) # Petty Cash account id
            journal_imprest_id = AccountJournal.search([('code', '=', 'PCI')], limit=1) # Journal Petty Cash Imprest Method
            journal_fluc_id = AccountJournal.search([('code', '=', 'PCF')], limit=1) # Journal Petty Cash Fluctuation Method
            journal_account_id = []
            _logger.info(f"YG INI {journal_fluc_id}")
            # raise ValidationError("coba")
            # CHECK METHOD OF PETTY CASH
            method = self.env['ir.config_parameter'].sudo().search([
                ('key', '=', 'petty_cash.petty_cash_method'),
            ], limit=1)

            if (len(method) < 1):
                raise ValidationError(("Go to setting and choose the method of petty cash and then click SAVE"))

            # CREATE NEW RECORD FOR PETTY CASH REPLENISHMENT
            petty_cash_record = {
                'tanggal_transaksi': self.date,
                'journal_id': account_id.id,
            }
            created_record = self.env['petty_cash.accounting'].sudo().create(petty_cash_record)

            # CREATE NEW LINE INSIDE THE RECORD
            petty_cash_line = {
                'petty_accounting_id': created_record.id,
                'desc': f'Pengisian Tanggal {self.date}',
                'debit': 0,
                'kredit': self.amount
            }
            self.env['petty_cash.kas_line'].sudo().create(petty_cash_line)

            # CHECKING METHOD IMPREST OR FLUCTUATION
            if (method.value == 'imprest'):
                journal_account_id = journal_imprest_id
                # CREATE NEW JOURNAL ACCOUNT IF ! JOURNAL PETTY CASH IMPREST(PCI)
                if not journal_account_id:
                    journal_account_vals = {
                        'name': 'PETTY CASH IMPREST',
                        'type': 'general',
                        'code': 'PCI',
                        'my_account_id': self.env['account.account'].sudo().search([('code', '=', '11110001')]).id

                    }
                    journal_account_id = AccountJournal.create(journal_account_vals)
            else:
                journal_account_id = journal_fluc_id
                # CREATE NEW JOURNAL ACCOUNT IF ! JOURNAL PETTY CASH FLUCTUATION(PCF)
                if not journal_account_id:

                    journal_account_vals = {
                        'name': 'PETTY CASH FLUCTUATION',
                        'type': 'general',
                        'code': 'PCF',
                        'my_account_id': self.env['account.account'].sudo().search([('code', '=', '11110001')]).id
                    }
                    journal_account_id = AccountJournal.create(journal_account_vals)
                

            # CREATE ACCOUNT MOVE RECORD FOR REPLENISHMENT
            move_vals = {
                    'date': self.date,
                    'journal_id': journal_account_id.id,
                    'line_ids': [(0, 0, {
                        'name': f"Petty Cash {self.date}",  # Use name or id for reference
                        'debit': self.amount,
                        'account_id': account_id.id,
                        'analytic_account_id': False,
                    }), (0, 0, {
                        'name': f"Petty Cash {self.date}",  # Use name or id for reference
                        'credit': self.amount,
                        'account_id': journal_account_id.my_account_id.id,
                        'analytic_account_id': False,
                    })],
                }
            move = self.env['account.move'].sudo().create(move_vals)

            # Link account move to petty cash record for reference
            created_record.account_move_id = move.id
        except Exception as e:
            raise ValidationError(f"ini erorrnyaa {e}")
        

    def add_data(self):
        datas = self._add_data()
        return datas
