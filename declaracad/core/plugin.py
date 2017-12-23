"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Jul 12, 2015

@author: jrm
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from atom.api import Unicode
from .api import Plugin


class CorePlugin(Plugin):

    _log_filename = Unicode()
    _log_format = Unicode(
        '%(asctime)-15s | %(levelname)-7s | %(name)s | %(message)s')

    def start(self):
        self.init_logging()
        self.workbench.application.deferred_call(self.start_default_workspace)

    def start_default_workspace(self):
        ui = self.workbench.get_plugin('enaml.workbench.ui')
        ui.select_workspace('declaracad.workspace')


    def _default__log_filename(self):
        log_dir = os.path.expanduser('~/.config/declaracad/logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, 'declaracad.txt')

    def init_logging(self):
        """ Log to stdout and the file """
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        formatter = logging.Formatter(self._log_format)

        #: Log to stdout
        stream = logging.StreamHandler(sys.stdout)
        stream.setLevel(logging.DEBUG)
        stream.setFormatter(formatter)

        #: Log to rotating handler
        disk = RotatingFileHandler(
            self._log_filename,
            maxBytes=1024*1024*10,  # 10 MB
            backupCount=10,
        )
        disk.setLevel(logging.DEBUG)
        disk.setFormatter(formatter)

        root.addHandler(disk)
        root.addHandler(stream)
