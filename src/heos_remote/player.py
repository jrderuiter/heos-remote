from heos import Registry, Player, PlayerGroup


def get_player(name: str, rediscover: bool = False) -> Player:
    """Fetches a player with the given name."""

    registry = Registry()

    if rediscover:
        registry.discover()

    try:
        player = registry.players[name]
    except KeyError:
        raise PlayerNotFoundError(
            f"Unknown player '{name}', available players "
            f"are: {list(registry.players.keys())}"
        ) from None

    return player


class PlayerNotFoundError(Exception):
    pass


def get_group(name: str, rediscover: bool = False) -> PlayerGroup:
    """Fetches a player group with the given name."""
    registry = Registry()

    if rediscover:
        registry.discover()

    try:
        group = registry.groups[name]
    except KeyError:
        raise GroupNotFoundError(
            f"Unknown group '{name}', available group "
            f"are: {list(registry.group.keys())}"
        ) from None

    return group


class GroupNotFoundError(Exception):
    pass
