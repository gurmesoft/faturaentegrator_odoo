from odoo import api, models

# ISO 3166-1 alpha-2 -> Fatura Entegratör / GIB ülke adı (WordPress eklentisi ile uyumlu)
FE_COUNTRY_NAME_BY_CODE = {
    'TR': 'Türkiye',
    'CY': 'Kıbrıs',
    'DE': 'Almanya',
    'GB': 'Birleşik Krallık',
    'US': 'Amerika Birleşik Devletleri',
    'FR': 'Fransa',
    'NL': 'Hollanda',
    'IT': 'İtalya',
    'ES': 'İspanya',
    'AZ': 'Azerbaycan',
    'GE': 'Gürcistan',
    'IQ': 'Irak',
    'IR': 'İran',
    'SY': 'Suriye',
    'GR': 'Yunanistan',
    'BG': 'Bulgaristan',
    'RO': 'Romanya',
    'RU': 'Rusya Federasyonu',
    'UA': 'Ukrayna',
    'SA': 'Suudi Arabistan',
    'AE': 'Birleşik Arap Emirlikleri',
}


class FECountryMapper(models.AbstractModel):
    _name = 'fe.country.mapper'
    _description = 'Fatura Entegratör Ülke Eşleme'

    @api.model
    def map_country_name(self, country):
        """res.country veya ISO kodunu FE API ülke adına çevir."""
        if not country:
            return FE_COUNTRY_NAME_BY_CODE['TR']
        if isinstance(country, str):
            code = country.strip().upper()
            if code in FE_COUNTRY_NAME_BY_CODE:
                return FE_COUNTRY_NAME_BY_CODE[code]
            country_rec = self.env['res.country'].search([('code', '=', code)], limit=1)
            if country_rec:
                country = country_rec
            else:
                return country.strip()
        code = (country.code or '').upper()
        if code in FE_COUNTRY_NAME_BY_CODE:
            return FE_COUNTRY_NAME_BY_CODE[code]
        name_tr = country.with_context(lang='tr_TR').name
        return name_tr or country.name or FE_COUNTRY_NAME_BY_CODE['TR']

    @api.model
    def map_partner_country(self, partner):
        return self.map_country_name(partner.country_id if partner else None)
