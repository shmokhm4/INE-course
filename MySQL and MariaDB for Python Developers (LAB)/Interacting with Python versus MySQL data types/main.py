from samples import data1, data2, data3, data4, data5, data6

# دالة توحيد نوع البيانات
def unify_datatype(vals):
    # Floating point?
    if all(isinstance(v, float) for v in vals):
        return "DOUBLE PRECISION"

    # Integer?
    if all(isinstance(v, int) for v in vals):
        size = max(abs(v) for v in vals).bit_length()
        if size <= 16:
            return "SMALLINT"
        elif size <= 32:
            return "INTEGER"
        elif size <= 64:
            return "BIGINT"
        else:
            from math import log10
            return f"DECIMAL({int(1 + log10(2 ** size))})"

    # Decimal?
    from decimal import Decimal
    if all(isinstance(v, Decimal) for v in vals):
        to_right = 0
        to_left = 1
        for v in vals:
            v_str = str(v)
            to_right = max(to_right, v_str[::-1].find('.'))
            to_left = max(to_left, v_str.find('.'))
        to_right += 1
        return f"DECIMAL({to_left + to_right}, {to_right})"

    # If it is string, is it currency?
    if all(isinstance(v, str) and v[0] == '$' for v in vals):
        return "DECIMAL(10, 2)"

    # Handle fractions
    from fractions import Fraction
    if all(isinstance(v, Fraction) for v in vals):
        return "DOUBLE PRECISION"

    # If nothing else can be found, use TEXT
    return "TEXT"


# دالة استنتاج المخطط لبيانات مختلفة
def infer_schema_iterable(data_iterable):
    data = list(data_iterable)

    if not data:
        raise ValueError("The dataset is empty")

    object_type = type(data[0])

    if all(isinstance(item, dict) for item in data):
        keys = set().union(*(item.keys() for item in data))
        types = {}
        for key in keys:
            colvals = [item.get(key, None) for item in data]
            types[key] = unify_datatype(colvals)
    elif hasattr(object_type, '_fields'):
        fields = data[0]._fields
        types = {}
        for n, col in enumerate(fields):
            colvals = [getattr(row, col) for row in data]
            types[col] = unify_datatype(colvals)
    elif hasattr(object_type, '__dataclass_fields__'):
        fields = data[0].__dataclass_fields__.keys()
        types = {}
        for col in fields:
            colvals = [getattr(row, col) for row in data]
            types[col] = unify_datatype(colvals)
    elif all(isinstance(item, list) or isinstance(item, tuple) for item in data):
        max_length = max(len(item) for item in data)
        types = {}
        for i in range(max_length):
            colvals = [item[i] if i < len(item) else None for item in data]
            types[f'col{i}'] = unify_datatype(colvals)
    elif hasattr(object_type, '__dict__'):
        attributes = [attr for attr in dir(data[0]) if not attr.startswith('_')]
        types = {}
        for attr in attributes:
            colvals = [getattr(item, attr) for item in data]
            types[attr] = unify_datatype(colvals)
    else:
        raise ValueError("Unsupported data type in the dataset")

    # Format the DDL SQL command
    sql = [f"CREATE TABLE {object_type.__name__} ("]
    for col, typ in types.items():
        sql.append(f"    {col} {typ},")
    sql[-1] = sql[-1].rstrip(',')
    sql.append(");")

    return "\n".join(sql)


# استدعاء الدالة الجديدة واختبارها
data_iterables = [
    data1,  # Namedtuples
    data2,  # Namedtuples with different names
    data3,  # Namedtuples with currency
    data4,  # Mixed tuples and namedtuples
    data5,  # Single namedtuple
    data6  # Large integers
]

for data in data_iterables:
    try:
        print(infer_schema_iterable(data))
    except ValueError as err:
        print(err)
    print('-' * 50)

