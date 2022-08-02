# -*- coding: utf-8 -*-
import mysql.connector
from odoo import fields, models


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    is_diva_customer = fields.Char(string='Is Diva customer?')
    dt_user_id = fields.Char(string='DropTaxi User Id')
    dt_referral_code = fields.Char(string='Referral Code')
    dt_gender = fields.Char(string='Gender')
    dt_completed_rides = fields.Char(string='Completed Rides')
    dt_cancelled_rides = fields.Char(string='Cancelled Rides')
    dt_referral_discounts_count = fields.Char(string='Referral Discount Count')
    dt_referral_count = fields.Char(string='Referral Count')
    dt_login_count = fields.Char(string='Login Count')
    dt_user_rating = fields.Char(string='User Rating')
    dt_country_dial_code = fields.Char(string='Country Dial Code')
    dt_account_type = fields.Selection([
        ('1', 'Passenger'),
        ('2', 'Dispatcher'),
        ('3', 'Admin'),
        ('4', 'franchise'),
        ('5', 'Biller'),
    ], tracking=True)
    # Token & Password
    dt_push_notification_token = fields.Char(string='Push Notification Token')
    dt_password_hash = fields.Char(string='Hashed Password', help='users password in salted and hashed format')
    dt_pwd_raw = fields.Char(string='Raw Password', help="User's raw password")

    # amount
    dt_wallet_amount = fields.Float(string="Wallet Amount")
    dt_reward_points_redeemed = fields.Float(string="Reward Points Redeemed")
    dt_reward_points = fields.Float(string="Reward Points")

    def cron_customer_data(self):
        connectors = self.env['diva.transport'].search([])
        for connector in connectors:
            try:
                con = mysql.connector.connect(
                    host=connector.mysql_host,
                    user=connector.mysql_user,
                    port=connector.mysql_port,
                    password=connector.mysql_password,
                    database=connector.mysql_database)
                # create cursor object
                cursor = con.cursor(dictionary=True)
                self.sync_customer_data(cursor)
            except Exception as ex:
                print(
                    f"Problem with Mysql Database!\n{ex}\nIt is certainly a problem of Internet connexion. PhoneBot "
                    f"will retry to run in 15 seconds.")

    def sync_customer_data(self, cursor):
        # assign data query
        query1 = "select * from cab_tbl_users"

        # executing cursor
        cursor.execute(query1)

        # display all records
        customer_records = cursor.fetchall()
        # describe table
        for record in customer_records:
            # mapped country
            country_id = False
            if record.get('country_code'):
                country_id = self.env['res.country'].search([('code', '=', record.get('country_code'))])

            # mapped language
            lang_id = False
            if record.get('disp_lang'):
                lang_id = self.env['res.lang'].search([('iso_code', '=', record.get('disp_lang'))])

            # customer dict
            customer_dict = {
                'is_diva_customer': True,
                'dt_user_id': record.get('user_id', ''),
                'name': record.get('firstname', '') + record.get('lastname', ''),
                'street': record.get('address', ''),
                'email': record.get('email', ''),
                'lang': lang_id.code if lang_id else '',
                'country_id': country_id and country_id.id or False,
                'dt_gender': record.get('sex', ''),
                'dt_account_type': str(record.get('account_type')),
                'dt_country_dial_code': record.get('country_dial_code', ''),
                'dt_cancelled_rides': record.get('cancelled_rides', ''),
                'dt_completed_rides': record.get('completed_rides', ''),
                'dt_referral_code': record.get('referal_code', ''),
                'dt_user_rating': record.get('user_rating', ''),
                'dt_push_notification_token': record.get('push_notification_token', ''),
                'dt_referral_discounts_count': record.get('referral_discounts_count', ''),
                'dt_referral_count': record.get('referral_count', ''),
                'dt_login_count': record.get('login_count', ''),
                'active': True if record.get('is_activated') == 1 else False,
                'dt_wallet_amount': float(record.get('wallet_amount')),
                'dt_reward_points_redeemed': float(record.get('reward_points_redeemed')),
                'dt_reward_points': float(record.get('reward_points')),
            }

            partner_id = False
            if record.get('phone', False):
                partner_id = self.env['res.partner'].search([('phone', '=', record.get('phone'))])
            # create partner
            if not partner_id:
                customer_dict.update({'phone': record.get('phone', '')})
                customer_id = self.create(customer_dict)
            # update partner
            else:
                partner_id.write(customer_dict)
