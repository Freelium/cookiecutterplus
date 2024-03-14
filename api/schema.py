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

{
  'no_input': True, 
  'output_path': '/private/var/folders/tj/tnbktw9s7rx0_qy2yp31gmnc0000gq/T/pytest-of-clyde.tedrick/pytest-19/test_cookiecutter_api_success0', 
  'template_payloads': [{
    'context_vars': {
      'component_name': 'My Cut Cookie', 
      'project_name': 'my-cut-cookie', 
      'project_slug': 'my-cut-cookie'
    }, 
    'name': 'gha', 
    'template_context': 'tests/fixtures/basic-backwards', 
    'template_path': ''
  }]
}


# class CookieCutterTemplateSchema(Schema):
#     name = fields.String(required=True)
#     template_context = fields.String(required=True)
#     template_path = fields.String(required=True)
#     context_vars = fields.Dict(required=True)

# class RepoSchema(Schema):
#     destination = fields.String(required=True)
#     repo_type = fields.String(required=True, validate=lambda x: x in ['public', 'private'])

# class PersistenceSchema(Schema):
#     gh = fields.Nested(RepoSchema, required=False)

# class MainSchema(Schema):
#     output_path = fields.String(required=True)
#     persistence = fields.Nested(PersistenceSchema, required=False)
#     template_payloads = fields.List(fields.Nested(CookieCutterTemplateSchema), required=True)
#     no_input = fields.Boolean(required=False, dump_default=True)
