"""An AWS Python Pulumi program"""
import os

import pulumi
import pulumi_aws as aws
from pulumi_aws import s3

# For pulling config options
config = pulumi.Config()
domain = config.require("domain")
site_contents = config.require("pathToWebsiteContents")

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
bucket = s3.Bucket('%s.%s.%s' % (aws.get_region().name,
                                 pulumi.get_stack(),
                                 domain),
                   acl="private",
                   tags=stack_tags)

logging_bucket = s3.Bucket('%s.%s.%s-logs' % (aws.get_region().name,
                                 pulumi.get_stack(),
                                 domain),
                   acl="private",
                   tags=stack_tags)

# Add a file
bucketObject = s3.BucketObject(
    'index.html',
    bucket=bucket.id,
    source=pulumi.FileAsset(os.path.join(site_contents, 'index.html'))
)

# CloudFront distribution, basically strait from the docs
s3_origin_id = "%s.%s.%s" % (aws.get_region().name, pulumi.get_stack(), domain)
distribution_name = "%s.%s" % (pulumi.get_stack(), domain)
distribution_aliases = ["www.%s" % (distribution_name)]

s3_distribution = aws.cloudfront.Distribution(distribution_name,
    origins=[aws.cloudfront.DistributionOriginArgs(
        domain_name=bucket.bucket_regional_domain_name,
        origin_id=s3_origin_id,
        # TODO
        s3_origin_config=aws.cloudfront.DistributionOriginS3OriginConfigArgs(
            origin_access_identity="origin-access-identity/cloudfront/ABCDEFG1234567",
        ),
    )],
    enabled=True,
    is_ipv6_enabled=True,
    comment="Pulumim managed distribution",
    default_root_object="index.html",
    # TODO
    logging_config=aws.cloudfront.DistributionLoggingConfigArgs(
        include_cookies=False,
        bucket=logging_bucket.bucket_domain_name,
    ),
    aliases=distribution_aliases,
    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        allowed_methods=[
            "GET",
            "HEAD",
        ],
        cached_methods=[
            "GET",
            "HEAD",
        ],
        target_origin_id=s3_origin_id,
        forwarded_values=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs(
            query_string=False,
            cookies=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs(
                forward="none",
            ),
        ),
        viewer_protocol_policy="redirect-to-https",
        min_ttl=0,
        default_ttl=3600,
        max_ttl=86400,
    ),
    # Options: PriceClass_All, PriceClass_200, PriceClass_100 (Cheapest)
    price_class="PriceClass_100",
    restrictions=aws.cloudfront.DistributionRestrictionsArgs(
        geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type="none",
        ),
    ),
    tags=stack_tags,
    # TODO
    viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
        cloudfront_default_certificate=True,
    ))

### Exports
# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
