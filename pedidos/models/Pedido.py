# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Pedido(models.Model):
    _name = 'pedidos.pedido'
    _description = 'Pedido'

    name = fields.Char(
        string="Número do Pedido",
        readonly=True
    )

    client_name = fields.Char(
        string="Nome do cliente",
        required=True
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

    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('seq.pedido')
        return super(Pedido, self).create(values)