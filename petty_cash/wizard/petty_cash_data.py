from odoo import models, fields, api
import logging
_logger = logging.getLogger("*___INI LAGI TESTING___*")

class ReportPettyCashData(models.TransientModel):
    _name = "petty_cash.data"

    date_from =  fields.Date(string='Start Date', required=True)
    date_to =  fields.Date(string='End Date', required=True)

    def _get_data(self):
        petty_cash = self.env['petty_cash.accounting'].sudo().search([])

        if self.date_from and self.date_to:
            petty_cash_report = petty_cash.filtered(lambda x: x.tanggal_transaksi >= self.date_from and x.tanggal_transaksi <= self.date_to)
            
        result = []
        debit_sum = 0.0
        kredit_sum = 0.0
        balance_sum = 0.0

        # Group data by tanggal_transaksi
        grouped_data = {}
        for line in petty_cash_report:
            key = line.tanggal_transaksi
            if key not in grouped_data:
                grouped_data[key] = {
                    'tanggal_transaksi': line.tanggal_transaksi,
                    'journal_id': {
                        'code':[],
                        'name':[]
                    },
                    'debit': [],
                    'kredit': [],
                    'balance': [],
                    'total': [0,0,0],
                }

            # Append values from kas_line_ids
            first_balance = True
            for kas_line in line.kas_line_ids:
                grouped_data[key]['journal_id']['code'].append(kas_line.petty_accounting_id.journal_id.code)
                grouped_data[key]['journal_id']['name'].append(kas_line.petty_accounting_id.journal_id.name)
                grouped_data[key]['debit'].append(kas_line.debit)
                grouped_data[key]['kredit'].append(kas_line.kredit)
                if first_balance:
                    grouped_data[key]['balance'].append(kas_line.petty_accounting_id.balance)
                    first_balance = False
                else:
                    grouped_data[key]['balance'].append(0)

            # for index, (key, values) in enumerate(grouped_data.items()):
            #     if(index == len(grouped_data)-1):
            #         debit_sum = sum(values['debit'])
            #         kredit_sum = sum(values['kredit'])
            #         _logger.info(f"debit_sum {debit_sum}")
            #         _logger.info(f"kredit_sum {kredit_sum}")


        for v in grouped_data.values():
            for d in v['debit']:
                debit_sum += d
            
            for k in v['kredit']:
                kredit_sum += k
            
            for b in v['balance']:
                balance_sum += b

            grouped_data[key]['total'][0] = debit_sum
            grouped_data[key]['total'][1] = kredit_sum
            grouped_data[key]['total'][2] = balance_sum
        _logger.info(f"GROUPED DATA {grouped_data}")

        # Convert grouped data to result format
        for key, values in grouped_data.items():
            res = {
                'tanggal_transaksi': values['tanggal_transaksi'],
                'journal_id': values['journal_id'],
                'debit': values['debit'],
                'kredit': values['kredit'],
                'balance': values['balance'],
                'total': values['total'],
            }
            result.append(res)

        datas = {
            'ids': self.ids,
            'model': 'petty_cash.data',
            'form': result,
            'start_date': self.date_from,
            'end_date': self.date_to,
        }

        return datas


    def get_report(self):
        datas = self._get_data()
        return self.env.ref('petty_cash.report_petty_cash').report_action(self, data=datas)
