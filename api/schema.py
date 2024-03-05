from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError


class MainSchema(Schema):
    no_input = fields.Boolean(required=False)
    output_path = fields.String(required=True)
    persistence = fields.Nested(PersistenceSchema, required=True)
    template_payload = fields.Nested(TemplatePayloadSchema, required=True)

class TemplatePayloadSchema(Schema):
    payload_dict = fields.Dict(required=True)

class CookieCutterTemplateSchema(Schema):
    template_context = fields.String(required=True)
    template_path = fields.String(required=True)
    context_vars = fields.Dict(required=True)

class PersistenceSchema(Schema):
    github = fields.Nested(RepoSchema, required=False, missing=None, data_key="github")
    gh = fields.Nested(RepoSchema, required=False, missing=None)

class RepoSchema(Schema):
    destination = fields.String(required=True)
    repo_type = fields.String(required=True, validate=lambda x: x in ['public', 'private'])
