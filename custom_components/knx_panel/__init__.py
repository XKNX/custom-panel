"""Custom panel for KNX."""
from .websocket import register_websocket_api


async def async_setup(hass, config):
    """Set up this integration using yaml."""
    url = "/api/panel_custom/knx_ui"
    location = hass.config.path("custom_components/knx_panel/knx_ui.js")
    hass.http.register_static_path(url, location)
    hass.components.frontend.async_register_built_in_panel(
        component_name="custom",
        sidebar_title="KNX UI",
        sidebar_icon="mdi:earth",
        frontend_url_path="knx_ui",
        config={
            "_panel_custom": {
                "name": "knx-custom-panel",
                "embed_iframe": False,
                "trust_external": False,
                "js_url": url,
            }
        },
        require_admin=True,
    )

    register_websocket_api(hass)

    return True
