from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField

class SearchForm(Form):
    query = TextField('Search', [])
    sort_by = TextField('sort_by', [],default="recent")
    repository = TextField('repository', [], default="pubmed")
    offset = HiddenField('offset',[],default=0)
    limit = HiddenField('offset',[],default=10)
    