# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Produto(models.Model):
    _name = 'pedidos.produto'
    _description = 'Produto'

    product_name = fields.Many2one(
        comodel_name="pedidos.estoque",
        string="Nome do produto"
    )

    description = fields.Text(
        related="product_name.description",
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
        related="product_name.unit_price",
        string="Preço Unitário"
    )

    quanty_available = fields.Integer(
        related="product_name.quanty_available",
        string="Quantidade Disponivel"
    )

    pedido_id = fields.Many2one(
        comodel_name='pedidos.pedido',
        string="Pedido",
        readonly=True
    )