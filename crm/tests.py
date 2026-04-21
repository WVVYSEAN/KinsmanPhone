"""
CRM test suite.

The email/password auth + UserInvite tests were removed when that feature
was reverted (migration 0024_drop_userinvite). All auth is now Google OAuth only.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import (
    Workspace, WorkspaceMembership, HeatSettings, Contact,
    DripEmail, DripEditExample,
)
from .drip import compute_outcome_score

User = get_user_model()


# ── Drip outcome scoring ──────────────────────────────────────────────────────

class ComputeOutcomeScoreTests(TestCase):

    def setUp(self):
        owner = User.objects.create_user(username='owner@t.com', email='owner@t.com', password='x')
        self.ws = Workspace.objects.create(name='Test WS', owner=owner)
        self.contact = Contact.objects.create(workspace=self.ws, name='Alice Test', email='alice@test.com')

    def _example(self, original='hello', edited=None):
        return DripEditExample(
            workspace=self.ws,
            contact=self.contact,
            original_body=original,
            edited_body=edited if edited is not None else original,
        )

    def test_reply_not_edited_scores_1_0(self):
        ex = self._example('hello')
        ex.reply_received = True
        self.assertEqual(compute_outcome_score(ex), 1.0)

    def test_reply_edited_scores_0_8(self):
        ex = self._example('hello', edited='world')
        ex.reply_received = True
        self.assertEqual(compute_outcome_score(ex), 0.8)

    def test_no_reply_not_edited_scores_0_5(self):
        ex = self._example('hello')
        ex.reply_received = False
        self.assertEqual(compute_outcome_score(ex), 0.5)

    def test_no_reply_edited_scores_0_2(self):
        ex = self._example('hello', edited='world')
        ex.reply_received = False
        self.assertEqual(compute_outcome_score(ex), 0.2)


# ── HeatSettings drip model defaults ──────────────────────────────────────────

class HeatSettingsDripDefaultsTests(TestCase):

    def setUp(self):
        owner = User.objects.create_user(username='o2@t.com', email='o2@t.com', password='x')
        self.ws = Workspace.objects.create(name='WS2', owner=owner)

    def test_drip_interval_default(self):
        cfg = HeatSettings.get_for_workspace(self.ws)
        self.assertEqual(cfg.drip_interval_days, 3)

    def test_drip_max_followups_default(self):
        cfg = HeatSettings.get_for_workspace(self.ws)
        self.assertEqual(cfg.drip_max_followups, 5)

    def test_training_data_min_quality_default(self):
        cfg = HeatSettings.get_for_workspace(self.ws)
        self.assertEqual(cfg.training_data_min_quality, 0.5)

    def test_drip_model_id_default_blank(self):
        cfg = HeatSettings.get_for_workspace(self.ws)
        self.assertEqual(cfg.drip_model_id, '')
