"""KNX Websocket API."""
from __future__ import annotations

from typing import Callable

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
import voluptuous as vol
from xknx.telegram import Telegram
from xknx.telegram.apci import GroupValueRead, GroupValueResponse, GroupValueWrite

from .const import KNX_DOMAIN, AsyncMessageCallbackType, MessageCallbackType


def register_websocket_api(hass: HomeAssistant) -> None:
    """Register the KNX Websocket API."""
    websocket_api.async_register_command(hass, ws_info)
    websocket_api.async_register_command(hass, ws_subscribe_telegram)


@websocket_api.websocket_command(
    {
        vol.Required("type"): "knx_panel/info",
    }
)
@websocket_api.async_response
async def ws_info(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict,
) -> None:
    """Handle get info command."""
    xknx = hass.data[KNX_DOMAIN].xknx
    connection.send_result(
        msg["id"],
        {
            "version": xknx.version,
            "connected": xknx.connection_manager.connected.is_set(),
            "current_address": str(xknx.current_address),
        },
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "knx_panel/subscribe_telegrams",
    }
)
@websocket_api.async_response
async def ws_subscribe_telegram(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict,
) -> None:
    """Handle get info command."""

    async def forward_telegrams(telegram: Telegram):
        """Forward events to websocket."""
        if not isinstance(
            telegram.payload, (GroupValueRead, GroupValueWrite, GroupValueResponse)
        ):
            return

        connection.send_message(
            websocket_api.event_message(
                msg["id"],
                {
                    "destination_address": str(telegram.destination_address),
                    "payload": str(telegram.payload.value)
                    if hasattr(telegram.payload, "value")
                    else "",
                    "type": str(telegram.payload.__class__.__name__),
                    "source_address": str(telegram.source_address),
                    "direction": str(telegram.direction),
                    "timestamp": str(telegram.timestamp),
                },
            )
        )

    connection.subscriptions[msg["id"]] = await async_subscribe_telegrams(
        hass, forward_telegrams
    )

    connection.send_message(websocket_api.result_message(msg["id"]))


async def async_subscribe_telegrams(
    hass: HomeAssistant, callback: AsyncMessageCallbackType | MessageCallbackType
) -> Callable[[], None]:
    """Subscribe to telegram received callback."""
    xknx = hass.data[KNX_DOMAIN].xknx

    unregister = xknx.telegram_queue.register_telegram_received_cb(
        callback, match_for_outgoing=True
    )

    def async_remove():
        """Remove callback."""
        xknx.telegram_queue.unregister_telegram_received_cb(unregister)

    return async_remove
