from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError


class CookieCutterTemplateSchema(Schema):
    template_context = fields.String(required=True)
    template_path = fields.String(required=True)
    context_vars = fields.Dict(required=True)


class RepoSchema(Schema):
    destination = fields.String(required=True)
    repo_type = fields.String(required=True, validate=lambda x: x in ['public', 'private'])


class PersistenceSchema(Schema):
    gh = fields.Nested(RepoSchema, required=False)


class MainSchema(Schema):
    output_path = fields.String(required=True)
    persistence = fields.Nested(PersistenceSchema, required=False)
    template_payload = fields.Dict(keys=fields.Str(), values=fields.Nested(CookieCutterTemplateSchema), required=True)
    no_input = fields.Boolean(required=False, dump_default=True)
