odoo.define('external_worker_so.portal_project_task', function (require) {
'use strict';

var rpc = require('web.rpc');

$(document).on('click', '.start_task', function(ev){
    self = this;
    let task_id = parseInt($(ev.currentTarget).attr('data-task-id'))
    return rpc.query({
        model: 'project.task',
        method: 'action_portal_timer_start',
        args: [task_id],
    }).then(function(result){
            $('.start_task').hide();
            $('.resume_task').hide();
            $('.stop_task').show();
            $('.pause_task').show();
    });
 });
 $(document).on('click', '.start_sec_task', function(ev){
    self = this;
    let task_id = parseInt($(ev.currentTarget).attr('data-task-id'))
    return rpc.query({
        model: 'project.task',
        method: 'action_portal_timer_start',
        args: [task_id],
    }).then(function(result){
            $('.start_sec_task').css('display','none');
            $('.stop_task').css('display','block');
            $('.pause_task').css('display','block');
    });
 });
 $(document).on('click', '.pause_task', function(ev){
    self = this;
    let task_id = parseInt($(ev.currentTarget).attr('data-task-id'))
    rpc.query({
        model: 'project.task',
        method: 'action_portal_timer_pause',
        args: [task_id],
    }).then(function(result){
        $('.pause_task').css('display','none');
        $('.resume_task').css('display','block');
    });
 });
 $(document).on('click', '.resume_task', function(ev){
    self = this;
    let task_id = parseInt($(ev.currentTarget).attr('data-task-id'))
    rpc.query({
        model: 'project.task',
        method: 'action_portal_timer_resume',
        args: [task_id],
    }).then(function(result){
            $('.resume_task').css('display','none');
            $('.pause_task').css('display','block');
    });
});
$(document).on('click', '.stop_task', function(ev){
    self = this;
    let task_id = parseInt($(ev.currentTarget).attr('data-task-id'))
    return rpc.query({
        model: 'project.task',
        method: 'action_portal_timer_stop',
         args: [task_id],
    }).then(function(result){
         $('.stop_task').css('display','none');
         $('.pause_task').css('display','none');
         $('.resume_task').css('display','none');
         $('.start_sec_task').css('display','block');
    });
});
});
