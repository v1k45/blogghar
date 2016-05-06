#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # lets use development settings by default.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "blogghar.settings.development")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
