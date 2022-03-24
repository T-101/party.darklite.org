from tempus_dominus.widgets import DateTimePicker, DatePicker

OPTIONS = {'locale': 'en-ie', "icons": {"time": "fas fa-clock"}, 'format': 'YYYY-MM-DD HH:mm'}
ATTRS = {'class': 'form-group col-md-6', 'size': 'small'}


class LocaleDateTimePicker(DateTimePicker):
    def __init__(self, options=None, attrs=None, *args, **kwargs):
        if options is None:
            options = OPTIONS
        if attrs is None:
            attrs = ATTRS
        super().__init__(options=options, attrs=attrs, *args, **kwargs)
        self.size = "small"


class LocaleDatePicker(DatePicker):
    def __init__(self, options=None, attrs=None, *args, **kwargs):
        if options is None:
            options = {'locale': 'en-ie', 'format': 'YYYY-MM-DD'}
        if attrs is None:
            attrs = ATTRS
        super().__init__(options=options, attrs=attrs, *args, **kwargs)
        self.size = "small"
