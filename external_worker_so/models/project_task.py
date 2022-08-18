# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProjectTaskInherited(models.Model):
    _inherit = 'project.task'

    def action_portal_timer_start(self):
        data = {}
        self.sudo().action_timer_start()
        data.update({
            'encode_uom_in_days': self.encode_uom_in_days,
            'display_timer_start_primary': self.display_timer_start_primary,
            'display_timer_start_secondary': self.display_timer_start_secondary,
            'display_timer_stop': self.display_timer_stop,
            'display_timer_pause': self.display_timer_pause,
            'display_timer_resume': self.display_timer_resume,
        })
        return data

    def action_portal_timer_pause(self):
        data = {}
        self.sudo().action_timer_pause()
        data.update({
            'encode_uom_in_days': self.encode_uom_in_days,
            'display_timer_start_primary': self.display_timer_start_primary,
            'display_timer_start_secondary': self.display_timer_start_secondary,
            'display_timer_stop': self.display_timer_stop,
            'display_timer_pause': self.display_timer_pause,
            'display_timer_resume': self.display_timer_resume,
        })
        return data

    def action_portal_timer_resume(self):
        data = {}
        self.sudo().action_timer_resume()
        data.update({
            'encode_uom_in_days': self.encode_uom_in_days,
            'display_timer_start_primary': self.display_timer_start_primary,
            'display_timer_start_secondary': self.display_timer_start_secondary,
            'display_timer_stop': self.display_timer_stop,
            'display_timer_pause': self.display_timer_pause,
            'display_timer_resume': self.display_timer_resume,
        })
        return data

    def action_portal_timer_stop(self):
        data = {}
        self = self.sudo()
        if self.user_timer_id.timer_start and self.display_timesheet_timer:
            rounded_hours = self._get_rounded_hours(self.user_timer_id._get_minutes_spent())
            wizard_round = self.env['project.task.create.timesheet'].create({
                'time_spent': rounded_hours,
                'task_id': self.id,
            })
            wizard_round.save_timesheet()
        data.update({
            'encode_uom_in_days': self.encode_uom_in_days,
            'display_timer_start_primary': self.display_timer_start_primary,
            'display_timer_start_secondary': self.display_timer_start_secondary,
            'display_timer_stop': self.display_timer_stop,
            'display_timer_pause': self.display_timer_pause,
            'display_timer_resume': self.display_timer_resume,
        })
        return data

    def portal_stage_change(self, stage_id=False):
        data = {}
        self = self.sudo()
        self.stage_id = stage_id
        data.update({
            'stage_id': self.stage_id,
        })
        return data
