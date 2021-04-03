from marshmallow import fields


def field_to_html(field: fields.Field, *args, **kwargs):
    return _field_to_html[type(field)](field, *args, **kwargs)


def inputString(field, name, value=None):
    req = " required" if field.required else ""
    val = f' value="{value}"' if value is not None else ""
    return f'<input type="text" name="{name}"{val}{req}>'


def inputBoolean(field, name, value=False):
    return f"{{ fields.boolean({name}, value={value}) }}"


def inputFloat(field, name, value=None):
    req = " required" if field.required else ""
    val = f' value="{value}"' if value is not None else ""
    return f'<input type="number" step="any" name="{name}"{val}{req}>'


def inputInteger(field, name, value=None):
    req = " required" if field.required else ""
    val = f' value="{value}"' if value is not None else ""
    return f'<input type="number" step=1 name="{name}"{val}{req}>'


def inputDate(field, name, value=None):
    req = " required" if field.required else ""
    val = f' value="{value}"' if value is not None else ""
    return f'<input type="date" name="{name}"{val}{req}>'


def inputDatetime(field, name, value=None):
    req = " required" if field.required else ""
    val = f' value="{value}"' if value is not None else ""
    return f'<input type="datetime-local" name="{name}"{val}{req}>'


def inputTime(field, name, value=None):
    req = " required" if field.required else ""
    val = f' value="{value}"' if value is not None else ""
    return f'<input type="time" name="{name}"{val}{req}>'


def inputEmail(field, name, value=None):
    req = " required" if field.required else ""
    val = f' value="{value}"' if value is not None else ""
    return f'<input type="email" name="{name}"{val}{req}>'


def inputUrl(field, name, value=None):
    req = " required" if field.required else ""
    val = f' value="{value}"' if value is not None else ""
    return f'<input type="url" name="{name}"{val}{req}>'


_field_to_html = {
    fields.String: inputString,
    fields.Boolean: inputBoolean,
    fields.Float: inputFloat,
    fields.Integer: inputInteger,
    fields.Date: inputDate,
    fields.DateTime: inputDatetime,
    fields.Time: inputTime,
    fields.Email: inputEmail,
    fields.Url: inputUrl,
}
