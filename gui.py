import tkinter as tk
from tkinter import ttk, messagebox, Frame

class EveProductionCalculator(tk.Tk):
    def __init__(self, ore_data, discovered_modules):
        super().__init__()

        # Store data passed to the calculator
        self.ore_data = ore_data
        self.discovered_modules = discovered_modules

        # Setup the main window
        self.title("EVE Online Production Calculator")
        self.geometry("800x600")

        # Create menu bar
        self.create_menu_bar()
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create tabs
        self.ore_refining_tab = ttk.Frame(self.notebook)
        self.ships_tab = ttk.Frame(self.notebook)
        self.capital_ships_tab = ttk.Frame(self.notebook)
        self.components_tab = ttk.Frame(self.notebook)
        self.pi_calculator_tab = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.ore_refining_tab, text="Ore Refining")
        self.notebook.add(self.ships_tab, text="Ships")
        self.notebook.add(self.capital_ships_tab, text="Capital Ships")
        self.notebook.add(self.components_tab, text="Components")
        self.notebook.add(self.pi_calculator_tab, text="PI Calculator")

        # Initialize each tab
        self.create_ore_refining_tab()
        self.create_ships_tab()
        self.create_capital_ships_tab()
        self.create_components_tab()
        self.create_pi_calculator_tab()

        # Set up status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu_bar(self):
        """Create a menu bar with options to edit blueprint ownership"""
        menu_bar = tk.Menu(self)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Edit Blueprint Ownership", command=self.edit_blueprint_ownership)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.config(menu=menu_bar)

    def edit_blueprint_ownership(self):
        """Open a window to edit blueprint ownership status"""
        ownership_window = tk.Toplevel(self)
        ownership_window.title("Edit Blueprint Ownership")
        ownership_window.geometry("400x600")

        # Frame for ship selection
        ship_selection_frame = ttk.LabelFrame(ownership_window, text="Select Ship")
        ship_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Ship selection
        ship_label = ttk.Label(ship_selection_frame, text="Select Ship:")
        ship_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        ship_list = [module.display_name for module in self.discovered_modules['ships'].values()]
        self.ship_var = tk.StringVar(value=ship_list[0] if ship_list else "")
        ship_dropdown = ttk.Combobox(ship_selection_frame, textvariable=self.ship_var, values=ship_list, state="readonly")
        ship_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ship_dropdown.bind("<<ComboboxSelected>>", self.on_ship_selected)

        # Blueprint ownership selection
        ownership_label = ttk.Label(ship_selection_frame, text="Blueprint Ownership:")
        ownership_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.ownership_var = tk.StringVar(value="Unowned")
        ownership_dropdown = ttk.Combobox(ship_selection_frame, textvariable=self.ownership_var, values=["Owned", "Unowned"], state="readonly")
        ownership_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ownership_dropdown.bind("<<ComboboxSelected>>", self.on_ownership_selected)

        # Frame for capital ship selection
        capital_ship_selection_frame = ttk.LabelFrame(ownership_window, text="Select Capital Ship")
        capital_ship_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Capital Ship selection
        capital_ship_label = ttk.Label(capital_ship_selection_frame, text="Select Capital Ship:")
        capital_ship_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        capital_ship_list = [module.display_name for module in self.discovered_modules['capital_ships'].values()]
        self.capital_ship_var = tk.StringVar(value=capital_ship_list[0] if capital_ship_list else "")
        capital_ship_dropdown = ttk.Combobox(capital_ship_selection_frame, textvariable=self.capital_ship_var, values=capital_ship_list, state="readonly")
        capital_ship_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        capital_ship_dropdown.bind("<<ComboboxSelected>>", self.on_capital_ship_selected)

        # Blueprint ownership selection
        capital_ownership_label = ttk.Label(capital_ship_selection_frame, text="Blueprint Ownership:")
        capital_ownership_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.capital_ownership_var = tk.StringVar(value="Unowned")
        capital_ownership_dropdown = ttk.Combobox(capital_ship_selection_frame, textvariable=self.capital_ownership_var, values=["Owned", "Unowned"], state="readonly")
        capital_ownership_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        capital_ownership_dropdown.bind("<<ComboboxSelected>>", self.on_capital_ownership_selected)

        # Frame for component selection
        component_selection_frame = ttk.LabelFrame(ownership_window, text="Select Component")
        component_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Component selection
        component_label = ttk.Label(component_selection_frame, text="Select Component:")
        component_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        component_list = [module.display_name for module in self.discovered_modules['components'].values()]
        self.component_var = tk.StringVar(value=component_list[0] if component_list else "")
        component_dropdown = ttk.Combobox(component_selection_frame, textvariable=self.component_var, values=component_list, state="readonly")
        component_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        component_dropdown.bind("<<ComboboxSelected>>", self.on_component_selected)

        # Blueprint ownership selection
        component_ownership_label = ttk.Label(component_selection_frame, text="Blueprint Ownership:")
        component_ownership_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.component_ownership_var = tk.StringVar(value="Unowned")
        component_ownership_dropdown = ttk.Combobox(component_selection_frame, textvariable=self.component_ownership_var, values=["Owned", "Unowned"], state="readonly")
        component_ownership_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        component_ownership_dropdown.bind("<<ComboboxSelected>>", self.on_component_ownership_selected)

    def create_ore_refining_tab(self):
        """Create the ore refining calculator tab"""
        # Frame for input controls
        input_frame = ttk.LabelFrame(self.ore_refining_tab, text="Input")
        input_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Ore selection
        ore_label = ttk.Label(input_frame, text="Select Ore:")
        ore_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        ore_list = list(self.ore_data.keys())
        self.ore_var = tk.StringVar(value=ore_list[0])
        ore_dropdown = ttk.Combobox(input_frame, textvariable=self.ore_var, values=ore_list, state="readonly")
        ore_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ore_dropdown.bind("<<ComboboxSelected>>", self.on_ore_selected)

        # Quantity input
        quantity_label = ttk.Label(input_frame, text="Enter Quantity:")
        quantity_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.quantity_var = tk.StringVar(value="100")
        self.quantity_entry = ttk.Entry(input_frame, textvariable=self.quantity_var, width=15)
        self.quantity_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Calculate button
        calculate_button = ttk.Button(input_frame, text="Calculate Minerals", command=self.calculate_ore_refining)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame for results
        results_frame = ttk.LabelFrame(self.ore_refining_tab, text="Mineral Output")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable results area
        self.ore_results_text = tk.Text(results_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.ore_results_text.yview)
        self.ore_results_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ore_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_ships_tab(self):
        """Create the Ships tab"""
        # Frame for ship selection
        ship_selection_frame = ttk.LabelFrame(self.ships_tab, text="Select Ship")
        ship_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Ship selection
        ship_label = ttk.Label(ship_selection_frame, text="Select Ship:")
        ship_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        ship_list = [module.display_name for module in self.discovered_modules['ships'].values()]
        self.ship_var = tk.StringVar(value=ship_list[0] if ship_list else "")
        ship_dropdown = ttk.Combobox(ship_selection_frame, textvariable=self.ship_var, values=ship_list, state="readonly")
        ship_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ship_dropdown.bind("<<ComboboxSelected>>", self.on_ship_selected)

        # Material Efficiency selection
        me_label = ttk.Label(ship_selection_frame, text="Material Efficiency (ME):")
        me_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.me_var = tk.IntVar(value=0)
        me_dropdown = ttk.Combobox(ship_selection_frame, textvariable=self.me_var, values=list(range(11)), state="readonly")
        me_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Calculate button
        calculate_button = ttk.Button(ship_selection_frame, text="Calculate Requirements", command=self.calculate_ship_requirements)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame for results
        results_frame = ttk.LabelFrame(self.ships_tab, text="Ship Requirements")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable results area
        self.ship_results_text = tk.Text(results_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.ship_results_text.yview)
        self.ship_results_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ship_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_capital_ships_tab(self):
        """Create the Capital Ships tab"""
        # Frame for capital ship selection
        capital_ship_selection_frame = ttk.LabelFrame(self.capital_ships_tab, text="Select Capital Ship")
        capital_ship_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Capital Ship selection
        capital_ship_label = ttk.Label(capital_ship_selection_frame, text="Select Capital Ship:")
        capital_ship_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        capital_ship_list = [module.display_name for module in self.discovered_modules['capital_ships'].values()]
        self.capital_ship_var = tk.StringVar(value=capital_ship_list[0] if capital_ship_list else "")
        capital_ship_dropdown = ttk.Combobox(capital_ship_selection_frame, textvariable=self.capital_ship_var, values=capital_ship_list, state="readonly")
        capital_ship_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        capital_ship_dropdown.bind("<<ComboboxSelected>>", self.on_capital_ship_selected)

        # Material Efficiency selection
        me_label = ttk.Label(capital_ship_selection_frame, text="Material Efficiency (ME):")
        me_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.capital_me_var = tk.IntVar(value=0)
        capital_me_dropdown = ttk.Combobox(capital_ship_selection_frame, textvariable=self.capital_me_var, values=list(range(11)), state="readonly")
        capital_me_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Calculate button
        calculate_button = ttk.Button(capital_ship_selection_frame, text="Calculate Requirements", command=self.calculate_capital_ship_requirements)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame for results
        results_frame = ttk.LabelFrame(self.capital_ships_tab, text="Capital Ship Requirements")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable results area
        self.capital_ship_results_text = tk.Text(results_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.capital_ship_results_text.yview)
        self.capital_ship_results_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.capital_ship_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_components_tab(self):
        """Create the Components tab"""
        # Frame for component selection
        component_selection_frame = ttk.LabelFrame(self.components_tab, text="Select Component")
        component_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Component selection
        component_label = ttk.Label(component_selection_frame, text="Select Component:")
        component_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        component_list = [module.display_name for module in self.discovered_modules['components'].values()]
        self.component_var = tk.StringVar(value=component_list[0] if component_list else "")
        component_dropdown = ttk.Combobox(component_selection_frame, textvariable=self.component_var, values=component_list, state="readonly")
        component_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        component_dropdown.bind("<<ComboboxSelected>>", self.on_component_selected)

        # Frame for results
        results_frame = ttk.LabelFrame(self.components_tab, text="Component Requirements")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable results area
        self.component_results_text = tk.Text(results_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.component_results_text.yview)
        self.component_results_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.component_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_pi_calculator_tab(self):
        """Create the Planetary Interaction calculator tab"""
        # Placeholder for future PI calculator implementation
        pi_label = ttk.Label(self.pi_calculator_tab, 
                            text="PI Calculator not yet implemented.\nThis tab will allow calculation of PI material requirements.")
        pi_label.pack(expand=True, pady=20)

    def on_ore_selected(self, event=None):
        """Handler for ore selection change"""
        # This could be used to update UI elements based on ore selection
        pass

    def on_ship_selected(self, event=None):
        """Handler for ship selection change"""
        selected_ship_name = self.ship_var.get()
        for module in self.discovered_modules['ships'].values():
            if module.display_name == selected_ship_name:
                self.update_ship_requirements(module, self.me_var.get())
                break

    def on_capital_ship_selected(self, event=None):
        """Handler for capital ship selection change"""
        selected_capital_ship_name = self.capital_ship_var.get()
        for module in self.discovered_modules['capital_ships'].values():
            if module.display_name == selected_capital_ship_name:
                self.update_capital_ship_requirements(module, self.capital_me_var.get())
                break

    def on_component_selected(self, event=None):
        """Handler for component selection change"""
        selected_component_name = self.component_var.get()
        for module in self.discovered_modules['components'].values():
            if module.display_name == selected_component_name:
                self.update_component_requirements(module)
                break

    def on_component_ownership_selected(self, event=None):
        """Handler for component blueprint ownership selection change"""
        selected_component_name = self.component_var.get()
        ownership_status = self.component_ownership_var.get()
        for module in self.discovered_modules['components'].values():
            if module.display_name == selected_component_name:
                module.owned_status = ownership_status
                break

    def calculate_ore_refining(self):
        """Calculate minerals from ore refining"""
        ore_type = self.ore_var.get()
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Invalid quantity: {str(e)}")
            return

        minerals = self.ore_data.get(ore_type, {})
        if not minerals:
            messagebox.showerror("Error", f"Ore type '{ore_type}' not found in database")
            return

        # Enable text widget for editing
        self.ore_results_text.config(state=tk.NORMAL)
        self.ore_results_text.delete(1.0, tk.END)
        
        # Add header
        self.ore_results_text.insert(tk.END, f"Refining {quantity} units of {ore_type}:\n\n")
        
        # Add mineral outputs
        for mineral, amount in minerals.items():
            total = amount * quantity
            self.ore_results_text.insert(tk.END, f"{mineral}: {total:,}\n")
        
        # Disable text widget again
        self.ore_results_text.config(state=tk.DISABLED)
        
        # Update status
        self.status_var.set(f"Calculated refining output for {quantity} {ore_type}")

    def update_ship_requirements(self, ship_module, me_level):
        """Update the ship requirements display considering material efficiency"""
        self.ship_results_text.config(state=tk.NORMAL)
        self.ship_results_text.delete(1.0, tk.END)
        
        # Add header
        self.ship_results_text.insert(tk.END, f"Requirements for {ship_module.display_name} (ME{me_level}):\n\n")
        
        # Calculate and add each requirement
        for mineral, amount in ship_module.retriever_requirements.items():
            adjusted_amount = amount * (1 - me_level / 100)  # ME level reduces by 1% per level
            self.ship_results_text.insert(tk.END, f"{mineral}: {int(adjusted_amount):,}\n")
        
        self.ship_results_text.config(state=tk.DISABLED)

    def update_capital_ship_requirements(self, capital_ship_module, me_level):
        """Update the requirements for the selected capital ship based on ME level"""
        # Determine the correct attribute name for the requirements
        for attr_name in dir(capital_ship_module):
            if attr_name.endswith("_requirements"):
                requirements_attr = attr_name
                break
        else:
            raise AttributeError(f"Module '{capital_ship_module}' does not have a requirements attribute")

        # Access the requirements dynamically
        requirements = getattr(capital_ship_module, requirements_attr)

        # Calculate and display the updated requirements
        self.capital_ship_results_text.config(state=tk.NORMAL)
        self.capital_ship_results_text.delete(1.0, tk.END)

        for component, quantity in requirements.items():
            adjusted_quantity = quantity * (1 - 0.01 * me_level)
            self.capital_ship_results_text.insert(tk.END, f"{component}: {adjusted_quantity}\n")

        self.capital_ship_results_text.config(state=tk.DISABLED)

    def update_component_requirements(self, component_module):
        """Update the component requirements display"""
        self.component_results_text.config(state=tk.NORMAL)
        self.component_results_text.delete(1.0, tk.END)
        
        # Add header
        self.component_results_text.insert(tk.END, f"Requirements for {component_module.display_name}:\n\n")
        
        # Add each requirement
        for mineral, amount in component_module.capital_component_data.items():
            self.component_results_text.insert(tk.END, f"{mineral}: {amount}\n")
        
        self.component_results_text.config(state=tk.DISABLED)

    def calculate_ship_requirements(self):
        """Calculate the requirements for the selected ship"""
        selected_ship_name = self.ship_var.get()
        me_level = self.me_var.get()
        for module in self.discovered_modules['ships'].values():
            if module.display_name == selected_ship_name:
                self.update_ship_requirements(module, me_level)
                break

    def calculate_capital_ship_requirements(self):
        """Calculate the requirements for the selected capital ship"""
        selected_capital_ship_name = self.capital_ship_var.get()
        me_level = self.capital_me_var.get()
        for module in self.discovered_modules['capital_ships'].values():
            if module.display_name == selected_capital_ship_name:
                self.update_capital_ship_requirements(module, me_level)
                break
