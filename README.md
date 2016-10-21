# Generate a signed S3 url
```
USE CASES:
   Generate signed S3 urls to share them in a short time to someone.

USAGE:
    ./s3-signed-url.py -u {PATH} -t {EXPIRY_TIME_IN_SECOND}
    ./s3-signed-url.py -u {PATH}

DESCRIPTION:
    -u    --url             The url of the s3 object (absolute or relative is fine)
    -t    --time            Expiry time in second. Default: 1 hour

EXAMPLES:
    If the link of your s3 object is:
    https://s3-ap-southeast-1.amazonaws.com/devops/share/share.zip
    And we want to share in 1 min:
    ------------------------------------------------------------
    ./s3-signed-url.py -u devops/share/share.zip -t 60
    ./s3-signed-url.py -u https://s3-ap-southeast-1.amazonaws.com/devops/share/share.zip -t 60
    ------------------------------------------------------------

NOTE:
    You must set AWS credentials in environment variables
    export AWS_ACCESS_KEY_ID=xxx
    export AWS_SECRET_ACCESS_KEY=xxx

```

# Bash:
```bash
./s3-signed-url.py -u devops/share/share.zip -t 600  
```
or

```bash
./s3-signed-url.py -u https://s3-ap-southeast-1.amazonaws.com/devops/share/share.zip -t 600
```

# Output
```
Bucket: devops
Object: share/share.zip
Signed url: -------------------------->
http://devops.s3.amazonaws.com/share/share.zip?AWSAccessKeyId=AKIAJOZ5UPG3QQ22TXYQ&Expires=1476959854&Signature=bpeuTv3Adz4g5HDm0ZtgmoDma38%3D
```
