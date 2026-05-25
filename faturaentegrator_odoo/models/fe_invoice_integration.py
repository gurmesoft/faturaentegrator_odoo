from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FEInvoiceIntegration(models.Model):
    _name = 'fe.invoice.integration'
    _description = 'Fatura Entegratör Fatura Entegrasyonu'
    _order = 'name, id'

    company_id = fields.Many2one('res.company', required=True, ondelete='cascade', index=True)
    name = fields.Char(required=True)
    external_id = fields.Char(required=True, index=True)

    _sql_constraints = [
        (
            'fe_invoice_integration_company_external_uniq',
            'unique(company_id, external_id)',
            'Bu entegrasyon bu şirket için zaten kayıtlı.',
        ),
    ]

    @api.model
    def _parse_integration_items(self, data):
        items = data.get('data') or data or []
        if isinstance(items, dict):
            items = items.get('items') or []
        return items if isinstance(items, list) else []

    @api.model
    def _integration_item_values(self, item):
        name = (
            item.get('name')
            or item.get('title')
            or (item.get('vendor') and item['vendor'].get('name'))
            or _('Entegrasyon')
        )
        ext_id = item.get('id') or item.get('uuid') or ''
        if not ext_id:
            return None
        return {'name': name, 'external_id': str(ext_id)}

    @api.model
    def sync_for_company(self, company):
        """FE API'den fatura entegrasyonlarını çekip şirket bazında günceller."""
        company.ensure_one()
        if not company.fe_api_key:
            raise UserError(_('Önce Fatura Entegratör API anahtarını kaydedin.'))

        client = company.fe_get_client()
        data = client.integration_invoice_index()
        items = self._parse_integration_items(data)

        Integration = self.sudo()
        existing = Integration.search([('company_id', '=', company.id)])
        seen_external_ids = set()

        for item in items:
            parsed = self._integration_item_values(item)
            if not parsed:
                continue
            seen_external_ids.add(parsed['external_id'])
            record = existing.filtered(lambda r: r.external_id == parsed['external_id'])[:1]
            if record:
                record.write({'name': parsed['name']})
            else:
                Integration.create({
                    'company_id': company.id,
                    'name': parsed['name'],
                    'external_id': parsed['external_id'],
                })

        stale = existing.filtered(lambda r: r.external_id not in seen_external_ids)
        if stale:
            stale.unlink()

        return Integration.search([('company_id', '=', company.id)])

    @api.model
    def default_choice_for_company(self, company):
        """Tek entegrasyon varsa sihirbaz için varsayılan kayıt id'si."""
        integrations = self.search([('company_id', '=', company.id)], order='name, id')
        return integrations.id if len(integrations) == 1 else False
