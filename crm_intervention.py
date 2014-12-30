# -*- coding: utf-8 -*-
##############################################################################
#
#    crm_intervention_timesheet module for OpenERP, CRM Intervention Timesheet
#    Copyright (C) 2011 SYLEAM Info Services (<http://www.Syleam.fr/>)
#              Sebastien LANGE <sebastien.lange@syleam.fr>
#
#    This file is a part of crm_intervention_timesheet
#
#    crm_intervention_timesheet is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    crm_intervention_timesheet is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, fields


class crm_intervention(models.Model):
    _inherit = 'crm.intervention'
    _name = "crm.intervention"

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', ondelete='cascade', default='get_default_analytic')
    timesheet_ids = fields.One2many('hr.analytic.timesheet', 'intervention_id', 'Timesheet')

    @api.one
    def get_default_analytic(self):
        """
        Gives id of analytic for this case
        """
        return self.env['crm.analytic.timesheet.configuration'].search([('model', '=', self._name)]).analytic_account_id.id

    def onchange_partner_intervention_id(self):
        if not self.partner_id:
            self.partner_invoice_id = False
            self.partner_shipping_id = False
            self.partner_order_id = False
            self.email_from = False
            self.partner_address_phone = False
            self.partner_address_mobile = False
            self.analytic_account_id = False

        address_obj = self.pool.get('res.partner.address')
        addr = self.partner_id.address_get(['default', 'delivery', 'invoice', 'contact'])

        self.partner_invoice_id = addr['invoice']
        self.partner_order_id = addr['contact']
        self.partner_shipping_id = addr['delivery']
        self.email_from = address_obj.browse(addr['delivery']).email
        self.partner_address_phone = address_obj.browse(addr['delivery']).phone
        self.partner_address_mobile = address_obj.browse(addr['delivery']).mobile

        for timesheet in self.partner_id.crm_analytic_ids:
            if timesheet.crm_model_id.model == self._name:
                self.analytic_account_id = timesheet.analytic_account_id.id

crm_intervention()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
