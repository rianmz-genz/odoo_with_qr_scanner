# -*- coding: utf-8 -*-
# from odoo import http


# class Exampleowl(http.Controller):
#     @http.route('/exampleowl/exampleowl', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exampleowl/exampleowl/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('exampleowl.listing', {
#             'root': '/exampleowl/exampleowl',
#             'objects': http.request.env['exampleowl.exampleowl'].search([]),
#         })

#     @http.route('/exampleowl/exampleowl/objects/<model("exampleowl.exampleowl"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exampleowl.object', {
#             'object': obj
#         })
