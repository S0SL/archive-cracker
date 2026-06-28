#!/usr/bin/env python3
"""
Archive Password Cracker - Cross-platform GUI application
Supports Windows, Linux, and Android
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

font_path = os.path.join(base_path, 'fonts', 'simkai.ttf')

from kivy.core.text import LabelBase
from kivy.config import Config

LabelBase.register(name='Chinese', fn_regular=font_path)
Config.set('kivy', 'default_font_name', 'Chinese')

from ui.app import ArchiveCrackerApp


def main():
    app = ArchiveCrackerApp()
    app.run()


if __name__ == '__main__':
    main()
