from collections import OrderedDict

from django_jinja_knockout.forms import RendererModelForm

from apps.users.models import CustomUser


def user__get_str_fields(self):
    str_fields = OrderedDict(
        [
            ("email", self.email),
        ]
    )
    if self.first_name:
        str_fields["first_name"] = self.first_name
    if self.last_name:
        str_fields["last_name"] = self.last_name
    return str_fields


# Monkey patch User model to support .get_str_fields(), used by ModelFormActionsView / KoGridView.
# It's not required, just serves an example and improves User interface.
CustomUser.get_str_fields = user__get_str_fields


class UserPreferencesForm(RendererModelForm):

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")
