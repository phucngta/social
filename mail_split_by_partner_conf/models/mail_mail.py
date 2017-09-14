# -*- coding: utf-8 -*-
# © 2017 Phuc.nt
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from email.utils import formataddr

from odoo import models, fields, api


class MailMail(models.Model):
    _inherit = 'mail.mail'

    # The number of mail is created to notify followers
    mail_count = fields.Integer(
        string='Number of mails')

    split_mail_by_recipients = fields.Selection([
        ('split', 'One mail for each recipient'),
        ('merge', 'One mail for all recipients'),
        ('default', 'Project Default')],
        string='Split mail by recipient partner',
        default='default',
        help='',
    )

    @api.multi
    def send_get_mail_to(self, partner=None):
        # format address if partner is a list
        if len(partner) > 1:
            email_to = [formataddr((p.name, p.email)) for p in partner]
        else:
            email_to = super(MailMail, self).send_get_mail_to(partner=partner)
        return email_to

    @api.multi
    def send_get_email_dict(self, partner=None):
        # check option merge or split recipients
        res = super(MailMail, self).send_get_email_dict(partner=partner)

        default = self.env['ir.config_parameter'].get_param(
            'default_mail_split_by_partner_conf')
        if self.split_mail_by_recipients == 'default' and \
                        default == 'split' or \
                        self.split_mail_by_recipients == 'split':
            self.mail_count += 1
        else:
            if self.email_to or partner == self.recipient_ids[0]:
                self.mail_count += 1
                res.update({
                    'email_to': self.send_get_mail_to(
                        partner=self.recipient_ids),
                })

        return res
