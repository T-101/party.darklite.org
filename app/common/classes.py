from tempus_dominus.widgets import DateTimePicker, DatePicker

OPTIONS = {'locale': 'en-ie', "icons": {"time": "fas fa-clock"}, 'format': 'YYYY-MM-DD HH:mm'}
ATTRS = {'class': 'form-group col-md-6', 'size': 'small', "input_toggle": False, "type": "date",
         "append": "fas fa-calendar", 'placeholder': 'YYYY-MM-DD HH:mm'}


class LocaleDateTimePicker(DateTimePicker):
    def __init__(self, options=None, attrs=None, *args, **kwargs):
        attrs = attrs or {}
        options = options or {}
        super().__init__(options=OPTIONS | options, attrs=ATTRS | attrs, *args, **kwargs)


class LocaleDatePicker(DatePicker):
    def __init__(self, options=None, attrs=None, *args, **kwargs):
        attrs = attrs or {}
        options = options or {}
        attrs["placeholder"] = "YYYY-MM-DD"
        options["format"] = 'YYYY-MM-DD'
        super().__init__(options=OPTIONS | options, attrs=ATTRS | attrs, *args, **kwargs)
