from wtforms import Form, SelectField, validators, IntegerField
from wtforms.widgets.html5 import NumberInput, DateInput
from wtforms.fields.html5 import DateField
from datetime import datetime

class HousesForm(Form):
    timestamp = DateField('Timestamp', default=datetime.today, format='%Y-%m-%d')
    full_sq = IntegerField('Full area', widget=NumberInput(), default=50)
    life_sq = IntegerField('Life area', widget=NumberInput(), default=50)
    num_room = IntegerField('Number of rooms', widget=NumberInput(), default=1)
    floor = IntegerField('Floor', widget=NumberInput(), default=1)
    max_floor = IntegerField('Max Floor', widget=NumberInput(), default=1)
    build_year = IntegerField('Build year', widget=NumberInput(), default=1950)
    sub_area = SelectField('Sub area')
    

    # password = PasswordField('New Password', [
    #     validators.DataRequired(),
    #     validators.EqualTo('confirm', message='Passwords must match')
    # ])
    # confirm = PasswordField('Repeat Password')
	