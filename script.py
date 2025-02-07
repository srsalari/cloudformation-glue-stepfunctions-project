import sys
from awsglue.transforms import ApplyMapping
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Parse arguments including the JOB_NAME passed by Glue.
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

# Initialize Spark and Glue contexts.
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Initialize the Glue job.
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

print("Hello from Glue!")

# Read input JSON data from S3 as a DynamicFrame.
datasource0 = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://q3-glue-project/inputs.json"]},
    format="json"
)

# Apply mapping to rename/transform fields.
# Note: Adjust field names and types based on your input data schema.
mapped_frame = ApplyMapping.apply(
    frame=datasource0,
    mappings=[
        ("field1", "string", "new_field1", "string"),
        ("field2", "int", "new_field2", "int")
    ]
)

# Convert the DynamicFrame to a Spark DataFrame and display its content.
df = mapped_frame.toDF()
df.show(truncate=False)

# Write the transformed data back to S3 in JSON format.
datasink = glueContext.write_dynamic_frame.from_options(
    frame=mapped_frame,
    connection_type="s3",
    connection_options={"path": "s3://q3-glue-project/script.py"},
    format="json"
)

# Commit the Glue job.
job.commit()