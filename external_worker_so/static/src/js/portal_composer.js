odoo.define('external_worker_so.portal_composer', function (require) {
'use strict';

const publicWidget = require('web.public.widget');
const session = require('web.session');
const portalComposer = require('portal.composer');
const {_t, qweb} = require('web.core');
var core = require('web.core');

const PortalComposer = portalComposer.PortalComposer;

    PortalComposer.include({
        events: _.extend({}, PortalComposer.prototype.events, {
        'click .o_portal_chatter_log_composer_btn': 'async _onLogSubmitButtonClick',
        }),
        xmlDependencies: (PortalComposer.prototype.xmlDependencies || [])
        .concat(['/external_worker_so/static/src/xml/portal_chatter.xml'
        ]),
        /**
     * @private
     * @param {Event} ev
     */
    _onLogSubmitButtonClick: function (ev) {
        ev.preventDefault();
        if (!this.$inputTextarea.val().trim() && !this.attachments.length) {
            this.$inputTextarea.addClass('border-danger');
            const error = _t('Some fields are required. Please make sure to write a message or attach a document');
            this.$(".o_portal_chatter_composer_error").text(error).removeClass('d-none');
            return Promise.reject();
        } else {
            return this._chatterPostMessage(ev.currentTarget.getAttribute('data-action'));
        }
    },

    });

});
