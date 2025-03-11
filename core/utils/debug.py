"""
Debug utilities for EVE Production Tracker

This module provides debugging functions that can be enabled/disabled
via command line arguments.
"""

# Global debug flag - default to False (off)
DEBUG_MODE = False

def set_debug_mode(enabled=False):
    """
    Set the global debug mode
    
    Args:
        enabled: Boolean to enable/disable debug mode
    """
    global DEBUG_MODE
    DEBUG_MODE = enabled
    
    if enabled:
        debug_print("Debug mode enabled")

def debug_print(*args, **kwargs):
    """
    Print debug information if debug mode is enabled
    
    Args:
        *args: Arguments to pass to print()
        **kwargs: Keyword arguments to pass to print()
    """
    if DEBUG_MODE:
        print(*args, **kwargs)
