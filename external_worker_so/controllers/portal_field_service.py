# -*- coding: utf-8 -*-

from collections import OrderedDict
from odoo import http, _
from operator import itemgetter
from odoo.http import request
from markupsafe import Markup
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.osv.expression import OR, AND
from odoo.tools import groupby as groupbyelem


class CustomerPortalFieldServiceInherit(CustomerPortal):

    # ------------------------------------------------------------
    # My service
    # ------------------------------------------------------------
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'service_count' in counters:
            values['service_count'] = request.env['project.task'].sudo().search_count(
                [('user_ids', 'in', request.env.user.id), ('is_fsm', '=', True)]) \
                if request.env['project.task'].check_access_rights('read', raise_exception=False) else 0
        return values

    def _service_get_page_view_values(self, service, access_token, **kwargs):
        page_name = 'service'
        history = 'my_service_history'
        try:
            project_accessible = bool(
                service.project_id.id and self._document_check_access('project.project', service.project_id.id))
        except (AccessError, MissingError):
            project_accessible = False
        project_types = request.env['project.task.type'].search(
            [('project_ids', 'in', service.project_id and service.project_id.ids or False)])
        values = {
            'page_name': page_name,
            'service': service,
            'user': request.env.user,
            'project_accessible': project_accessible,
            'project_types': project_types,
            'service_stage_id': service.stage_id,
        }
        return self._get_page_view_values(service, access_token, values, history, False, **kwargs)

    def _service_get_searchbar_sortings(self):
        return {
            'date': {'label': _('Newest'), 'order': 'create_date desc', 'sequence': 1},
            'name': {'label': _('Title'), 'order': 'name', 'sequence': 2},
            'project': {'label': _('Project'), 'order': 'project_id, stage_id', 'sequence': 3},
            'users': {'label': _('Assignees'), 'order': 'user_ids', 'sequence': 4},
            'stage': {'label': _('Stage'), 'order': 'stage_id, project_id', 'sequence': 5},
            'status': {'label': _('Status'), 'order': 'kanban_state', 'sequence': 6},
            'priority': {'label': _('Priority'), 'order': 'priority desc', 'sequence': 7},
            'date_deadline': {'label': _('Deadline'), 'order': 'date_deadline asc', 'sequence': 8},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc', 'sequence': 11},
            'planned_date_begin': {'label': _('Start Date'), 'order': 'planned_date_begin desc', 'sequence': 12},
            'planned_date_end': {'label': _('End Date'), 'order': 'planned_date_end desc', 'sequence': 13},
        }

    def _service_get_searchbar_groupby(self):
        values = {
            'none': {'input': 'none', 'label': _('None'), 'order': 1},
            'project': {'input': 'project', 'label': _('Project'), 'order': 2},
            'stage': {'input': 'stage', 'label': _('Stage'), 'order': 4},
            'status': {'input': 'status', 'label': _('Status'), 'order': 5},
            'priority': {'input': 'priority', 'label': _('Priority'), 'order': 6},
            'customer': {'input': 'customer', 'label': _('Customer'), 'order': 9},
            'planned_date_begin': {'input': 'planned_date_begin', 'label': _('Start Date'), 'order': 10},
            'planned_date_end': {'input': 'planned_date_end', 'label': _('End Date'), 'order': 11},
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    def _service_get_groupby_mapping(self):
        return {
            'project': 'project_id',
            'stage': 'stage_id',
            'customer': 'partner_id',
            'priority': 'priority',
            'planned_date_begin': 'planned_date_begin',
            'planned_date_end': 'planned_date_end',
            'status': 'kanban_state',
        }

    def _service_get_order(self, order, groupby):
        groupby_mapping = self._service_get_groupby_mapping()
        field_name = groupby_mapping.get(groupby, '')
        if not field_name:
            return order
        return '%s, %s' % (field_name, order)

    def _service_get_searchbar_inputs(self):
        values = {
            'all': {'input': 'all', 'label': _('Search in All'), 'order': 1},
            'content': {'input': 'content', 'label': Markup(_('Search <span class="nolabel"> (in Content)</span>')),
                        'order': 1},
            'ref': {'input': 'ref', 'label': _('Search in Ref'), 'order': 1},
            'project': {'input': 'project', 'label': _('Search in Project'), 'order': 2},
            'users': {'input': 'users', 'label': _('Search in Assignees'), 'order': 3},
            'stage': {'input': 'stage', 'label': _('Search in Stages'), 'order': 4},
            'status': {'input': 'status', 'label': _('Search in Status'), 'order': 5},
            'priority': {'input': 'priority', 'label': _('Search in Priority'), 'order': 6},
            'message': {'input': 'message', 'label': _('Search in Messages'), 'order': 10},
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    def _service_get_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ('content', 'all'):
            search_domain.append([('name', 'ilike', search)])
            search_domain.append([('description', 'ilike', search)])
        if search_in in ('customer', 'all'):
            search_domain.append([('partner_id', 'ilike', search)])
        if search_in in ('message', 'all'):
            search_domain.append([('message_ids.body', 'ilike', search)])
        if search_in in ('stage', 'all'):
            search_domain.append([('stage_id', 'ilike', search)])
        if search_in in ('project', 'all'):
            search_domain.append([('project_id', 'ilike', search)])
        if search_in in ('ref', 'all'):
            search_domain.append([('id', 'ilike', search)])
        if search_in in ('users', 'all'):
            user_ids = request.env['res.users'].sudo().search([('name', 'ilike', search)])
            search_domain.append([('user_ids', 'in', user_ids.ids)])
        if search_in in ('priority', 'all'):
            search_domain.append([('priority', 'ilike', search == 'normal' and '0' or '1')])
        if search_in in ('status', 'all'):
            search_domain.append([
                ('kanban_state', 'ilike',
                 'normal' if search == 'In Progress' else 'done' if search == 'Ready' else 'blocked' if search == 'Blocked' else search)
            ])
        return OR(search_domain)

    @http.route(['/my/services', '/my/services/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_services(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                           search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = self._service_get_searchbar_sortings()
        searchbar_sortings = dict(sorted(self._service_get_searchbar_sortings().items(),
                                         key=lambda item: item[1]["sequence"]))

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }

        searchbar_inputs = self._service_get_searchbar_inputs()
        searchbar_groupby = self._service_get_searchbar_groupby()

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
            sortby = 'planned_date_begin'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        domain += [('user_ids', 'in', request.env.user.id), ('is_fsm', '=', True)]

        # default group by value
        if not groupby:
            groupby = 'planned_date_begin'

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            domain += self._service_get_search_domain(search_in, search)

        ServiceSudo = request.env['project.task'].sudo()
        domain = AND([domain, request.env['ir.rule']._compute_domain(ServiceSudo._name, 'read')])

        # service count
        service_count = ServiceSudo.search_count(domain)
        print("--------------------", domain)
        # pager
        pager = portal_pager(
            url="/my/services",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'groupby': groupby, 'search_in': search_in, 'search': search},
            total=service_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        order = self._service_get_order(order, groupby)

        services = ServiceSudo.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_service_history'] = services.ids[:100]

        groupby_mapping = self._service_get_groupby_mapping()
        group = groupby_mapping.get(groupby)
        print("--------------------grouped_tasks", group)
        if group:
            grouped_tasks = [request.env['project.task'].concat(*g) for k, g in
                             groupbyelem(services, itemgetter(group))]
        else:
            grouped_tasks = [services]
        print("--------------------grouped_tasks", grouped_tasks)

        task_states = dict(request.env['project.task']._fields['kanban_state']._description_selection(request.env))
        if sortby == 'status':
            if groupby == 'none' and grouped_tasks:
                grouped_tasks[0] = grouped_tasks[0].sorted(lambda services: task_states.get(services.kanban_state))
            else:
                grouped_tasks.sort(key=lambda services: task_states.get(services[0].kanban_state))

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_tasks': grouped_tasks,
            'page_name': 'service',
            'default_url': '/my/services',
            'service_url': 'service',
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
        return request.render("external_worker_so.portal_my_services", values)

    @http.route(['/my/service/<int:service_id>'], type='http', auth="public", website=True)
    def portal_my_service(self, service_id, access_token=None, **kw):
        try:
            service_sudo = self._document_check_access('project.task', service_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        # ensure attachment are accessible with access token inside template
        for attachment in service_sudo.attachment_ids:
            attachment.generate_access_token()
        values = self._service_get_page_view_values(service_sudo, access_token, **kw)
        portal_task_id = request.env['project.task'].browse(service_id)

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
        return request.render("external_worker_so.portal_my_service", values)
