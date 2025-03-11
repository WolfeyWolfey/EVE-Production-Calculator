"""
EVE Production Calculator main application window
This is an alternative implementation to gui.py that provides a simplified interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

from core.config.blueprint_config import load_blueprint_ownership, save_blueprint_ownership
from core.gui.gui_utils import create_labeled_entry, create_button, create_scrolled_text
from core.utils.debug import debug_print

class EveProductionCalculator(tk.Tk):
    """Main application window for EVE Production Calculator"""
    
    def __init__(self, registry, calculator, blueprint_config):
        """
        Initialize the main application window
        
        Args:
            registry: Module registry
            calculator: Requirements calculator
            blueprint_config: Blueprint ownership configuration
        """
        super().__init__()
        
        # Store references
        self.registry = registry
        self.calculator = calculator
        self.blueprint_config = blueprint_config
        
        # Configure window
        self.title("EVE Online Production Calculator")
        self.geometry("1024x768")
        self.minsize(800, 600)
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create tabs
        self.ships_tab = ttk.Frame(self.notebook)
        self.capital_ships_tab = ttk.Frame(self.notebook)
        self.components_tab = ttk.Frame(self.notebook)
        self.pi_tab = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.ships_tab, text="Ships")
        self.notebook.add(self.capital_ships_tab, text="Capital Ships")
        self.notebook.add(self.components_tab, text="Components")
        self.notebook.add(self.pi_tab, text="PI Materials")
        
        # Initialize tabs
        self.create_ships_tab()
        self.create_capital_ships_tab()
        self.create_components_tab()
        self.create_pi_tab()
        
        # Create menu
        self.create_menu()
        
        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_menu(self):
        """Create menu bar"""
        menu_bar = tk.Menu(self)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Blueprint menu
        blueprint_menu = tk.Menu(menu_bar, tearoff=0)
        blueprint_menu.add_command(label="Blueprint Manager", command=self.open_blueprint_manager)
        blueprint_menu.add_command(label="Reset Ship Ownership", command=self.reset_ship_ownership)
        menu_bar.add_cascade(label="Blueprints", menu=blueprint_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menu_bar)
    
    def create_ships_tab(self):
        """Create ships tab"""
        # To be implemented
        ttk.Label(self.ships_tab, text="Ships tab content").pack(pady=20)
    
    def create_capital_ships_tab(self):
        """Create capital ships tab"""
        # To be implemented
        ttk.Label(self.capital_ships_tab, text="Capital ships tab content").pack(pady=20)
    
    def create_components_tab(self):
        """Create components tab"""
        # To be implemented
        ttk.Label(self.components_tab, text="Components tab content").pack(pady=20)
    
    def create_pi_tab(self):
        """Create PI materials tab"""
        # To be implemented
        ttk.Label(self.pi_tab, text="PI materials tab content").pack(pady=20)
    
    def open_settings(self):
        """Open settings window"""
        # To be implemented with settings GUI
        messagebox.showinfo("Settings", "Settings dialog will be implemented here")
    
    def open_blueprint_manager(self):
        """Open blueprint manager"""
        # To be implemented with blueprints GUI
        messagebox.showinfo("Blueprint Manager", "Blueprint manager will be implemented here")
    
    def reset_ship_ownership(self):
        """Reset ship ownership status"""
        # To be implemented with blueprint utilities
        messagebox.showinfo("Reset Ship Ownership", "Reset ship ownership will be implemented here")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About EVE Production Calculator",
            "EVE Online Production Calculator\n\n"
            "A tool for calculating production requirements for EVE Online ships,"
            "components, and PI materials."
        )
    
    def on_close(self):
        """Handle window close event"""
        # Save blueprint configuration before exiting
        save_blueprint_ownership(self.blueprint_config)
        
        # Destroy window
        self.destroy()


def launch_app(registry, calculator, blueprint_config):
    """
    Launch the EVE Production Calculator application
    
    Args:
        registry: Module registry
        calculator: Requirements calculator
        blueprint_config: Blueprint ownership configuration
    """
    app = EveProductionCalculator(registry, calculator, blueprint_config)
    app.mainloop()
    return app
