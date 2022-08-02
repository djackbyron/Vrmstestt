odoo.define('external_worker_so.portal_chatter', function (require) {
'use strict';

const publicWidget = require('web.public.widget');
const session = require('web.session');
const portalchatter = require('portal.chatter');
const {_t, qweb} = require('web.core');
var core = require('web.core');

const PortalChatter = portalchatter.PortalChatter;

    PortalChatter.include({
    events: _.extend({}, PortalChatter.prototype.events, {
    'click .o_portal_chatter_log_composer_btn': 'async _onLogSubmitButtonClick',
    }),
    xmlDependencies: (PortalChatter.prototype.xmlDependencies || [])
    .concat(['/external_worker_so/static/src/xml/portal_chatter.xml'
    ]),
    /**
     * @private
     * @param {Event} ev
     */
    _onLogSubmitButtonClick: function (ev) {
        ev.preventDefault();
        var message = $('.o_portal_chatter_composer_input textarea[name="message"]');
        var attachments = $('.o_portal_chatter_composer_input .o_portal_chatter_attachments');

        if (!attachments.length) {
            $('.o_portal_chatter_composer_input textarea[name="message"]').addClass('border-danger');
            const error = _t('Some fields are required. Please make sure to write a message or attach a document');
            $(".o_portal_chatter_composer_error").text(error).removeClass('d-none');
            return Promise.reject();
        } else if (!message.val().trim()) {
            $('.o_portal_chatter_composer_input textarea[name="message"]').addClass('border-danger');
            const error = _t('Some fields are required. Please make sure to write a message or attach a document');
            $(".o_portal_chatter_composer_error").text(error).removeClass('d-none');
            return Promise.reject();
        }
        else {
            return this._chatterPostMessage(ev.currentTarget.getAttribute('data-action'));
        }
    },
    /**
     * post message using rpc call and display new message and message count
     *
     * @private
     * @param {String} route
     * @returns {Promise}
     */
    _chatterPostMessage: async function (route) {
        const result = await this._rpc({
            route: route,
            params: this._prepareMessageData(),
        });
        core.bus.trigger('reload_chatter_content', result);
        return result;
    },
    /**
     * prepares data to send message
     *
     * @private
     */
    _prepareMessageData: function () {
        return Object.assign(this.options || {}, {
            'message': this.$('textarea[name="message"]').val(),
            'attachment_ids': _.pluck(this.attachments, 'id'),
            'attachment_tokens': _.pluck(this.attachments, 'access_token'),
        });
    },
    });
});
