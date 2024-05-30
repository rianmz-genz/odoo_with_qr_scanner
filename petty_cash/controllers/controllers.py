# -*- coding: utf-8 -*-
# from odoo import http


# class KasKecil(http.Controller):
#     @http.route('/kas_kecil/kas_kecil/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kas_kecil/kas_kecil/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kas_kecil.listing', {
#             'root': '/kas_kecil/kas_kecil',
#             'objects': http.request.env['kas_kecil.kas_kecil'].search([]),
#         })

#     @http.route('/kas_kecil/kas_kecil/objects/<model("kas_kecil.kas_kecil"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kas_kecil.object', {
#             'object': obj
#         })
