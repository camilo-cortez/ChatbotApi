from commands.base_command import BaseCommand

class Ping(BaseCommand):

    def execute(self):
        return 'pong'