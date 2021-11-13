"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
from pulumi_aws import s3

# For pulling config options
config = pulumi.Config()

# Create an AWS resource (S3 Bucket)
# Use the stack, which is the environment name for
# bucket naming.
bucket = s3.Bucket('%s.%s.site' % (aws.get_region().name, pulumi.get_stack()))

# Add a file
bucketObject = s3.BucketObject(
    'index.html',
    bucket=bucket.id,
    source=pulumi.FileAsset('www/index.html')
)

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
