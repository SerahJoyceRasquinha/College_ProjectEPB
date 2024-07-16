from django import forms
from django.core.validators import FileExtensionValidator

class FileUploadForm(forms.Form):
    course_category = forms.CharField(required=True)
    report_name = forms.CharField(required=True)
    input_excel = forms.FileField(required=True, validators=[FileExtensionValidator(allowed_extensions=["xlsx"])])