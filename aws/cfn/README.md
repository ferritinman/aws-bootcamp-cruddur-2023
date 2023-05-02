## Architecture Guide

Before you run any tempaltes, but sure to create an S3 bucket to contain all
of our artifacts for CloudFormation

```
aws s3 mk s3://cfn-artifacts-ferritinman
export CFN_BUCKET="cfn-artifacts-ferritinman"
gp env CFN_BUCKET="cfn-artifacts-ferritinman"
```