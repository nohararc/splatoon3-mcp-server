#!/usr/bin/env python3
import sys
import os

# srcディレクトリをPythonパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from server import main

if __name__ == "__main__":
    main()
