# Copyright (c) 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from platformio import __registry_api__
from platformio.clients.account import AccountClient
from platformio.clients.rest import RESTClient
from platformio.package.pack import PackageType


class RegistryClient(RESTClient):
    def __init__(self):
        super(RegistryClient, self).__init__(base_url=__registry_api__)

    def publish_package(
        self, archive_path, owner=None, released_at=None, private=False
    ):
        account = AccountClient()
        if not owner:
            owner = (
                account.get_account_info(offline=True).get("profile").get("username")
            )
        with open(archive_path, "rb") as fp:
            response = self.send_request(
                "post",
                "/v3/package/%s/%s" % (owner, PackageType.from_archive(archive_path)),
                params={"private": 1 if private else 0, "released_at": released_at},
                headers={
                    "Authorization": "Bearer %s" % account.fetch_authentication_token()
                },
                data=fp,
            )
            return response

    def unpublish_package(self, name, owner=None, version=None, undo=False):
        account = AccountClient()
        if not owner:
            owner = (
                account.get_account_info(offline=True).get("profile").get("username")
            )
        path = "/v3/package/%s/%s" % (owner, name)
        if version:
            path = path + "/version/" + version
        response = self.send_request(
            "delete",
            path,
            params={"undo": 1 if undo else 0},
            headers={
                "Authorization": "Bearer %s" % account.fetch_authentication_token()
            },
        )
        return response
