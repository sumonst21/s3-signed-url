#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: khoa.le@hrboss.com

from __future__ import print_function
import base64
import hmac
import sha
import urllib
import time
import os
import argparse

HELP = """
Generate a signed S3 url

USE CASES:
   Generate signed S3 urls to share them in a short time to someone.

USAGE:
    ./s3-signed-url.py -p {PATH} -t {EXPIRY_TIME_IN_SECOND}
    ./s3-signed-url.py -p {PATH}

DESCRIPTION:
    -p    --path            The path of the s3 object (include S3 Bucket)
    -t    --time            Expiry time in second. Default: 1 hour

EXAMPLES:
    If the link of your s3 object is:
    https://s3-ap-southeast-1.amazonaws.com/devops/share/share.zip
    And we want to share in 1 min:
    ------------------------------------------------------------
    ./s3-signed-url.py -p devops/share/share.zip -t 60
    ------------------------------------------------------------

NOTE:
    You must set AWS credentials in environment variables
    export AWS_ACCESS_KEY_ID=xxx
    export AWS_SECRET_ACCESS_KEY=xxx

"""


def getenv(env_var):
    """Get environment variable

    Args:
        env_var (string) -- the environment variable you want to get
    Returns:
        string: -- the value of the environment variable
    """

    if env_var in os.environ:
        return os.environ[env_var]
    else:
        print ('ERROR! no env_var: %s. Run "source .env" to activate environment variables' % env_var)
        exit(1)


def get_s3_signed_url(path, expire):
    """Get signed url from a s3 path and time to expire

    Args:
      path (string): -- the s3 path in format BUCKET/OBJECT
      expire (int): --  available in seconds
    Returns:
      string: -- the s3 signed url
    """
    aws_access_key_id = getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = getenv('AWS_SECRET_ACCESS_KEY')

    bucket = path.split('/')[0]
    obj = '/'.join(path.split('/')[1:])
    print('Bucket:', bucket)
    print('Object:', obj)

    # Expiry Timestamp
    expiry_ts = int(time.time()) + expire
    h = hmac.new(aws_secret_access_key,
                 "GET\n\n\n%d\n/%s/%s" % (expiry_ts, bucket, obj),
                 sha)

    # Signature
    sig = urllib.quote_plus(base64.encodestring(h.digest()).strip())

    signed_url = 'http://%s.s3.amazonaws.com/%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' \
                 % (bucket, obj, aws_access_key_id, expiry_ts, sig)

    return signed_url


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p',
                        help='The path of the s3 object (include S3 Bucket)')
    parser.add_argument('--time', '-t',
                        help='Expiry time in second. Default: 1 hour')
    args = parser.parse_args()

    if args.path is None:
        print(HELP)
        exit(1)
    else:
        path = args.path.strip()

    if path[0] == '/':
        path = path[1:]

    if args.time is None:
        expire = 60 * 60  # 1 hour
    else:
        expire = int(args.time)

    signed_url = get_s3_signed_url(path, expire)

    print('Signed url: -------------------------->')
    print(signed_url)
