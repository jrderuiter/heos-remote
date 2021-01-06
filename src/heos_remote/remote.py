import asyncio
from collections import defaultdict
import logging
from typing import List, Union

from . import commands
from .events import EventListener, KeyEvent, KeyState
from .player import Player, PlayerGroup


class Remote:
    """
    Remote interface class, which listens to events from EventListeners
    and responds to the received events. Subclasses should override the
    'handle_event' method to implement the desired behavior.
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def handle_event(self, event: KeyEvent):
        """Handles a given key event."""
        raise NotImplementedError()

    def start(self, listeners: List[EventListener]):
        """Starts an event loop that handles events from the given listeners."""
        for listener in listeners:
            asyncio.ensure_future(listener.listen(self.handle_event))

        loop = asyncio.get_event_loop()
        loop.run_forever()


class PlayerRemote(Remote):
    """
    Basic remote implementation that relays presses from pre-defined keys
    to basic player commands.
    """

    # TODO: Make keys configurable?

    def __init__(self, player_or_group: Union[Player, PlayerGroup]):
        super().__init__()
        self._commands = defaultdict(dict)
        self._register_commands(player_or_group)

    def _register_commands(self, player_or_group):
        self._add_command("KEY_VOLUMEUP", KeyState.down, commands.IncreaseVolume(player_or_group))
        self._add_command("KEY_VOLUMEDOWN", KeyState.down, commands.DecreaseVolume(player_or_group))
        self._add_command("KEY_MUTE", KeyState.down, commands.ToggleMute(player_or_group))
        self._add_command("KEY_NEXTSONG", KeyState.down, commands.PlayNext(player_or_group))
        self._add_command("KEY_PREVIOUSSONG", KeyState.down, commands.PlayPrevious(player_or_group))
        self._add_command("KEY_PLAYPAUSE", KeyState.down, commands.TogglePlay(player_or_group))

    def _add_command(self, key_code: str, key_state: KeyState, command: commands.Command):
        self._commands[key_code][key_state] = command

    def handle_event(self, event: KeyEvent):
        command = self._commands[event.key_code].get(event.key_state)

        if command is not None:
            self._logger.info(
                f"Running command {command} for event {event}"
            )
            command.run()
        else:
            self._logger.debug(f"No command found for event {event}")
