from odoo import api, models


class FEInvoiceLinkMixin(models.AbstractModel):
    _name = 'fe.invoice.link.mixin'
    _description = 'FE invoice link search helpers'

    @api.model
    def _search_fe_invoice_by_link(self, link_field, operator, value):
        """fe.invoice kaydına göre account.move / sale.order domain üret."""
        if operator == '=?':
            if not value:
                return []
            operator, value = '=', value

        if operator not in ('=', '!=', 'in', 'not in'):
            return NotImplemented

        Invoice = self.env['fe.invoice']

        if operator in ('=', '!=') and not value:
            linked_ids = Invoice.search([(link_field, '!=', False)]).mapped(link_field).ids
            if operator == '=':
                return [('id', 'not in', linked_ids)]
            return [('id', 'in', linked_ids)]

        if operator in ('in', 'not in'):
            invoice_domain = [('id', operator, value or [])]
        else:
            invoice_domain = [('id', '=', value)]

        linked_ids = Invoice.search(invoice_domain).mapped(link_field).ids
        if operator in ('=', 'in'):
            return [('id', 'in', linked_ids)]
        return [('id', 'not in', linked_ids)]
