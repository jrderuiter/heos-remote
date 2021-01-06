
class Command:

    def __call__(self):
        return self.run()

    def run(self):
        raise NotImplementedError()

    def __str__(self):
        return f"{self.__class__.__name__}()"


class IncreaseVolume(Command):

    def __init__(self, player_or_group, step_size=2):
        self.player_or_group = player_or_group
        self.step_size = step_size

    def run(self):
        self.player_or_group.volume += self.step_size

    def __str__(self):
        return f"{self.__class__.__name__}(step_size={self.step_size})"


class DecreaseVolume(Command):

    def __init__(self, player_or_group, step_size=2):
        self.player_or_group = player_or_group
        self.step_size = step_size

    def run(self):
        self.player_or_group.volume -= self.step_size

    def __str__(self):
        return f"{self.__class__.__name__}(step_size={self.step_size})"


class ToggleMute(Command):

    def __init__(self, player_or_group):
        self.player_or_group = player_or_group

    def run(self):
        self.player_or_group.mute = not self.player_or_group.mute


class TogglePlay(Command):

    def __init__(self, player_or_group):
        self.player_or_group = player_or_group

    def run(self):
        self.player_or_group.toggle_play()


class PlayNext(Command):

    def __init__(self, player_or_group):
        self.player_or_group = player_or_group

    def run(self):
        self.player_or_group.play_next()


class PlayPrevious(Command):

    def __init__(self, player_or_group):
        self.player_or_group = player_or_group

    def run(self):
        self.player_or_group.play_previous()
