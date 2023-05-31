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
    
    def abrir_pedido(self):
        for record in self:
            if record.order_status == 'concluido' or record.order_status == 'cancelado':
                raise ValidationError('Um pedido já concluido ou cancelado não pode ser aberto novamente')
            record.order_status = 'aberto'

    def processar_pedido(self):
        for record in self:
            if record.order_status != 'aberto':
                raise ValidationError('Um pedido apenas pode ser processado se estiver aberto')

            if not record.produtos_ids:
                raise ValidationError('Para processar o pedido, precisa de um produto')
            
            for produto in record.produtos_ids:
                if produto.quanty_available == 0:
                    raise ValidationError(f'Produto {produto.product_name.name} está sem estoque')
            
            record.order_status = 'processo'

    def concluir_pedido(self):
        for record in self:
            if record.order_status != 'processo':
                raise ValidationError('Um pedido apenas pode ser concluido após ser processado')
            
            for produto in record.produtos_ids:
                product_estoque = self.env['pedidos.estoque'].browse(produto.product_name.id)
                product_estoque.write({'quanty_available':product_estoque.quanty_available - 1})
            record.order_status = 'concluido'
    
    def cancelar_pedido(self):
        for record in self:
            record.order_status = 'cancelado'