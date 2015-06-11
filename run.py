#!/usr/bin/env python3

import sys
import pulla.main

try:
    sys.exit(pulla.main.main())
except KeyboardInterrupt:
    sys.exit(1)
