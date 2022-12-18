from marshmallow import Schema, fields


class LocationSchema(Schema):
    #id = fields.Integer()
    person_id = fields.Integer(attribute="person_id")
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")

