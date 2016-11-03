#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: khoa.le@hrboss.com

from __future__ import print_function
import base64
try:
    from Crypto.Hash import SHA, HMAC
except ImportError:
    print('You need to install pyscrypto library:')
    print('pip install pycrypto')
    exit(1)

import time
import os
import argparse
import urllib
try:
    from urllib.parse import quote as quote_plus
except ImportError:
    from urllib import quote_plus

HELP = """
Generate a signed S3 url

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
    - You need to install pyscrypto library:
    pip install pycrypto

    - You must set AWS credentials in environment variables
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
        print('ERROR! no env_var: %s. Run "source .env" to activate environment variables' % env_var)
        exit(1)


def parse_bucket_obj(path):
    """Get bucket, obj from a s3 path/url

    Args:
      path (string): -- the s3 url (absolute or relative is fine)
    Returns:
      (bucket, obj) (tuple): -- the bucket and object key path
    """

    path = path.strip()
    pos_com = path.find('.com/')
    if pos_com > 0:  # full url https://s3-ap-southeast-1.amazonaws.com/devops/share/share.zip
        path = path[pos_com + 5:]

    if path[0] == '/':
        path = path[1:]

    bucket = path.split('/')[0]
    obj = '/'.join(path.split('/')[1:])

    print('Bucket:', bucket)
    print('Object:', obj)

    return bucket, obj


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

    bucket, obj = parse_bucket_obj(path)
    # Expiry Timestamp
    expiry_ts = int(time.time()) + expire
    h = HMAC.new(bytes(aws_secret_access_key.encode('utf-8')),
                 ("GET\n\n\n%d\n/%s/%s" % (expiry_ts, bucket, obj)).encode('utf-8'),
                 SHA)

    # Signature
    sig = quote_plus(base64.encodestring(h.digest()).strip().decode('utf-8'))

    signed_url = 'http://%s.s3.amazonaws.com/%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' \
                 % (bucket, quote_plus(obj), aws_access_key_id, expiry_ts, sig)

    return signed_url


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u',
                        help='The s3 url (absolute or relative is fine)')
    parser.add_argument('--time', '-t',
                        help='Expiry time in second. Default: 1 hour')
    args = parser.parse_args()

    if args.url is None:
        print(HELP)
        exit(1)
    else:
        path = args.url.strip()

    if args.time is None:
        expire = 60 * 60  # 1 hour
    else:
        expire = int(args.time)

    signed_url = get_s3_signed_url(path, expire)

    print('Signed url: -------------------------->')
    print(signed_url)
