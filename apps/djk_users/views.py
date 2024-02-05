from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django_jinja_knockout import tpl
from django_jinja_knockout.forms.vm_renderers import FormViewmodel
from django_jinja_knockout.models import model_fields_verbose_names
from django_jinja_knockout.viewmodels import vm_list
from django_jinja_knockout.views import ModelFormActionsView, page_context_decorator

from .forms import UserPreferencesForm


@page_context_decorator(view_title=_("Welcome"))
def main_page(request, **kwargs):
    return TemplateResponse(request, "welcome-main.htm")


class UserChangeFormViewmodel(FormViewmodel):

    def get_action_local_name(self):
        action_local_name = super().get_action_local_name()
        action_local_name = f"{action_local_name} {_("user")} {self.instance}"
        return action_local_name

    def get_verbose_name(self):
        verbose_names = model_fields_verbose_names(self.instance)
        verbose_names["full_name"] = "Full name"
        str_fields = self.get_object_desc(self.instance)
        str_fields["full_name"] = f'{str_fields.pop("first_name", "")} {str_fields.pop("last_name", "")}'.strip()
        if str_fields["full_name"] == "":
            del str_fields["full_name"]
        return tpl.print_bs_badges(str_fields, show_keys=1, i18n=verbose_names)


class UserChangeView(ModelFormActionsView):

    form = UserPreferencesForm
    # Overriding vm_form is optional and is not required:
    vm_form = UserChangeFormViewmodel

    def action_edit_form(self, obj=None):
        if obj is None:
            obj = self.get_object_for_action()
        if self.request.user.is_superuser or obj == self.request.user:
            return super().action_edit_form(obj)
        else:
            return vm_list(
                {"view": "alert_error", "message": "You do not have the rights to edit another user preferences."}
            )
