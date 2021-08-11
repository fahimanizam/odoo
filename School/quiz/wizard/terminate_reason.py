# See LICENSE file for full copyright and licensing details.

from odoo import models


class TerminateReasonEvent(models.TransientModel):
    _inherit = "terminate.reason"

    def save_terminate(self):
        """Override method to delete event participant and cancel
        event registration of student when he is terminated. """
        student_rec = self.env["student.student"].browse(
            self._context.get("active_id")
        )
        user_input_rec = self.env["survey.user_input"].search(
            [("part_name_id", "=", student_rec.id)]
        )
        if user_input_rec:
            user_input_rec.write({"state": "cancel"})
        event_participant = self.env["school.event.participant"].search(
            [("name", "=", student_rec.id)]
        )
        if event_participant:
            event_participant.unlink()
        return super(TerminateReasonEvent, self).save_terminate()
