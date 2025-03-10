"""
Settings GUI for EVE Production Calculator
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from gui.gui_utils import create_button, create_label_frame

class SettingsWindow(tk.Toplevel):
    """Settings window for EVE Production Calculator"""
    def __init__(self, parent, registry, calculator, blueprint_config):
        """Initialize the settings window"""
        super().__init__(parent)
        
        # Store references
        self.parent = parent
        self.registry = registry
        self.calculator = calculator
        self.blueprint_config = blueprint_config
        
        # Configure window
        self.title("Settings")
        self.geometry("600x400")
        self.minsize(500, 300)
        self.resizable(True, True)
        
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Create UI
        self.create_ui()
        
        # Make window modal
        self.grab_set()
        self.focus_set()
        self.wait_window()
    
    def create_ui(self):
        """Create settings window UI"""
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame for blueprint ownership settings
        blueprint_frame = create_label_frame(main_frame, "Blueprint Ownership")
        blueprint_frame.pack(fill="x", padx=5, pady=5)
        
        # Button to edit blueprint ownership
        edit_blueprints_button = create_button(
            blueprint_frame,
            "Edit Blueprint Ownership",
            self.edit_blueprint_ownership
        )
        
        # Frame for import/export settings
        import_export_frame = create_label_frame(main_frame, "Import/Export")
        import_export_frame.pack(fill="x", padx=5, pady=5)
        
        # Buttons for import/export
        export_button = create_button(
            import_export_frame,
            "Export Settings",
            self.export_settings
        )
        
        import_button = create_button(
            import_export_frame,
            "Import Settings",
            self.import_settings
        )
        
        # Ship Information frame
        ship_info_frame = create_label_frame(main_frame, "Ship Information and Requirements")
        ship_info_frame.pack(fill="x", padx=5, pady=5)
        
        # Button to reset ship ownership
        reset_ship_button = create_button(
            ship_info_frame,
            "Reset All Ship Ownership",
            self.reset_ship_ownership
        )
        
        # Close button at the bottom
        close_button_frame = ttk.Frame(main_frame)
        close_button_frame.pack(fill="x", padx=5, pady=10)
        
        close_button = create_button(
            close_button_frame,
            "Close",
            self.destroy
        )
    
    def edit_blueprint_ownership(self):
        """Open the Blueprint Ownership Editor"""
        self.parent.edit_blueprint_ownership()
    
    def reset_ship_ownership(self):
        """Reset ownership status for all ships"""
        self.parent.reset_ship_ownership()
    
    def export_settings(self):
        """Export settings to a JSON file"""
        self.parent.export_settings()
    
    def import_settings(self):
        """Import settings from a JSON file"""
        self.parent.import_settings()
