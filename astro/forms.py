from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField


class AddTransitMeaning(FlaskForm):
    meaning = CKEditorField("Meaning")
    submit = SubmitField("Save")
