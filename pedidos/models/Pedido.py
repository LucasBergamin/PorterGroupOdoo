# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Pedido(models.Model):
    _name = 'pedidos.pedido'
    _description = 'Pedido'

    client_name = fields.Char(
        string="Nome do cliente"
    )

    order_date = fields.Date(
        string="Data do pedido"
    )

    order_status = fields.Selection(
        selection=[
            ('aberto','Aberto'),
            ('processo', 'Em Processo'),
            ('concluido', 'Concluido'),
            ('cancelado', 'Cancelado')
        ],
        default="aberto",
        string="Status do Pedido"
    )

    produtos_ids = fields.One2many(
        comodel_name="pedidos.produto",
        inverse_name="pedido_id",
        string="Produtos"
    )