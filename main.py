import sys
from bot.DaBot import DaBot
from daemon.SimpleDaemon import Daemon


class DaBotDaemon(Daemon):
    def run(self):
        da = DaBot()
        da.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with DaBotDaemon('/tmp/daemon-dabot.pid', error_log_file='errlog.txt') as daemon:
        daemon.process_command()
        # da = DaBot()
        # da.run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
