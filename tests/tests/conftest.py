"""
Pytest configuration — adds the project root to sys.path so all
test files can import the source modules without installation.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
