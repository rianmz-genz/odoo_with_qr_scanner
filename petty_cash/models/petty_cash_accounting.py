from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger("*___INI LAGI TESTING___*")

class PettyCashAccounting(models.Model):
    _name = "petty_cash.accounting"
    _description = "Accounting Kas Kecil"
    _rec_name = "id"

    tanggal_transaksi = fields.Date(string='Tanggal Pencatatan', required=True)
    
    journal_id = fields.Many2one(
        string='Account',
        comodel_name='account.account',
    )
    
    debit_cumulated = fields.Float(string='Debit', compute='_compute_debit_cumulated')
    kredit_cumulated = fields.Float(string='Kredit', compute='_compute_kredit_cumulated')
    balance = fields.Float(string='Balance', compute='_compute_balance')

    debit_sum = fields.Float(string='Debit Total', compute='_compute_debit_sum')
    kredit_sum = fields.Float(string='Kredit Total', compute='_compute_kredit_sum')
    balance_sum = fields.Float(string='Balance Total', compute='_compute_balance_sum')

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Person In Charge",
        default=lambda self: self.env.user.id,
        readonly=True
        )

    account_move_id = fields.Many2one(comodel_name='account.move', string='Account Move ID')

    def _compute_debit_cumulated(self):
        for record in self:
            total = 0.0
            for line in record.kas_line_ids:
                total += line.debit
            
            record.debit_cumulated = total

    def _compute_kredit_cumulated(self):
        for record in self:
            total = 0.0
            for line in record.kas_line_ids:
                total += line.kredit
            
            record.kredit_cumulated = total

    def _compute_balance(self):
        for record in self:
            record.balance = record.debit_cumulated - record.kredit_cumulated

    def _compute_debit_sum(self):
        for record in self:
            total = 0.0
            total += record.debit_cumulated
            
            record.debit_sum = total

    def _compute_kredit_sum(self):
        for record in self:
            total = 0.0
            total += record.kredit_cumulated
            
            record.kredit_sum = total

    def _compute_balance_sum(self):
        for record in self:
            total = 0.0
            total += record.balance
            
            record.balance_sum = total


    # FIELD BUKTI CATATAN KAS
    upload_nota_transaksi_keterangan = fields.Text(string='Upload Nota Transaksi Keterangan')
    image_ids = fields.One2many('petty_cash.image_upload', 'petty_doc_id', string='Images')

    # FIELD KAS LINE ID
    kas_line_ids = fields.One2many('petty_cash.kas_line', 'petty_accounting_id', string='Kas Line')
    
    # def process_journal_entry(self, petty_cash_move):
    #     _logger.info(f"Processing Journal Entry {petty_cash_move.name}")


    # def getMethod():
    #     env = api.Environment(context={'discard_cache': True})  # Ensure latest value
    #     petty_cash_method = env['res.config.settings'].get_values().get('petty_cash_method')
    #     return petty_cash_method

    # _logger.info(f"INI BG {getMethod()}")

    

    
    @api.model
    def create(self, vals):
        # GET METODE KAS KECIL
        method = self.env['ir.config_parameter'].sudo().search([
            ('key', '=', 'petty_cash.petty_cash_method'),
        ], limit=1)
        # _logger.info(f"YG INI {method.value}")

        # CHECK OVERALL BALANCE
        line = self.env['petty_cash.accounting'].sudo().search([])
        balance_total = []
        for i in line:
            balance_total.append(i.balance)
        
        
        # Create new petty cash accounting record
        record = super(PettyCashAccounting, self).create(vals)

        # Search for existing account.move with matching date
        existing_move = self.env['account.move'].sudo().search([
            ('date', '=', record.tanggal_transaksi),
            ('journal_id.code', '=', 'PCF')
        ], limit=1)

        account_id = self.env['account.account'].sudo().search([('code', '=', '11110010')]) # Petty Cash account id
        journal_account_id = self.env['account.journal'].sudo().search([('code', '=', 'PCF')]) # Journal Petty Cash Imprest Method

        # EXECUTE JIKA METODE == FLUCTUATION
        if (method.value == 'fluctuation'): 
            # IF ACCOUNT JOURNAL OF PETTY CASH FLUC DOESNT EXIST, MAKE NEW
            # if (len(journal_account_id) < 1):
            #     journal_account_vals = {
            #         'name': 'PETTY CASH FLUCTUATION',
            #         'type': 'general',
            #         'code': 'PCFF',
            #         'my_account_id': self.env['account.account'].sudo().search([('code', '=', '11110001')]).id

            #     }
            #     journal_account_id = self.env['account.journal'].sudo().create(journal_account_vals)

            # Existing move found, update lines
            if (record.debit_cumulated != 0): # check if this from replenishment or not
                if existing_move:
                    existing_move.write({
                        'line_ids': [(0, 0, {
                            'name': f"Petty Cash {record.tanggal_transaksi}",  # Use name or id for reference
                            'debit': record.debit_cumulated,
                            'account_id': record.journal_id.id,
                        }), (0, 0, {
                            'name': f"Petty Cash {record.tanggal_transaksi}",  # Use name or id for reference
                            'credit': record.debit_cumulated,
                            'account_id': account_id.id,
                        })],
                    })
                else: # No existing move, create new one
                    move_vals = {
                        'date': record.tanggal_transaksi,
                        'journal_id': journal_account_id.id,
                        'line_ids': [(0, 0, {
                            'name': f"Petty Cash {record.tanggal_transaksi}",  # Use name or id for reference
                            'debit': record.debit_cumulated,
                            'account_id': record.journal_id.id,
                        }), (0, 0, {
                            'name': f"Petty Cash {record.tanggal_transaksi}",  # Use name or id for reference
                            'credit': record.debit_cumulated,
                            'account_id': account_id.id,
                        })],
                    }
                    move = self.env['account.move'].sudo().create(move_vals)

                # Optional: Link account move to petty cash record for reference
                record.account_move_id = existing_move.id if existing_move else move.id
                _logger.info(f"DISINI {record.kas_line_ids.kredit}")

        # IF EXPENSE (DEBIT) MORE THAN PETTY CASH (CREDIT) RAISE ERROR
        total = sum(balance_total) + record.debit_cumulated
        if (total <= 0):
            return record
        else:
            raise ValidationError(("The total amount of expense is more than current petty cash. Please replenish your petty cash."))

    # REPLENISH BUTTON FUNCTION FOR IMPREST METHOD
    def replenish_button(self):
        # GET METODE KAS KECIL
        method = self.env['ir.config_parameter'].sudo().search([
            ('key', '=', 'petty_cash.petty_cash_method'),
        ], limit=1)

        
        # Search for existing account.move with current date
        existing_move = self.env['account.move'].sudo().search([
            ('date', '=', fields.Date.today()),
            ('journal_id.code', '=', 'PCI')
        ], limit=1)

        account_id = self.env['account.account'].sudo().search([('code', '=', '11110010')]) # Petty Cash account id
        journal_account_id = self.env['account.journal'].sudo().search([('code', '=', 'PCI')]) # Journal Petty Cash Imprest Method 

        # CHECK IF THE METHOD IS IMPREST OR NOT
        if (method.value == 'imprest'): 
            if (len(journal_account_id) > 0): # CHECK IF THE JOURNAL ACCOUNT FOR IMPREST EXIST
                if existing_move:
                    # Existing move found, update lines
                    for record in self :
                        existing_move.write({
                            'line_ids': [(0, 0, {
                                'name': f"Petty Cash {record.tanggal_transaksi}",  # Use name or id for reference
                                'debit': record.debit_cumulated,
                                'account_id': record.journal_id.id,
                            }), (0, 0, {
                                'name': f"Petty Cash {record.tanggal_transaksi}",  # Use name or id for reference
                                'credit': record.debit_cumulated,
                                'account_id': journal_account_id.my_account_id.id,
                            })],
                        })
                else:
                    # No existing move, create new one
                    # current_date = fields.Date.today()
                    # current_month = str(current_date.month).rjust(2, "0")
                    # current_year = current_date.year
                    # name_id = str(self.id).rjust(4, "0")

                    move_vals = {
                        'date': fields.Date.today(),
                        'journal_id': journal_account_id.id,
                        # 'name': f"{journal_account_id.code}/{current_year}/{current_month}/{name_id}",
                        'line_ids': [],
                    }

                    # Loop through records and append line values
                    for record in self:
                        move_vals['line_ids'].append((0, 0, {
                            'name': f"Petty Cash {record.tanggal_transaksi}",  # Consider using record.name if available
                            'debit': record.debit_cumulated,
                            'account_id': record.journal_id.id,
                        }))
                        move_vals['line_ids'].append((0, 0, {
                            'name': f"Petty Cash {record.tanggal_transaksi}",  # Consider using record.name if available
                            'credit': record.debit_cumulated,
                            'account_id': journal_account_id.my_account_id.id,
                        }))

                    move = self.env['account.move'].sudo().create(move_vals)

                # Optional: Link account move to petty cash record for reference
                self.account_move_id = existing_move.id if existing_move else move.id

                # CREATE NEW RECORD FOR PETTY CASH REPLENISHMENT
                petty_cash_record = {
                    'tanggal_transaksi': fields.Date.today(),
                    'journal_id': account_id.id,
                }
                created_record = self.env['petty_cash.accounting'].sudo().create(petty_cash_record)

                debit_total = 0
                for i in self:
                    debit_total += i.debit_cumulated

                # CREATE NEW LINE INSIDE THE RECORD
                petty_cash_line = {
                    'petty_accounting_id': created_record.id,
                    'desc': f'Pengisian Tanggal {fields.Date.today()}',
                    'debit': 0,
                    'kredit': debit_total
                }
                self.env['petty_cash.kas_line'].sudo().create(petty_cash_line)
                
            else:
                raise ValidationError(("The Journal of Petty Cash Imprest (PCI) doesn't exist. Please do the first step of replenishment"))
        else:
            raise ValidationError(("The method of Petty Cash is not Imprest."))

        
# Ini untuk page Kas Line dengan berisi table
class KasLine(models.Model):
    _name = "petty_cash.kas_line"
    _description = "Kas Line"

    petty_accounting_id = fields.Many2one('petty_cash.accounting', string='Accounting Kas Kecil')
    
    desc = fields.Text(string='Keterangan')
    debit = fields.Float(string='Debit')
    kredit = fields.Float(string='Kredit')

class UploadGambar(models.Model):
    _name = "petty_cash.image_upload"

    image = fields.Binary(string="Image")
    petty_doc_id = fields.Many2one('petty_cash.accounting', string='Images')


