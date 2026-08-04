#!/usr/bin/env python3

import sys
import pulla.main

try:
    pulla.main.app()
except KeyboardInterrupt:
    sys.exit(1)
