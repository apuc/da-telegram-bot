"""Generic linux daemon base class for python 3.x."""

import sys, os, time, atexit, signal, logging


class Daemon:
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method."""

    def __init__(self, pidfile, error_log_file='/dev/null'):
        self.logging = logging
        self.logging.basicConfig(filename=error_log_file, filemode='w',
                                 format='%(name)s - %(levelname)s - %(message)s\n')
        self.logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        self.error_log_file = error_log_file
        self.pidfile = pidfile
        self.commands = {}

    def __enter__(self):
        self.base_commands()
        self.reg_command()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            self.logging.error('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            self.logging.error('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon."""
        self.logging.info("Start")

        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pf:

                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pidfile {0} already exist. " + \
                      "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            self.logging.error(message.format(self.pidfile))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""
        self.logging.info("Stop")

        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pidfile {0} does not exist. " + \
                      "Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            self.logging.error(message.format(self.pidfile))
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.logging.info("Restart")
        self.stop()
        self.start()

    def status(self):
        print("Status")
        try:
            with open(self.pidfile, 'r') as pf:

                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            print("Process started, pid %d" % pid)
        else:
            print("Process is not running")

    def console_stdout(self):
        sys.stdout = sys.__stdout__
        print(123)

    def process_command(self):
        if len(sys.argv) > 1:
            command = sys.argv[1]
            handler = self.get_command_handler(command)
            if handler:
                handler()
            else:
                print("Unknown command: %s" % command)
        else:
            print("usage: %s start|stop|restart|status" % sys.argv[0])
            sys.exit(2)

    def base_commands(self):
        self.add_command('start', self.start)
        self.add_command('stop', self.stop)
        self.add_command('restart', self.restart)
        self.add_command('status', self.status)
        self.add_command('console_stdout', self.console_stdout)

    def add_command(self, command, handler):
        if command not in self.commands:
            self.commands[command] = handler

    def get_command_handler(self, command):
        if command in self.commands:
            return self.commands[command]

        return None

    def reg_command(self):
        pass

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart()."""
