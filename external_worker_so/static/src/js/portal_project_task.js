odoo.define('external_worker_so.portal_project_task', function (require) {
'use strict';
console.log("-----------------------portal_project_task")

const publicWidget = require('web.public.widget');
const Widget = require('web.Widget');

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
//            $('.resume_task').hide();
//            $('.stop_task').show();
//            $('.pause_task').show();
    });
     console.log("test")
 });
 $(document).on('click', '.start_sec_task', function(ev){
    self = this;
    let task_id = parseInt($(ev.currentTarget).attr('data-task-id'))
    return rpc.query({
        model: 'project.task',
        method: 'action_portal_timer_start',
        args: [task_id],
    }).then(function(result){
            $('.start_task').hide();
//            $('.start_sec_task').hide();
            $('.stop_task').show();
            $('.pause_task').show();
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
        $('.pause_task').hide();
        $('.start_task').show()
        $('.resume_task').show()


    });
     console.log("test")
 });
 $(document).on('click', '.resume_task', function(ev){
    self = this;
    let task_id = parseInt($(ev.currentTarget).attr('data-task-id'))
    rpc.query({
        model: 'project.task',
        method: 'action_portal_timer_resume',
        args: [task_id],
    }).then(function(result){
            $('.resume_task').hide();
            $('.pause_task').show();
            $('.stop_task').show();
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
         if (!result.display_timer_stop || result.encode_uom_in_days) {
            $('.stop_task').hide();
            $('.start_task').show()
            $('.pause_task').show()
         }
    });
});
});
