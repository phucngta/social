# -*- coding: utf-8 -*-
from odoo import models, api


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.multi
    def message_get_recipient_values(self, notif_message=None,
                                     recipient_ids=None):
        # merge followers when mail
        res = super(MailThread, self).message_get_recipient_values(
            notif_message=notif_message, recipient_ids=recipient_ids)

        res['recipient_ids'] = [(6, 0, recipient_ids)]
        return res
