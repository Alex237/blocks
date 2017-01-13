#!/usr/bin/env python
import os, time, sys, urllib, re

# http://eyalarubas.com/python-subproc-nonblock.html
from subprocess import Popen, PIPE
from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read

class glslViewer:
    COMMAND='glslViewer'
    process = {}
    cout = {}
    wait_time = 0.0001
    time = 0.
    delta = 0.
    fps = 0

    def __init__(self, filename, options = {}):
        cmd = [self.COMMAND]

        if options.has_key("width"):
            cmd.append('-w '+ str(options["width"]))
        if options.has_key("height"):
            cmd.append('-h '+ str(options["height"]))

        if options.has_key("visible"):
            if not options["visible"]:
                cmd.append('--headless')

        cmd.append(filename)
        self.process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr = PIPE, shell=False)
        flags = fcntl(self.process.stdout, F_GETFL) # get current self.process.stdout flags
        fcntl(self.process.stdout, F_SETFL, flags | O_NONBLOCK)
        # self.cout = NonBlockingStreamReader(self.process)

    def read(self):
        while True:
            try:
                return read(self.process.stdout.fileno(), 1024).rstrip()
            except OSError:
                return 'none'

    def isFinish(self):
        return self.process.poll() is not None
        
    def getTime(self):
        self.process.stdin.write('time\n')
        sleep(self.wait_time)
        answer = self.read()
        if answer:
            if answer.replace('.','',1).isdigit():
                self.time = float(answer)
        return self.time
        
    def getDelta(self):
        self.process.stdin.write('delta\n')
        sleep(self.wait_time)
        answer = self.read()
        if answer:
            if answer.replace('.','',1).isdigit():
                self.delta = float(answer)
        return self.delta


    def getFPS(self):
        return self.process.stdin.write('fps\n')
        sleep(self.wait_time)
        answer = self.read()
        if answer:
            if answer.replace('.','',1).isdigit():
                self.fps = float(answer)
        return self.fps

    def stop(self):
        self.process.kill()
