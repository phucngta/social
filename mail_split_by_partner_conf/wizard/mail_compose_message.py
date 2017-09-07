# -*- coding: utf-8 -*-
from odoo import models, api


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        # TODO - is need check case fields is none
        if fields is not None:
            fields.append('split_mail_by_recipients')

        return super(MailComposer, self).generate_email_for_composer(
            template_id, res_ids, fields=fields)

    @api.multi
    def get_mail_values(self, res_ids):
        res = super(MailComposer, self).get_mail_values(res_ids)
        recipient_ids = []
        if self.composition_mode == 'mass_mail' and \
                        res[res_ids[0]]['split_mail_by_recipients'] == 'merge':
            result = {}
            for res_id in res_ids:
                recipient_ids += [int(i[1]) for i in
                                  res[res_id]['recipient_ids']]

            res[res_ids[0]]['recipient_ids'] = [(6, 0, recipient_ids)]
            result[res_ids[0]] = res[res_ids[0]]
            return result

        return res
