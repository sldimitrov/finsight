from django.test import SimpleTestCase

from .forms import AccountForm


class AccountFormTests(SimpleTestCase):
    def test_valid_account_data_is_accepted(self):
        form = AccountForm(
            data={
                "name": "Everyday account",
                "type": "checking",
                "balance": "125.50",
                "currency": "BGN",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_account_type_is_rejected(self):
        form = AccountForm(
            data={
                "name": "Everyday account",
                "type": "unknown",
                "balance": "125.50",
                "currency": "BGN",
            }
        )

        self.assertFalse(form.is_valid())

    def test_user_and_active_status_are_not_editable(self):
        form = AccountForm()

        self.assertNotIn("user", form.fields)
        self.assertNotIn("is_active", form.fields)
