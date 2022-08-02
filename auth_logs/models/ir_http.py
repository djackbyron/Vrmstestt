from odoo import api, http, models


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(Http, self).session_info()
        res.update({
            'allow_delete_logs' : True if self.env.user.has_group('auth_logs.group_allow_delete_logs') else False
        })
        return res
