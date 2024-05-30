from odoo import http, _, exceptions
from odoo.http import request
import logging
_logger = logging.getLogger("*___INI LAGI TESTING___*")
from functools import partial
from attr import fields
import base64
import io
import json
from datetime import datetime
from collections import defaultdict



class pettyCash(http.Controller):
    @http.route('/pettycash/login/', auth='public', methods=["POST"], csrf=False, cors="*", website=False)
    def login(self, **kw):
    # Validation
        try:
            login = kw["login"] 
        except KeyError:
            return request.make_response(json.dumps( {
                    'status': 'failed',
                    'message': '`login` is required.'
                }), headers={'Content-Type': 'application/json'})
        
        try:
            password = kw["password"]
        except KeyError:
            return request.make_response(json.dumps( {
                    'status': 'failed',
                    'message': '`password` is required.'
                }), headers={'Content-Type': 'application/json'})
        try:
            db = kw["db"]
            
        except KeyError:
            return request.make_response(json.dumps( {
                    'status': 'failed',
                    'message': '`db` is required.'
                }), headers={'Content-Type': 'application/json'})
        # Auth user
        http.request.session.authenticate(db, login, password)
        # Session info
        res = request.env['ir.http'].session_info()
        return request.make_response(json.dumps(res), headers={'Content-Type': 'application/json'})


    @http.route('/pettycash/list', auth='user', methods=["GET"], csrf=False, cors="*", website=False)
    def getList(self, **kw):
        # 1. Validasi & Operasi
        Pettycash = request.env['petty_cash.accounting'].sudo()

        existingKas = Pettycash.search([])

        if not existingKas:
            return request.make_response(json.dumps({
                'status': 'failed',
                # 'data': 'Tidak ada data',
            }), headers={'Content-Type': 'application/json'})

        # 2. Sum debit_sum for each unique month and year combination
        month_year_sums = defaultdict(float)

        res = []
        for kas in existingKas:
            month_year = kas.tanggal_transaksi.strftime('%Y-%m')
            month_year_sums[month_year] += kas.debit_sum

        # 3. Convert aggregated sums to response format
        for month_year, debit_sum in month_year_sums.items():
            res.append({
                'tanggal_transaksi': f"{month_year}",  # Using the first day of the month for representation
                'debit_sum': debit_sum,
            })

        # 4. Return
        return request.make_response(json.dumps({
            'status': 'success',
            'data': res
        }), headers={'Content-Type': 'application/json'})



    @http.route('/pettycash/list/top-expense', auth='user', methods=["GET"], csrf=False, cors="*", website=False)
    def getListTopExpense(self, **kw):
        # 1. Validasi & Operasi
        Pettycash = request.env['petty_cash.accounting'].sudo()
        
        existingKas = Pettycash.search([
        ])

        if (len(existingKas) < 1):
            return request.make_response(json.dumps( {
                'status': 'failed',
                'data': None,
            }), headers={'Content-Type': 'application/json'})

        grouped_data = {}

        for line in existingKas:
            key = line.journal_id.id
            if key not in grouped_data:
                grouped_data[key] = {
                'journal_id': f"{line.journal_id.code} {line.journal_id.name}",
                'debit_sum': 0
                }

            grouped_data[key]['debit_sum'] += line.debit_sum

        

        # 2. Return
        return request.make_response(json.dumps( {
            'status': 'success',
            'data': grouped_data
        }), headers={'Content-Type': 'application/json'})


    @http.route('/pettycash/list/top-user-expense', auth='user', methods=["GET"], csrf=False, cors="*", website=False)
    def getListTopUserExpense(self, **kw):
        # 1. Validasi & Operasi
        Pettycash = request.env['petty_cash.accounting'].sudo()
        
        existingKas = Pettycash.search([
        ])

        if (len(existingKas) < 1):
            return request.make_response(json.dumps( {
                'status': 'failed',
                'data': None,
            }), headers={'Content-Type': 'application/json'})

        grouped_data = {}

        for line in existingKas:
            key = line.user_id.id
            if key not in grouped_data:
                grouped_data[key] = {
                'user_id': f"{line.user_id.name}",
                'debit_sum': 0
                }

            grouped_data[key]['debit_sum'] += line.debit_sum

        # 2. Return
        return request.make_response(json.dumps( {
            'status': 'success',
            'data': grouped_data
        }), headers={'Content-Type': 'application/json'})

            


