from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError

class ContextVarsSchema(Schema):
    component_name = fields.Str()
    project_name = fields.Str()
    project_slug = fields.Str()

class TemplatePayloadSchema(Schema):
    name = fields.Str()
    template_context = fields.Str()
    template_path = fields.Str()
    context_vars = fields.Nested(ContextVarsSchema())

class CcplusSchema(Schema):
    badParameter = fields.Str()

class RepoSchema(Schema):
    destination = fields.String(required=True)
    repo_type = fields.String(required=True, validate=lambda x: x in ['public', 'private'])

class PersistenceSchema(Schema):
    gh = fields.Nested(RepoSchema, required=False)

class MainSchema(Schema):
    template_payloads = fields.List(fields.Nested(TemplatePayloadSchema), required=True)
    persistence = fields.Nested(PersistenceSchema, required=False)
    ccplus = fields.Nested(CcplusSchema, required=False)
    output_path = fields.Str(required=False)
    no_input = fields.Boolean(required=False, dump_default=True)
