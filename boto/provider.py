# Copyright (c) 2010 Mitch Garnaat http://garnaat.org/
# Copyright 2010 Google Inc.
# Copyright (c) 2010, Eucalyptus Systems, Inc.
# Copyright (c) 2011, Nexenta Systems Inc.
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
"""
This class encapsulates the provider-specific header differences.
"""

import os
import boto
from boto import config
from boto.gs.acl import ACL
from boto.gs.acl import CannedACLStrings as CannedGSACLStrings
from boto.s3.acl import CannedACLStrings as CannedS3ACLStrings
from boto.s3.acl import Policy

HEADER_PREFIX_KEY = 'header_prefix'
METADATA_PREFIX_KEY = 'metadata_prefix'

AWS_HEADER_PREFIX = 'x-amz-'
GOOG_HEADER_PREFIX = 'x-goog-'

ACL_HEADER_KEY = 'acl-header'
AUTH_HEADER_KEY = 'auth-header'
COPY_SOURCE_HEADER_KEY = 'copy-source-header'
COPY_SOURCE_VERSION_ID_HEADER_KEY = 'copy-source-version-id-header'
COPY_SOURCE_RANGE_HEADER_KEY = 'copy-source-range-header'
DELETE_MARKER_HEADER_KEY = 'delete-marker-header'
DATE_HEADER_KEY = 'date-header'
METADATA_DIRECTIVE_HEADER_KEY = 'metadata-directive-header'
RESUMABLE_UPLOAD_HEADER_KEY = 'resumable-upload-header'
SECURITY_TOKEN_HEADER_KEY = 'security-token-header'
STORAGE_CLASS_HEADER_KEY = 'storage-class'
MFA_HEADER_KEY = 'mfa-header'
SERVER_SIDE_ENCRYPTION_KEY = 'server-side-encryption-header'
VERSION_ID_HEADER_KEY = 'version-id-header'

STORAGE_COPY_ERROR = 'StorageCopyError'
STORAGE_CREATE_ERROR = 'StorageCreateError'
STORAGE_DATA_ERROR = 'StorageDataError'
STORAGE_PERMISSIONS_ERROR = 'StoragePermissionsError'
STORAGE_RESPONSE_ERROR = 'StorageResponseError'


class Provider(object):

    CredentialMap = {
        'aws' : ('aws_access_key_id', 'aws_secret_access_key'),
        'google' : ('gs_access_key_id', 'gs_secret_access_key'),
    }

    AclClassMap = {
        'aws' : Policy,
        'google' : ACL
    }

    CannedAclsMap = {
        'aws' : CannedS3ACLStrings,
        'google' : CannedGSACLStrings
    }

    HostKeyMap = {
        'aws' : 's3',
        'google' : 'gs'
    }

    ChunkedTransferSupport = {
        'aws' : False,
        'google' : True
    }

    # If you update this map please make sure to put "None" for the
    # right-hand-side for any headers that don't apply to a provider, rather
    # than simply leaving that header out (which would cause KeyErrors).
    HeaderInfoMap = {
        'aws' : {
            HEADER_PREFIX_KEY : AWS_HEADER_PREFIX,
            METADATA_PREFIX_KEY : AWS_HEADER_PREFIX + 'meta-',
            ACL_HEADER_KEY : AWS_HEADER_PREFIX + 'acl',
            AUTH_HEADER_KEY : 'AWS',
            COPY_SOURCE_HEADER_KEY : AWS_HEADER_PREFIX + 'copy-source',
            COPY_SOURCE_VERSION_ID_HEADER_KEY : AWS_HEADER_PREFIX +
                                                'copy-source-version-id',
            COPY_SOURCE_RANGE_HEADER_KEY : AWS_HEADER_PREFIX +
                                           'copy-source-range',
            DATE_HEADER_KEY : AWS_HEADER_PREFIX + 'date',
            DELETE_MARKER_HEADER_KEY : AWS_HEADER_PREFIX + 'delete-marker',
            METADATA_DIRECTIVE_HEADER_KEY : AWS_HEADER_PREFIX +
                                            'metadata-directive',
            RESUMABLE_UPLOAD_HEADER_KEY : None,
            SECURITY_TOKEN_HEADER_KEY : AWS_HEADER_PREFIX + 'security-token',
            SERVER_SIDE_ENCRYPTION_KEY : AWS_HEADER_PREFIX + 'server-side-encryption',
            VERSION_ID_HEADER_KEY : AWS_HEADER_PREFIX + 'version-id',
            STORAGE_CLASS_HEADER_KEY : AWS_HEADER_PREFIX + 'storage-class',
            MFA_HEADER_KEY : AWS_HEADER_PREFIX + 'mfa',
        },
        'google' : {
            HEADER_PREFIX_KEY : GOOG_HEADER_PREFIX,
            METADATA_PREFIX_KEY : GOOG_HEADER_PREFIX + 'meta-',
            ACL_HEADER_KEY : GOOG_HEADER_PREFIX + 'acl',
            AUTH_HEADER_KEY : 'GOOG1',
            COPY_SOURCE_HEADER_KEY : GOOG_HEADER_PREFIX + 'copy-source',
            COPY_SOURCE_VERSION_ID_HEADER_KEY : GOOG_HEADER_PREFIX +
                                                'copy-source-version-id',
            COPY_SOURCE_RANGE_HEADER_KEY : None,
            DATE_HEADER_KEY : GOOG_HEADER_PREFIX + 'date',
            DELETE_MARKER_HEADER_KEY : GOOG_HEADER_PREFIX + 'delete-marker',
            METADATA_DIRECTIVE_HEADER_KEY : GOOG_HEADER_PREFIX  +
                                            'metadata-directive',
            RESUMABLE_UPLOAD_HEADER_KEY : GOOG_HEADER_PREFIX + 'resumable',
            SECURITY_TOKEN_HEADER_KEY : GOOG_HEADER_PREFIX + 'security-token',
            SERVER_SIDE_ENCRYPTION_KEY : None,
            # Note that this version header is not to be confused with
            # the Google Cloud Storage 'x-goog-api-version' header.
            VERSION_ID_HEADER_KEY : GOOG_HEADER_PREFIX + 'version-id',
            STORAGE_CLASS_HEADER_KEY : None,
            MFA_HEADER_KEY : None,
        }
    }

    ErrorMap = {
        'aws' : {
            STORAGE_COPY_ERROR : boto.exception.S3CopyError,
            STORAGE_CREATE_ERROR : boto.exception.S3CreateError,
            STORAGE_DATA_ERROR : boto.exception.S3DataError,
            STORAGE_PERMISSIONS_ERROR : boto.exception.S3PermissionsError,
            STORAGE_RESPONSE_ERROR : boto.exception.S3ResponseError,
        },
        'google' : {
            STORAGE_COPY_ERROR : boto.exception.GSCopyError,
            STORAGE_CREATE_ERROR : boto.exception.GSCreateError,
            STORAGE_DATA_ERROR : boto.exception.GSDataError,
            STORAGE_PERMISSIONS_ERROR : boto.exception.GSPermissionsError,
            STORAGE_RESPONSE_ERROR : boto.exception.GSResponseError,
        }
    }

    def __init__(self, name, access_key=None, secret_key=None,
                 security_token=None):
        self.host = None
        self.access_key = access_key
        self.secret_key = secret_key
        self.security_token = security_token
        self.name = name
        self.acl_class = self.AclClassMap[self.name]
        self.canned_acls = self.CannedAclsMap[self.name]
        self.get_credentials(access_key, secret_key)
        self.configure_headers()
        self.configure_errors()
        # allow config file to override default host
        host_opt_name = '%s_host' % self.HostKeyMap[self.name]
        if config.has_option('Credentials', host_opt_name):
            self.host = config.get('Credentials', host_opt_name)

    def get_credentials(self, access_key=None, secret_key=None):
        access_key_name, secret_key_name = self.CredentialMap[self.name]
        if access_key is not None:
            self.access_key = access_key
        elif access_key_name.upper() in os.environ:
            self.access_key = os.environ[access_key_name.upper()]
        elif config.has_option('Credentials', access_key_name):
            self.access_key = config.get('Credentials', access_key_name)

        if secret_key is not None:
            self.secret_key = secret_key
        elif secret_key_name.upper() in os.environ:
            self.secret_key = os.environ[secret_key_name.upper()]
        elif config.has_option('Credentials', secret_key_name):
            self.secret_key = config.get('Credentials', secret_key_name)
        if isinstance(self.secret_key, unicode):
            # the secret key must be bytes and not unicode to work
            #  properly with hmac.new (see http://bugs.python.org/issue5285)
            self.secret_key = str(self.secret_key)

    def configure_headers(self):
        header_info_map = self.HeaderInfoMap[self.name]
        self.metadata_prefix = header_info_map[METADATA_PREFIX_KEY]
        self.header_prefix = header_info_map[HEADER_PREFIX_KEY]
        self.acl_header = header_info_map[ACL_HEADER_KEY]
        self.auth_header = header_info_map[AUTH_HEADER_KEY]
        self.copy_source_header = header_info_map[COPY_SOURCE_HEADER_KEY]
        self.copy_source_version_id = header_info_map[
            COPY_SOURCE_VERSION_ID_HEADER_KEY]
        self.copy_source_range_header = header_info_map[
            COPY_SOURCE_RANGE_HEADER_KEY]
        self.date_header = header_info_map[DATE_HEADER_KEY]
        self.delete_marker = header_info_map[DELETE_MARKER_HEADER_KEY]
        self.metadata_directive_header = (
            header_info_map[METADATA_DIRECTIVE_HEADER_KEY])
        self.security_token_header = header_info_map[SECURITY_TOKEN_HEADER_KEY]
        self.resumable_upload_header = (
            header_info_map[RESUMABLE_UPLOAD_HEADER_KEY])
        self.server_side_encryption_header = header_info_map[SERVER_SIDE_ENCRYPTION_KEY]
        self.storage_class_header = header_info_map[STORAGE_CLASS_HEADER_KEY]
        self.version_id = header_info_map[VERSION_ID_HEADER_KEY]
        self.mfa_header = header_info_map[MFA_HEADER_KEY]

    def configure_errors(self):
        error_map = self.ErrorMap[self.name]
        self.storage_copy_error = error_map[STORAGE_COPY_ERROR]
        self.storage_create_error = error_map[STORAGE_CREATE_ERROR]
        self.storage_data_error = error_map[STORAGE_DATA_ERROR]
        self.storage_permissions_error = error_map[STORAGE_PERMISSIONS_ERROR]
        self.storage_response_error = error_map[STORAGE_RESPONSE_ERROR]

    def get_provider_name(self):
        return self.HostKeyMap[self.name]

    def supports_chunked_transfer(self):
        return self.ChunkedTransferSupport[self.name]

# Static utility method for getting default Provider.
def get_default():
    return Provider('aws')
