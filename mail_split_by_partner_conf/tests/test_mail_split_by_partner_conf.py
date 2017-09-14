# -*- coding: utf-8 -*-
# © 2017 Phuc.nt
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMailSplitByPartnerConf(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestMailSplitByPartnerConf, self).setUp(*args, **kwargs)
        self.ICP = self.env['ir.config_parameter']
        # self.partner_01 = self.env.ref('base.res_partner_10')
        self.partner_01 = self.env['res.partner'].create({
            'name': 'partner_1',
            'email': 'partner_1@example.com'
        })
        self.partner_02 = self.env['res.partner'].create({
            'name': 'partner_2',
            'email': 'partner_2@example.com'
        })

        # self.partner_02 = self.env.ref('base.res_partner_12')
        # self.partner_03 = self.env.ref('base.res_partner_18')

        self.test_channel = self.env['mail.channel'].create({'name': 'Test'})
        self.follower1 = self.env['mail.followers'].create({
            'res_model': 'mail.channel',
            'res_id': self.test_channel.id,
            'partner_id': self.partner_01.id,
            # 'partner_id': self.user_employee.partner_id.id,
        })
        self.follower2 = self.env['mail.followers'].create({
            'res_model': 'mail.channel',
            'res_id': self.test_channel.id,
            'partner_id': self.partner_02.id,
        })
        # self.follower3 = self.env['mail.followers'].create({
        #     'res_model': 'mail.channel',
        #     'res_id': self.test_channel.id,
        #     'partner_id': self.partner_03.id,
        # })

    def message_post(self):
        self.message = self.env['mail.message'].create({
            'body': 'My Body',
            'model': 'mail.channel',
            'res_id': self.test_channel.id,
        })
        self.mail = self.env['mail.mail'].search([
            ('mail_message_id', '=', self.message.id)
        ])

    def test_message_post(self):
        self.ICP.set_param('default_mail_split_by_partner_conf', 'merge')
        self.message_post()
        self.assertEqual(len(self.mail.mail_count), 1)
        self.ICP.set_param('default_mail_split_by_partner_conf', 'split')
        self.message_post()
        self.assertEqual(len(self.mail.mail_count),
                         len(self.mail.recipient_ids))
