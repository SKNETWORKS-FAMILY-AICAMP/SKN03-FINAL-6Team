from pymilvus import utility, MilvusClient

def create_manual_schema(dense_dim=1024):
    fields = [
        # Use auto generated id as primary key
        FieldSchema(
            name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100
        ),
        # Store the original text to retrieve based on semantically distance
        FieldSchema(name="model_id", dtype=DataType.INT32),
        FieldSchema(name="model", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2500),
        # Milvus now supports both sparse and dense vectors,
        # we can store each in a separate field to conduct hybrid search on both vectors
        FieldSchema(name="sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        FieldSchema(name="dense_vector", dtype=DataType.FLOAT_VECTOR, dim=dense_dim),
    ]
    schema = CollectionSchema(fields, enable_dynamic_field=True)

    col_name = "manual"
    if utility.has_collection(col_name, using='tailorlink'):
        Collection(col_name).drop()
    collection = Collection(col_name, schema, consistency_level="Strong", using=MILVUS_ALIAS)