from .models import Gist

def get_operator(suffix):
    operators = {'lt': '<', 'lte': '<=', 'gt': '>', 'gte': '>='}
    return operators.get(suffix)

def build_query(**kwargs):
    query = "SELECT * FROM gists"
    conditions = []
    params = {}

    if 'github_id' in kwargs:
        conditions.append("github_id = :github_id")
        params['github_id'] = kwargs['github_id']

    datetime_fields = ['created_at', 'updated_at']
    for field in datetime_fields:
        if field in kwargs:
            conditions.append(f"datetime({field}) = datetime(:{field})")
            params[field] = kwargs[field]

        for suffix in ['gt', 'gte', 'lt', 'lte']:
            key = f"{field}__{suffix}"
            if key in kwargs:
                op = get_operator(suffix)
                conditions.append(f"datetime({field}) {op} datetime(:{key})")
                params[key] = kwargs[key]

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    return query, params

def search_gists(db_connection, **kwargs):
    if kwargs:
        query, params = build_query(**kwargs)
        results = db_connection.execute(query, params).fetchall()
    else:
        query = "SELECT * FROM gists"
        results = db_connection.execute(query).fetchall()

    return [Gist(row) for row in results]