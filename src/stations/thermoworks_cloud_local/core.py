"""Accessor for the Thermoworks Cloud API."""

import logging
from typing import List

from stations.thermoworks_cloud_local.utils import format_client_response

from .auth import Auth
from .models.device import Device, _document_to_device
from .models.device_channel import DeviceChannel, _document_to_device_channel
from .models.user import User, document_to_user

_LOGGER = logging.getLogger(__name__)


class ResourceNotFoundError(Exception):
    """Custom exception indicating that the requested resource could not be found."""

    def __init__(
        self,
        message: str,
    ) -> None:
        """Initialize the error."""

        super().__init__(message)
        self.message = message


class ThermoworksCloud:
    """Client for the Thermoworks Cloud service."""

    def __init__(self, auth: Auth) -> None:
        """Create a new client. `thermoworks_cloud.Auth` objects are created using a
        `thermoworks_cloud.AuthFactory`.

        Args:
            auth (Auth): Authorization object used to make authorized requests to the service.
        """
        self._auth = auth

    async def get_user(self) -> User:
        """Fetch information for the authenticated user."""

        response = await self._auth.request("get", f"documents/users/{self._auth.user_id}")
        if response.ok:
            user_document = await response.json()
            return document_to_user(user_document)

        if response.status == 404:
            raise ResourceNotFoundError("User not found")

        try:
            error_response = await format_client_response(response)
        except RuntimeError:
            error_response = "Could not read response body."

        raise RuntimeError(f"Failed to get user: {error_response}")

    async def get_device(self, device_serial: str) -> Device:
        """Fetch a device by serial number."""

        response = await self._auth.request("get", f"documents/devices/{device_serial}")
        if response.ok:
            device_document = await response.json()
            return _document_to_device(device_document)

        if response.status == 404:
            raise ResourceNotFoundError(f"Device with serial '{
                                        device_serial}'not found")

        try:
            error_response = await format_client_response(response)
        except RuntimeError:
            error_response = "Could not read response body."

        raise RuntimeError(f"Failed to get device: {error_response}")

    async def get_device_channel(
        self, device_serial: str, channel: str
    ) -> DeviceChannel:
        """Fetch channel information for a device."""

        response = await self._auth.request(
            "get", f"documents/devices/{device_serial}/channels/{channel}"
        )
        if response.ok:
            device_channel_document = await response.json()
            return _document_to_device_channel(device_channel_document)

        if response.status == 404:
            raise ResourceNotFoundError(
                f"Device channel with serial '{device_serial}' and channel '{
                    channel}' not found"
            )

        try:
            error_response = await format_client_response(response)
        except RuntimeError:
            error_response = "Could not read response body."

        raise RuntimeError(
            f"Failed to get device channel: {error_response}")

    async def get_devices(self, account_id: str) -> List[Device]:
        """Fetch devices for the authenticated user using Firestore query.

        It queries the Firestore 'devices' collection directly using the user's accountId.
        """

        # Build the Firestore query
        query_body = {
            "structuredQuery": {
                "from": [{"collectionId": "devices"}],
                "where": {
                    "fieldFilter": {
                        "field": {"fieldPath": "accountId"},
                        "op": "EQUAL",
                        "value": {"stringValue": account_id}
                    }
                },
                "orderBy": [{"field": {"fieldPath": "__name__"}, "direction": "ASCENDING"}]
            }
        }

        # Execute the query against Firestore REST API
        headers = {"Content-Type": "application/json"}
        response = await self._auth.request("post", "documents:runQuery",
                                            additional_headers=headers, json=query_body)

        if not response.ok:
            try:
                error_response = await format_client_response(response)
            except RuntimeError:
                error_response = "Could not read response body."
            raise RuntimeError(f"Failed to query devices: {error_response}")

        # Process the response
        result = await response.json()
        devices = []

        for item in result:
            if "document" in item:
                device = _document_to_device(item["document"])
                devices.append(device)

        return devices
