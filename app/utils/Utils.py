from app.model.ActionResult import DataType

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    #return json.dumps(d)
    return d


# FIXME 统一封装数据
# 打包数据
def pack(data, data_type):
    if data is None or data_type is None:
        return data
    if data_type == DataType.OBJECT:
        return data
    elif data_type == DataType.LIST_OBJECT:
        result = list()
        result.append(data)
        return result
    elif data_type == DataType.LIST_DICT:
        result = list()
        result.append(data.json())
