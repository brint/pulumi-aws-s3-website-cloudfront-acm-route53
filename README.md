# pulumi-aws-s3-website-cloudfront-acm-route53

Playing with Pulumi to learn it. Making an equivalent of [terraform-aws-s3-website-cloudfront-acm-route53](https://github.com/brint/terraform-aws-s3-website-cloudfront-acm-route53).

## Setup (OSX)

Using homebrew for install of pulumi and virtualenv (since that's what pulumi uses when using the CLI) for managing the local python environment. Pulumi requires Python 3.6+.

```
brew install pulumi
virtualenv -p python3.9 venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pulumi up
```

## Switching between environments

```
pulumi stack select dev
pulumi stack select prod
```
