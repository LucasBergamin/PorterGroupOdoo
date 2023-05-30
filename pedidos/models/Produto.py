# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Produto(models.Model):
    _name = 'pedidos.produto'
    _description = 'Produto'

    product_name = fields.Char(
        string="Nome do produto"
    )

    description = fields.Text(
        string="Descrição"
    )

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)

    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)

    unit_price = fields.Monetary(
        string="Preço Unitário"
    )