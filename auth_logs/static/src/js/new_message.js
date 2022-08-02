/** @odoo-module **/
import { registerInstancePatchModel, registerFieldPatchModel, } from '@mail/model/model_core';
import { session } from '@web/session';
import { attr } from '@mail/model/model_field';

registerFieldPatchModel('mail.message', 'mail/static/src/models/message/message.js.js', {
    /**
     * Whether this message can be deleted.
     */
    NewcanBeDeleted: attr({
        compute: '_NewcomputeCanBeDeleted',
    }),
});

registerInstancePatchModel('mail.message', 'mail/static/src/models/message/message.js.js', {

    /**
     * @returns {boolean}
     */
     _NewcomputeCanBeDeleted() { 
        if (session.allow_delete_logs){
            return true;
        }
        return false;
    }
});