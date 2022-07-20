from vault import db


class ExtractConfig(db.Model):
    __tablename__ = 'thanos_extract_config'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer)
    source_instance_id = db.Column(db.Integer)
    source_database = db.Column(db.String)
    source_table = db.Column(db.String)
    is_regex = db.Column(db.Integer)
    primary_keys = db.Column(db.String)
    extract_columns = db.Column(db.String)
    target_instance_id = db.Column(db.Integer)
    target_database = db.Column(db.String)
    target_table = db.Column(db.String)
    partition_type = db.Column(db.Integer)
    partition_input_column = db.Column(db.String)
    partition_output_column = db.Column(db.String)
    ignore_delete = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
