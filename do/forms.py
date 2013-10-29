from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms

__author__ = 'stefanotranquillini'


class TaskForm(forms.Form):
    task = forms.CharField(label="")

    def clean_task(self):
        task = self.cleaned_data['task']
        if task.find("#p") == -1:
            raise forms.ValidationError("Priority not set")
        # if task.find("@") == -1:
        #     raise forms.ValidationError("List not set")
        return task


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'form'
        # self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        # self.helper.form_class = 'form-inline'
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-xs-1'
        # self.helper.field_class = 'col-xs-10'
        self.helper.layout = Layout(
            Field('task', placeholder="Do something amazing")
            # FieldWithButtons('task', StrictButton("Go!"))
            # StrictButton('Sign in', css_class='btn-default'),
        )

        super(TaskForm, self).__init__(*args, **kwargs)