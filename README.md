# Generate a signed S3 url

USE CASES:  
   Generate signed S3 urls to share them in a short time to someone.  
  
USAGE:  
    ./s3-signed-url.py -p {PATH} -t {EXPIRY_TIME_IN_SECOND}  
    ./s3-signed-url.py -p {PATH}   
  
DESCRIPTION:  
    -p    --path            The path of the s3 object (include S3 Bucket)  
    -t    --time            Expiry time in second. Default: 1 hour  
  
EXAMPLES:  
    If the link of your s3 object is https://s3-ap-southeast-1.amazonaws.com/devops/share/share.zip  
    ------------------------------------------------------------  
    ./s3-signed-url.py -p devops/share/share.zip -t 60  
    ------------------------------------------------------------  
  
NOTE:  
    You must set AWS credentials in environment variables  
    export AWS_ACCESS_KEY_ID=xxx  
    export AWS_SECRET_ACCESS_KEY=xxx
