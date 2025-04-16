from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange('account_id')
    def _inverse_account_id(self):
        for record in self:
            if isinstance(record.id, models.NewId):
                _logger.info("Operando en registro no guardado")
                return
            self._inverse_analytic_distribution()
            self._conditional_add_to_compute('tax_ids', lambda line: (
                line.account_id.tax_ids
                and not line.product_id.taxes_id.filtered(lambda tax: tax.company_id == line.company_id)
            ))