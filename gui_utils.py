"""
GUI Utilities for EVE Production Calculator

This module contains factory methods for creating consistent GUI elements
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional, Any, Dict, Union

def create_labeled_dropdown(parent: ttk.Frame,
                          label_text: str,
                          variable: tk.StringVar,
                          values: List[str],
                          width: int = 30,
                          label_width: int = 15,
                          command: Optional[Callable] = None) -> ttk.Combobox:
    """
    Create a labeled dropdown (Combobox) with consistent styling
    
    Args:
        parent: Parent widget
        label_text: Text for the label
        variable: StringVar to bind to the dropdown
        values: List of values for the dropdown
        width: Width of the dropdown
        label_width: Width of the label
        command: Optional callback for ComboboxSelected event
        
    Returns:
        The created Combobox widget
    """
    frame = ttk.Frame(parent)
    frame.pack(fill="x", padx=5, pady=2)
    
    label = ttk.Label(frame, text=label_text, width=label_width)
    label.pack(side="left", padx=5, pady=2)
    
    dropdown = ttk.Combobox(frame, textvariable=variable, values=values, width=width)
    dropdown.pack(side="left", padx=5, pady=2, fill="x", expand=True)
    
    if command:
        dropdown.bind("<<ComboboxSelected>>", command)
        
    return dropdown

def create_labeled_entry(parent: ttk.Frame,
                       label_text: str,
                       variable: tk.StringVar,
                       width: int = 30,
                       label_width: int = 15) -> ttk.Entry:
    """
    Create a labeled entry field with consistent styling
    
    Args:
        parent: Parent widget
        label_text: Text for the label
        variable: StringVar to bind to the entry
        width: Width of the entry
        label_width: Width of the label
        
    Returns:
        The created Entry widget
    """
    frame = ttk.Frame(parent)
    frame.pack(fill="x", padx=5, pady=2)
    
    label = ttk.Label(frame, text=label_text, width=label_width)
    label.pack(side="left", padx=5, pady=2)
    
    entry = ttk.Entry(frame, textvariable=variable, width=width)
    entry.pack(side="left", padx=5, pady=2, fill="x", expand=True)
    
    return entry

def create_button(parent: ttk.Frame,
                text: str,
                command: Callable,
                width: int = 20) -> ttk.Button:
    """
    Create a button with consistent styling
    
    Args:
        parent: Parent widget
        text: Button text
        command: Callback for button click
        width: Width of the button
        
    Returns:
        The created Button widget
    """
    button = ttk.Button(parent, text=text, command=command, width=width)
    button.pack(padx=5, pady=5)
    
    return button

def create_scrolled_text(parent: ttk.Frame,
                        height: int = 20,
                        width: int = 80,
                        readonly: bool = True) -> tk.Text:
    """
    Create a scrolled text widget with consistent styling
    
    Args:
        parent: Parent widget
        height: Height in text lines
        width: Width in characters
        readonly: Whether the text widget should be read-only
        
    Returns:
        The created Text widget
    """
    # Create a frame to hold the Text and Scrollbar
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create a Text widget
    text_widget = tk.Text(frame, height=height, width=width, wrap="word")
    text_widget.pack(side="left", fill="both", expand=True)
    
    # Create a Scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
    scrollbar.pack(side="right", fill="y")
    
    # Connect the scrollbar to the text widget
    text_widget.config(yscrollcommand=scrollbar.set)
    
    # Make read-only if specified
    if readonly:
        text_widget.config(state="disabled")
    
    return text_widget

def create_label_frame(parent: ttk.Frame,
                     title: str,
                     pack_fill: str = "x",
                     expand: bool = False) -> ttk.LabelFrame:
    """
    Create a labeled frame with consistent styling
    
    Args:
        parent: Parent widget
        title: Title for the labeled frame
        pack_fill: Fill direction for pack manager
        expand: Whether to expand the frame
        
    Returns:
        The created LabelFrame widget
    """
    frame = ttk.LabelFrame(parent, text=title)
    frame.pack(fill=pack_fill, expand=expand, padx=10, pady=10)
    
    return frame

def set_text_content(text_widget: tk.Text, content: str) -> None:
    """
    Set content of a text widget, handling read-only state
    
    Args:
        text_widget: The Text widget to update
        content: Content to set
    """
    # Enable editing temporarily
    current_state = text_widget.cget("state")
    text_widget.config(state="normal")
    
    # Clear existing content and insert new content
    text_widget.delete("1.0", tk.END)
    text_widget.insert("1.0", content)
    
    # Restore original state
    text_widget.config(state=current_state)

def create_grid_view(parent: ttk.Frame, 
                    columns: List[Dict[str, Any]],
                    height: int = 10) -> ttk.Treeview:
    """
    Create a grid view (Treeview) with specified columns
    
    Args:
        parent: Parent widget
        columns: List of column definitions, each with 'id', 'text', and 'width' keys
        height: Height in rows
        
    Returns:
        The created Treeview widget
    """
    # Extract column IDs and create format string
    column_ids = [col['id'] for col in columns]
    
    # Create the treeview with scrollbars
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    tree = ttk.Treeview(frame, columns=column_ids, show='headings', height=height)
    
    # Configure columns and headings
    for col in columns:
        tree.column(col['id'], width=col.get('width', 100), anchor=col.get('anchor', 'w'))
        tree.heading(col['id'], text=col['text'])
    
    # Add scrollbars
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # Grid layout for tree and scrollbars
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    
    # Configure grid weights
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    
    return tree
