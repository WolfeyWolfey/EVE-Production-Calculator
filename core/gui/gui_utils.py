"""
GUI Utilities for EVE Production Calculator

This module contains factory methods for creating consistent GUI elements
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional, Any, Dict, Union

def _create_labeled_widget_base(parent: ttk.Frame, label_text: str, 
                             widget_class: Callable, widget_args: Dict[str, Any],
                             width: int = 30, label_width: int = 15) -> Any:
    """
    Base function for creating a labeled widget with consistent styling
    
    Args:
        parent: Parent widget
        label_text: Text for the label
        widget_class: Class/constructor for the widget to create
        widget_args: Arguments for the widget constructor
        width: Width of the widget
        label_width: Width of the label
        
    Returns:
        The created widget
    """
    frame = ttk.Frame(parent)
    frame.pack(fill="x", padx=5, pady=2)
    
    label = ttk.Label(frame, text=label_text, width=label_width)
    label.pack(side="left", padx=5, pady=2)
    
    widget_args.update({"width": width})
    widget = widget_class(frame, **widget_args)
    widget.pack(side="left", fill="x", expand=True, padx=5, pady=2)
    
    return widget

def create_labeled_dropdown(parent: ttk.Frame, label_text: str, 
                          variable: tk.StringVar, values: List[str],
                          width: int = 30, label_width: int = 15,
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
    widget_args = {
        "textvariable": variable,
        "values": values,
        "state": "readonly"
    }
    
    combobox = _create_labeled_widget_base(
        parent, label_text, ttk.Combobox, widget_args, width, label_width
    )
    
    if command:
        combobox.bind("<<ComboboxSelected>>", command)
    
    return combobox

def create_labeled_entry(parent: ttk.Frame, label_text: str, 
                       variable: tk.StringVar, width: int = 30,
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
    widget_args = {
        "textvariable": variable
    }
    
    return _create_labeled_widget_base(
        parent, label_text, ttk.Entry, widget_args, width, label_width
    )

def create_button(parent: ttk.Frame, text: str, command: Callable, 
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
    button.pack(fill="x", padx=5, pady=5)
    return button

def create_scrolled_text(parent: ttk.Frame, height: int = 20, 
                        width: int = 80, readonly: bool = True) -> tk.Text:
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
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Create text widget
    text_widget = tk.Text(frame, height=height, width=width, wrap=tk.WORD)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Create scrollbar
    scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Link scrollbar with text widget
    text_widget['yscrollcommand'] = scrollbar.set
    
    # Set readonly if needed
    if readonly:
        text_widget.config(state=tk.DISABLED)
    
    return text_widget

def create_label_frame(parent: tk.Widget, title: str, **kwargs) -> ttk.LabelFrame:
    """
    Create a LabelFrame with nice defaults
    
    Args:
        parent: Parent widget
        title: Title for the labeled frame
        **kwargs: Additional keyword arguments, including:
            pack_fill: Fill direction for pack manager (default=tk.BOTH)
            expand: Whether to expand the frame (default=True)
            use_grid: Whether to use grid instead of pack (default=False)
            grid_row: Row for grid layout (default=0)
            grid_column: Column for grid layout (default=0)
            grid_sticky: Sticky parameter for grid layout (default="nsew")
            grid_padx: X padding for grid layout (default=10)
            grid_pady: Y padding for grid layout (default=10)
            grid_rowspan: Row span for grid layout (default=1)
            grid_columnspan: Column span for grid layout (default=1)
        
    Returns:
        The created LabelFrame widget
    """
    # Extract layout parameters
    pack_fill = kwargs.get('pack_fill', tk.BOTH)
    expand = kwargs.get('expand', True)
    use_grid = kwargs.get('use_grid', False)
    grid_row = kwargs.get('grid_row', 0)
    grid_column = kwargs.get('grid_column', 0)
    grid_sticky = kwargs.get('grid_sticky', "nsew")
    grid_padx = kwargs.get('grid_padx', 10)
    grid_pady = kwargs.get('grid_pady', 10)
    grid_rowspan = kwargs.get('grid_rowspan', 1)
    grid_columnspan = kwargs.get('grid_columnspan', 1)
    
    # Create frame
    frame = ttk.LabelFrame(parent, text=title)
    
    # Apply layout
    if use_grid:
        frame.grid(
            row=grid_row, 
            column=grid_column, 
            sticky=grid_sticky, 
            padx=grid_padx, 
            pady=grid_pady,
            rowspan=grid_rowspan,
            columnspan=grid_columnspan
        )
    else:
        frame.pack(fill=pack_fill, expand=expand, padx=10, pady=10)
    
    return frame

def create_grid_view(parent: ttk.Frame, columns: List[Dict[str, Any]], 
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
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Extract column IDs
    column_ids = [col['id'] for col in columns]
    
    # Create treeview with scrollbar
    tree = ttk.Treeview(frame, columns=column_ids, show='headings', height=height)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Add vertical scrollbar
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=vsb.set)
    
    # Configure columns
    for col in columns:
        tree.heading(col['id'], text=col['text'])
        tree.column(col['id'], width=col.get('width', 100), anchor=col.get('anchor', 'center'))
    
    return tree

def set_text_content(text_widget: tk.Text, content: str) -> None:
    """
    Set content of a text widget, handling read-only state
    
    Args:
        text_widget: The Text widget to update
        content: Content to set
    """
    # Check if the widget is read-only (DISABLED)
    readonly = (text_widget.cget('state') == 'disabled')
    
    # Enable editing temporarily if it was read-only
    if readonly:
        text_widget.config(state=tk.NORMAL)
    
    # Clear existing content and insert new content
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, content)
    
    # Restore read-only state if needed
    if readonly:
        text_widget.config(state=tk.DISABLED)
