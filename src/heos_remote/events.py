import asyncio
from dataclasses import dataclass
from enum import Enum
import logging
from typing import Callable

import evdev


class KeyState(Enum):
    """State of a key during an event."""
    up = "UP"
    down = "DOWN"


@dataclass
class KeyEvent:
    """Key press event."""
    key_code: str
    key_state: KeyState


class EventListener:
    """
    Abstract interface for event listeners, which listen for key events
    and pass the events on to a given callback.
    """

    async def listen(self, callback: Callable[[KeyEvent], None]):
        raise NotImplementedError()


class EvdevEventListener(EventListener):
    """
    EventListener for Linux that uses evdev to detect key events.
    """

    def __init__(self, device_path: str, wait_delay: float = 0.5):
        self.device_path = device_path
        self.wait_delay = wait_delay
        self.logger = logging.getLogger(__name__)

    async def listen(self, callback):
        while True:
            self.logger.info(f"Waiting for device {self.device_path}")
            device = await self._get_device()
            self.logger.info(f"Found device {self.device_path}, listening for events")

            try:
                await self._handle_key_events(device, callback=callback)
            except IOError:
                self.logger.warning(f"Lost device {self.device_path}")

    async def _get_device(self):
        device = None
        while device is None:
            try:
                device = evdev.InputDevice(self.device_path)
            except IOError:
                await asyncio.sleep(self.wait_delay)
        return device

    async def _handle_key_events(self, device, callback):
        while True:
            async for event in device.async_read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    categorized = evdev.categorize(event)

                    self.logger.debug(
                        f"Received event (code: {categorized.keycode}, state: {categorized.keystate})"
                        f" on device {device.path}"
                    )

                    key_codes = _flat_map(categorized.keycode)
                    key_state = self._parse_keystate(categorized.keystate)

                    for key_code in key_codes:
                        try:
                            callback(
                                KeyEvent(
                                    key_code=key_code,
                                    key_state=key_state,
                                )
                            )
                        except Exception as e:
                            self.logger.error(f"Encountered exception during callback: {e}")

    @staticmethod
    def _parse_keystate(keystate: evdev.events.KeyEvent) -> KeyState:
        mapping = {
            evdev.events.KeyEvent.key_down: KeyState.down,
            evdev.events.KeyEvent.key_up: KeyState.up,
        }
        return mapping[keystate]


def _flat_map(value):
    if isinstance(value, (list, tuple)):
        yield from value
    else:
        yield value
