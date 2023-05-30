# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
        string="Data do pedido",
        required=True
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
    
    def aberto(self):
        self.order_status = 'aberto'

    def processo(self):
        if not self.produtos_ids:
            raise ValidationError('Para processar o pedido, precisa de um produto')
        
        for produto in self.produtos_ids:
            if produto.quanty_available == 0:
                raise ValidationError(f'Produto {produto.product_name.name} está sem estoque')
        
        self.order_status = 'processo'

    def concluido(self):
        self.order_status = 'concluido'
    
    def cancelado(self):
        self.order_status = 'cancelado'