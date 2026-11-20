from marshmallow import Schema, fields, validate

VALID_ROLES = ["admin", "analyst"]
VALID_LEVELS = ["Low", "Medium", "High", "Critical"]
VALID_VULN_STATUS = ["Open", "In Progress", "Patched"]
VALID_INCIDENT_STATUS = ["Open", "Investigating", "Resolved", "Closed"]

# 1. Schema User
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    role = fields.Str(load_default="analyst", validate=validate.OneOf(VALID_ROLES))
    created_at = fields.DateTime(dump_only=True)

# 2. Schema Asset
class AssetSchema(Schema):
    id = fields.Int(dump_only=True)
    owner_id = fields.Int(required=True)
    asset_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    asset_type = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    ip_address = fields.Str(required=True, validate=validate.Length(min=7, max=45))
    criticality = fields.Str(load_default="Medium", validate=validate.OneOf(VALID_LEVELS))
    created_at = fields.DateTime(dump_only=True)

# 3. Schema Vulnerability
class VulnerabilitySchema(Schema):
    id = fields.Int(dump_only=True)
    asset_id = fields.Int(required=True)
    cve_code = fields.Str(allow_none=True, validate=validate.Length(max=30))
    title = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    severity = fields.Str(required=True, validate=validate.OneOf(VALID_LEVELS))
    status = fields.Str(load_default="Open", validate=validate.OneOf(VALID_VULN_STATUS))
    discovered_at = fields.DateTime(dump_only=True)

# 4. Schema IncidentLog
class IncidentLogSchema(Schema):
    id = fields.Int(dump_only=True)
    incident_id = fields.Int(dump_only=True)
    analyst_id = fields.Int(required=True)
    action_taken = fields.Str(required=True, validate=validate.Length(min=3))
    logged_at = fields.DateTime(dump_only=True)

# 5. Schema Incident
class IncidentSchema(Schema):
    id = fields.Int(dump_only=True)
    asset_id = fields.Int(required=True)
    reporter_id = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    incident_type = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    severity = fields.Str(required=True, validate=validate.OneOf(VALID_LEVELS))
    status = fields.Str(load_default="Open", validate=validate.OneOf(VALID_INCIDENT_STATUS))
    description = fields.Str(allow_none=True)
    reported_at = fields.DateTime(dump_only=True)
    logs = fields.List(fields.Nested(IncidentLogSchema), dump_only=True)