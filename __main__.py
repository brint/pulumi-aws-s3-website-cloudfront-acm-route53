"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
from pulumi_aws import s3

# For pulling config options
config = pulumi.Config()
domain = config.require("domain")

# Standard tags for all resources in the stack
stack_tags = {
    "Environment": pulumi.get_stack(),
    "Region": aws.get_region().name,
    "Project": domain,
    "Orchestrator": "pulumi"
}
# Create an AWS resource (S3 Bucket)
# Use the stack, which is the environment name for
# bucket naming.
bucket = s3.Bucket('%s.%s.%s' % (aws.get_region().name, pulumi.get_stack(), domain), acl="private", tags=stack_tags)

# Add a file
bucketObject = s3.BucketObject(
    'index.html',
    bucket=bucket.id,
    source=pulumi.FileAsset('www/index.html')
)

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
