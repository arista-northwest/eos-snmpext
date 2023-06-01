# -*- coding: utf-8 -*-
# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""Simple EAPI Client

API Usage:

import eapiclient

session = eapi.Session(<hostaddr>, auth=(admin, ""))
resp = session.call(["show version"])

print(resp)

"""

import argparse
import http.client
import json
import socket
import urllib.parse
import uuid

from base64 import b64encode
from typing import Tuple, Optional

# Default timeout
TIMEOUT = 30.0

# Default and username password
DEFAULT_AUTH = ("admin", "")

# Specifies the default result encoding.  The alternative is 'text'
DEFAULT_ENCODING = "json"

# Default transport is http; https, unix or http+unix are also supported
DEFAULT_TRANSPORT = "http"  

# Specifies whether to add timestamps for each command by default
INCLUDE_TIMESTAMPS = False

# Set this to false to skip checking hostname
SSL_VERIFY = True


def encode_auth(auth: Tuple[str, str]) -> str:
    # encode the auth tuple for HTTP basic auth
    return b64encode(":".join(auth).encode("utf-8")).decode("ascii")


# See: https://github.com/msabramo/requests-unixsocket/blob/master/requests_unixsocket/adapters.py#L19
class UnixHTTPConnection(http.client.HTTPConnection):

    def __init__(self, path, timeout=60):
        """Create an HTTP connection to a unix domain socket
        """
        super(UnixHTTPConnection, self).__init__('localhost', timeout=timeout)
        self.path = path
        self.timeout = timeout
        self.sock = None

    def __del__(self):  # base class does not have d'tor
        if self.sock:
            self.sock.close()

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.path)
        self.sock = sock


class Session(object):
    """EAPI Session"""
    # pylint: disable=R0913,R0902

    def __init__(self,
                 target: str,
                 auth: Tuple[str, str] = DEFAULT_AUTH,
                 cert: Optional[str] = None,
                 key: Optional[str] = None,
                 timeout: float = TIMEOUT,
                 verify: bool = SSL_VERIFY):

        self._session = None

        parsed = urllib.parse.urlparse(target)

        hostname = parsed.hostname or "localhost"

        if not parsed.scheme:
            path = parsed.path
            port = 80

            if ":" in parsed.path:
                path, port_ = parsed.path.split(":", 2)
                port = int(port_)

            self._session = http.client.HTTPConnection(path, port, timeout)

        elif parsed.scheme == 'http':
            self._session = http.client.HTTPConnection(
                hostname, parsed.port, timeout)
        elif parsed.scheme == 'https' or cert:
            self._session = http.client.HTTPSConnection(hostname, parsed.port,
                                                        key_file=key,
                                                        cert_file=cert,
                                                        timeout=timeout,
                                                        check_hostname=verify)
        elif parsed.scheme in ('unix', 'http+unix'):
            self._session = UnixHTTPConnection(parsed.path, timeout=timeout)
        else:
            raise ValueError(f"Unknown scheme: {parsed.scheme}")

        userpass = encode_auth(auth)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {userpass}"
        }

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """shutdown the session"""
        self._session.close()

    def call(self, commands: list, encoding: str = DEFAULT_ENCODING,
             timestamps: bool = INCLUDE_TIMESTAMPS) -> dict:
        """Send commands to switch"""

        request_id = str(uuid.uuid4())

        params = {
            "version": 1,
            "cmds": commands,
            "format": encoding
        }

        # timestamps is a newer param, only include it if requested
        if timestamps:
            params["timestamps"] = timestamps

        payload = {
            "jsonrpc": "2.0",
            "method": "runCmds",
            "params": params,
            "id": request_id
        }

        self._session.request('POST', "/command-api",
                              body=json.dumps(payload), headers=self.headers)
        resp = self._session.getresponse()

        if resp.status != 200:
            raise ValueError(f"There was an error: {resp.status} {resp.reason}")

        return json.loads(resp.read())


def call(hostaddr: str,
         commands,
         auth: Tuple[str, str] = DEFAULT_AUTH,
         encoding: str = DEFAULT_ENCODING,
         timestamps: bool = INCLUDE_TIMESTAMPS,
         cert: Optional[str] = None,
         key: Optional[str] = None,
         timeout: float = TIMEOUT,
         verify: bool = SSL_VERIFY) -> dict:

    with Session(hostaddr, auth, cert, key, timeout, verify) as sess:
        resp = sess.call(commands, encoding, timestamps)

    return resp


def parse_args():
    parser = argparse.ArgumentParser("eapicli")
    parser.add_argument("target", type=str, default="http+unix:///var/run/command-api.sock",
                        help="Target URI accepts schemes: http(s)?://... or unix://...")
    parser.add_argument("-u", "--username", default="admin",
                        help="user name for authentication")
    parser.add_argument("-p", "--password", default="",
                        help="password for authentication")
    parser.add_argument("-e", "--encoding", default="json",
                        choices=["json", "text"])
    parser.add_argument("--cert", help="path to client certificate file")
    parser.add_argument("--key", help="path to private key")
    parser.add_argument("--verify", action="store_true",
                        default=True, help="verify hostname")
    parser.add_argument("--timeout", type=int)

    return parser.parse_args()


# def main():
#     args = parse_args()
#     commands = []
#     for line in sys.stdin:
#         commands.append(line)

#     print(call(args.target, commands, auth=(args.username, args.password),
#                encoding=args.encoding, timestamps=False, cert=args.cert,
#                key=args.key, timeout=args.timeout))


# if __name__ == "__main__":
#     main()