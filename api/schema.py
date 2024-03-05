from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError

class TemplatePayloadSchema(Schema):
    template_context = fields.String(required=True)
    template_path = fields.String(required=True)
    context_vars = fields.Dict(required=True)

class PersistenceSchema(Schema):
    destination = fields.String(required=True)
    persistence_type = fields.String(required=True)

class MainSchema(Schema):
    no_input = fields.Boolean(required=False)
    output_path = fields.String(required=True)
    persistence = fields.Nested(PersistenceSchema, required=True)
    template_payload = fields.Nested(TemplatePayloadSchema, required=True)
