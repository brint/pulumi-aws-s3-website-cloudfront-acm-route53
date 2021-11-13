"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
# Use the stack, which is the environment name for
# bucket naming.
bucket = s3.Bucket('%s.site' % pulumi.get_stack())

# Add a file
bucketObject = s3.BucketObject(
    'index.html',
    bucket=bucket.id,
    source=pulumi.FileAsset('www/index.html')
)

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
