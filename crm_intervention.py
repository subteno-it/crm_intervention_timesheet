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

from osv import osv
from osv import fields
from crm_timesheet import crm_operators


class crm_intervention(osv.osv):
    _inherit = 'crm.intervention'
    _name = "crm.intervention"

    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', ondelete='cascade', ),
        'timesheet_ids': fields.one2many('crm.analytic.timesheet', 'res_id', 'Messages', domain=[('model', '=', _name)]),
        'duration_timesheet': fields.function(crm_operators.duration_calc, method=True, string='Hours spend',
            store={
                'crm.intervention': (lambda self, cr, uid, ids, c={}: ids, ['timesheet_ids'], 10),
                'crm.analytic.timesheet': (crm_operators.get_crm, ['hours', 'analytic_account_id'], 10),
            },)
    }

    _defaults = {
         'analytic_account_id': crm_operators.get_default_analytic,
    }

    def onchange_partner_intervention_id(self, cr, uid, ids, part):
        if not part:
            return {'value': {'partner_invoice_id': False,
                             'partner_shipping_id': False,
                             'partner_order_id': False,
                             'email_from': False,
                             'partner_address_phone': False,
                             'partner_address_mobile': False,
                             'analytic_account_id': False,
                            }}
        partner_obj = self.pool.get('res.partner')
        address_obj = self.pool.get('res.partner.address')
        addr = partner_obj.address_get(cr, uid, [part], ['default', 'delivery', 'invoice', 'contact'])
        part = partner_obj.browse(cr, uid, part)
        val = {'partner_invoice_id': addr['invoice'],
               'partner_order_id': addr['contact'],
               'partner_shipping_id': addr['delivery'],
              }
        val['email_from'] = address_obj.browse(cr, uid, addr['delivery']).email
        val['partner_address_phone'] = address_obj.browse(cr, uid, addr['delivery']).phone
        val['partner_address_mobile'] = address_obj.browse(cr, uid, addr['delivery']).mobile
        for timesheet in part.crm_analytic_ids:
            if timesheet.crm_model_id.model == self._name:
                val['analytic_account_id'] = timesheet.analytic_account_id.id
        return {'value': val}

    def create(self, cr, uid, values, context=None):
        """
        Add model in context for crm_analytic_timesheet object
        """
        if context is None:
            context = {}
        # Add model for crm_timesheet
        context['model'] = self._name
        return super(crm_intervention, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        """
        Add model in context for crm_analytic_timesheet object
        """
        if context is None:
            context = {}
        # Add model for crm_timesheet
        context['model'] = self._name
        return super(crm_intervention, self).write(cr, uid, ids, values, context=context)

crm_intervention()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
