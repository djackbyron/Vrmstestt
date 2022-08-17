# -*- coding: utf-8 -*-

from collections import OrderedDict
from operator import itemgetter
from odoo import http, _
from werkzeug.exceptions import Forbidden
from odoo.http import request
from odoo.osv import expression
from odoo.addons.project.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.tools import groupby as groupbyelem
from odoo.osv.expression import OR, AND
from odoo.tools import consteq, plaintext2html
from odoo.addons.portal.controllers import mail
from odoo.exceptions import AccessError, MissingError


def _check_special_access(res_model, res_id, token='', _hash='', pid=False):
    record = request.env[res_model].browse(res_id).sudo()
    if _hash and pid:  # Signed Token Case: hash implies token is signed by partner pid
        return consteq(_hash, record._sign_token(pid))
    elif token:  # Token Case: token is the global one of the document
        token_field = request.env[res_model]._mail_post_token_field
        return (token and record and consteq(record[token_field], token))
    else:
        raise Forbidden()


class PortalChatterExternal(mail.PortalChatter):

    @http.route('/mail/chatter_fetch', type='json', auth='public', website=True)
    def portal_message_fetch(self, res_model, res_id, domain=False, limit=10, offset=0, **kw):
        if not domain:
            domain = []
        # Only search into website_message_ids, so apply the same domain to perform only one search
        # extract domain from the 'website_message_ids' field
        model = request.env[res_model]
        field = model._fields['website_message_ids']
        field_domain = field.get_domain_list(model)
        domain = expression.AND([
            domain,
            field_domain,
            [('res_id', '=', res_id), '|', ('body', '!=', ''), ('attachment_ids', '!=', False)]
        ])

        # Check access
        Message = request.env['mail.message']
        if kw.get('token'):
            access_as_sudo = _check_special_access(res_model, res_id, token=kw.get('token'))
            if not access_as_sudo:  # if token is not correct, raise Forbidden
                raise Forbidden()
            # Non-employee see only messages with not internal subtype (aka, no internal logs)
            # if not request.env['res.users'].has_group('base.group_user'):
            #     domain = expression.AND([Message._get_search_domain_share(), domain])
            Message = request.env['mail.message'].sudo()
        return {
            'messages': Message.search(domain, limit=limit, offset=offset).portal_message_format(),
            'message_count': Message.search_count(domain)
        }

    @http.route(['/mail/chatter_log_a_note'], type='json', methods=['POST'], auth='public', website=True)
    def portal_chatter_log_a_note(self, res_model, res_id, message, attachment_ids=None, attachment_tokens=None, **kw):
        """Create a new `mail.message` with the given `message` and/or `attachment_ids` and return new message values.

        The message will be associated to the record `res_id` of the model
        `res_model`. The user must have access rights on this target document or
        must provide valid identifiers through `kw`. See `_message_post_helper`.
        """
        res_id = int(res_id)

        self._portal_post_check_attachments(attachment_ids or [], attachment_tokens or [])

        if message or attachment_ids:
            result = {'default_message': message}
            # message is received in plaintext and saved in html
            if message:
                message = plaintext2html(message)
            post_values = {
                'res_model': res_model,
                'res_id': res_id,
                'message': message,
                'send_after_commit': False,
                'attachment_ids': False,  # will be added afterward
            }
            post_values.update((fname, kw.get(fname)) for fname in self._portal_post_filter_params())
            post_values['_hash'] = kw.get('hash')
            post_values['message_type'] = 'comment'
            post_values['subtype_xmlid'] = 'mail.mt_note'
            message = _message_post_helper(**post_values)
            result.update({'default_message_id': message.id})

            if attachment_ids:
                # sudo write the attachment to bypass the read access
                # verification in mail message
                record = request.env[res_model].browse(res_id)
                message_values = {'res_id': res_id, 'model': res_model}
                attachments = record._message_post_process_attachments([], attachment_ids, message_values)

                if attachments.get('attachment_ids'):
                    message.sudo().write(attachments)

                result.update({'default_attachment_ids': message.attachment_ids.sudo().read(
                    ['id', 'name', 'mimetype', 'file_size', 'access_token'])})
            return result


class CustomerPortalInherit(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        """
        Inherit this base method and showing only their task.
        :param counters:
        :return:
        """
        values = super()._prepare_home_portal_values(counters)
        if 'task_count' in counters:
            values['task_count'] = request.env['project.task'].search_count([('user_ids', 'in', request.env.user.id)]) \
                if request.env['project.task'].check_access_rights('read', raise_exception=False) else 0
        return values

    @http.route(['/my/tasks', '/my/tasks/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tasks(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                        search_in='content', groupby=None, **kw):
        """
        Override this base method and showing only their task.
        :param page:
        :param date_begin:
        :param date_end:
        :param sortby:
        :param filterby:
        :param search:
        :param search_in:
        :param groupby:
        :param kw:
        :return:
        """
        values = self._prepare_portal_layout_values()
        searchbar_sortings = self._task_get_searchbar_sortings()
        searchbar_sortings = dict(sorted(self._task_get_searchbar_sortings().items(),
                                         key=lambda item: item[1]["sequence"]))

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }

        searchbar_inputs = self._task_get_searchbar_inputs()
        searchbar_groupby = self._task_get_searchbar_groupby()

        # extends filterby criteria with project the customer has access to
        projects = request.env['project.project'].search([])
        for project in projects:
            searchbar_filters.update({
                str(project.id): {'label': project.name, 'domain': [('project_id', '=', project.id)]}
            })

        # extends filterby criteria with project (criteria name is the project id)
        # Note: portal users can't view projects they don't follow
        project_groups = request.env['project.task'].read_group([('project_id', 'not in', projects.ids)],
                                                                ['project_id'], ['project_id'])
        for group in project_groups:
            proj_id = group['project_id'][0] if group['project_id'] else False
            proj_name = group['project_id'][1] if group['project_id'] else _('Others')
            searchbar_filters.update({
                str(proj_id): {'label': proj_name, 'domain': [('project_id', '=', proj_id)]}
            })

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        # default group by value
        if not groupby:
            groupby = 'project'

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # only see own task
        domain += [('user_ids', 'in', request.env.user.id)]

        # search
        if search and search_in:
            domain += self._task_get_search_domain(search_in, search)

        TaskSudo = request.env['project.task'].sudo()
        domain = AND([domain, request.env['ir.rule']._compute_domain(TaskSudo._name, 'read')])

        # task count
        task_count = TaskSudo.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/tasks",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'groupby': groupby, 'search_in': search_in, 'search': search},
            total=task_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        order = self._task_get_order(order, groupby)

        tasks = TaskSudo.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_tasks_history'] = tasks.ids[:100]

        groupby_mapping = self._task_get_groupby_mapping()
        group = groupby_mapping.get(groupby)
        if group:
            grouped_tasks = [request.env['project.task'].concat(*g) for k, g in groupbyelem(tasks, itemgetter(group))]
        else:
            grouped_tasks = [tasks]

        task_states = dict(request.env['project.task']._fields['kanban_state']._description_selection(request.env))
        if sortby == 'status':
            if groupby == 'none' and grouped_tasks:
                grouped_tasks[0] = grouped_tasks[0].sorted(lambda tasks: task_states.get(tasks.kanban_state))
            else:
                grouped_tasks.sort(key=lambda tasks: task_states.get(tasks[0].kanban_state))

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_tasks': grouped_tasks,
            'page_name': 'task',
            'default_url': '/my/tasks',
            'task_url': 'task',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("project.portal_my_tasks", values)

    @http.route(['/my/task/<int:task_id>'], type='http', auth="public", website=True)
    def portal_my_task(self, task_id, access_token=None, **kw):
        try:
            task_sudo = self._document_check_access('project.task', task_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        # ensure attachment are accessible with access token inside template
        for attachment in task_sudo.attachment_ids:
            attachment.generate_access_token()
        values = self._task_get_page_view_values(task_sudo, access_token, **kw)
        portal_task_id = request.env['project.task'].browse(task_id)

        # start
        if portal_task_id.display_timer_start_primary:
            values['start_timer_visible'] = True
        else:
            values['start_timer_visible'] = False

        # start secondary
        if portal_task_id.display_timer_start_secondary:
            values['start_sec_timer_visible'] = True
        else:
            values['start_sec_timer_visible'] = False

        # stop
        if portal_task_id.display_timer_stop:
            values['stop_timer_visible'] = True
        else:
            values['stop_timer_visible'] = False

        # pause
        if portal_task_id.display_timer_pause:
            values['pause_timer_visible'] = True
        else:
            values['pause_timer_visible'] = False

        # resume
        if portal_task_id.display_timer_resume:
            values['resume_timer_visible'] = True
        else:
            values['resume_timer_visible'] = False
        return request.render("project.portal_my_task", values)
