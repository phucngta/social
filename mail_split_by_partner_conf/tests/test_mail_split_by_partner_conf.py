# -*- coding: utf-8 -*-
# © 2017 Phuc.nt
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMailSplitByPartnerConf(TransactionCase):
    def setUp(self):
        super(TestMailSplitByPartnerConf, self).setUp()
        self.ICP = self.env['ir.config_parameter']
        # self.partner_01 = self.env.ref('base.res_partner_10')
        self.partner_1 = self.env['res.partner'].create({
            'name': 'partner_1',
            'email': 'partner_1@example.com'
        })
        self.partner_2 = self.env['res.partner'].create({
            'name': 'partner_2',
            'email': 'partner_2@example.com'
        })
        self.test_channel = self.env['mail.channel'].create({'name': 'Test'})

    def message_post(self):
        self.message = self.env['mail.message'].create({
            'body': 'My Body',
            'model': 'mail.channel',
            'res_id': self.test_channel.id,
            'partner_ids': [(6, 0, [self.partner_1.id, self.partner_2.id])]
        })
        mails = self.env['mail.mail'].search([
            ('mail_message_id', '=', self.message.id)
        ])
        mails.send()
        return mails

    def test_message_post(self):
        self.ICP.set_param('default_mail_split_by_partner_conf', 'merge')
        mails = self.message_post()
        self.assertEqual(mails.mail_count, 1)

        self.ICP.set_param('default_mail_split_by_partner_conf', 'split')
        mails = self.message_post()
        self.assertEqual(mails.mail_count, len(mails.recipient_ids))
