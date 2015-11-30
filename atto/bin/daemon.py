#!/usr/bin/env python

import sys, os, time, atexit
from signal import SIGTERM 
import logging

import util

logger = logging.getLogger()

class Daemon:
    """ A generic daemon class.
    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pidfile, config_file=None, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.config_file = config_file
        if os.path.exists(config_file) and os.path.isfile(config_file):
            self.config_file_stats = os.stat(config_file)
        else:
            logger.critical("Config file couldn't be found: %s", config_file)
            raise IOError("Config file couldn't be found: %s" % (config_file) )
        self.config = {}
        self.check_config()
    
    def check_config(self):
        stats = os.stat(self.config_file)
        if len(self.config.keys()) == 0:
            logger.info("Loading Config: %s", self.config_file)
            self.load_config()
        elif self.config_file_stats.st_ino != stats.st_ino:
            logger.warn("Inode on %s changed. Reloading config", self.config_file)
            self.config_file_stats = stats
            self.load_config()
        elif self.config_file_stats.st_mtime != stats.st_mtime:
            logger.warn("Config file modification time was changed, Reloading: %s", self.config_file)
            self.config_file_stats = stats

    def load_config(self):
        try:
            self.config = util.load_yaml_file(self.config_file)
        except:
            if self.config == {}:
                logger.critical("Issue Loading config: %s   Exiting", self.config_file)
                exit()
            else:
                logger.critical("Issue reloading config: %s   Keeping current settings", self.config_file)
    
    def daemonize(self):
        """ Do the UNIX double-fork magic """
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit first parent
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
    
        # decouple from parent environment
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 
    
        # do second fork
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit from second parent
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1) 
    
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
    
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process    
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
