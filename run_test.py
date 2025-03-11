#!/usr/bin/env python3
"""
Test script for the EVE Production Tracker after restructuring
"""

import sys
import os

if __name__ == "__main__":
    # Execute the main.py script to test if all imports work properly
    try:
        import main
        main.main()
        print("Application started successfully with new structure!")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Type: {type(e).__name__}")
        print(f"Module: {getattr(e, '__module__', 'N/A')}")
        import traceback
        traceback.print_exc()
