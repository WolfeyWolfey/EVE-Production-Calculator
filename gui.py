import tkinter as tk
from tkinter import ttk, messagebox
from blueprints_gui import BlueprintManager
from blueprint_config import update_blueprint_ownership, get_blueprint_ownership, update_blueprint_invention

class EveProductionCalculator(tk.Tk):
    def __init__(self, ore_data, discovered_modules, blueprint_config):
        super().__init__()

        # Store data passed to the calculator
        self.ore_data = ore_data
        self.discovered_modules = discovered_modules
        self.blueprint_config = blueprint_config
        
        # Get PI data from discovered modules if available
        self.pi_data = {}
        if 'pi_data' in discovered_modules:
            self.pi_data = discovered_modules['pi_data']

        # Initialize variables for blueprint ownership
        self.ship_var = tk.StringVar()  
        self.capital_ship_var = tk.StringVar()
        self.component_var = tk.StringVar()
        self.cap_module_var = tk.StringVar()
        self.cap_component_var = tk.StringVar()
        self.cap_component_ownership_var = tk.StringVar()
        
        # Ship calculator variables
        self.me_var = tk.StringVar(value="0")  
        self.capital_me_var = tk.StringVar(value="0")  
        self.faction_var = tk.StringVar(value="All")
        self.ship_type_var = tk.StringVar(value="All")

        # Initialize variables for calculations
        self.ore_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1000")
        self.refining_efficiency_var = tk.StringVar(value="70")
        
        # Initialize variables for PI calculator
        self.pi_type_var = tk.StringVar()
        self.pi_component_var = tk.StringVar()
        self.pi_details_text = None  

        # Initialize variables for blueprint ownership
        self.ownership_var = tk.StringVar(value="Unowned")
        self.capital_ownership_var = tk.StringVar(value="Unowned")
        self.component_ownership_var = tk.StringVar(value="Unowned")
        self.cap_component_ownership_var = tk.StringVar(value="Unowned")
        
        # Setup the main window
        self.title("EVE Online Production Calculator")
        self.geometry("800x600")

        # Create menu bar
        self.create_menu_bar()
        
        # Set up status bar variable first
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Initialize Blueprint Manager
        self.blueprint_manager = BlueprintManager(self, discovered_modules, blueprint_config)
        
        # Create tabs
        self.create_tabs()
        
        # Create status bar UI element
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu_bar(self):
        """Create the menu bar for the application"""
        menu_bar = tk.Menu(self)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Reload", command=self.reload_application)
        file_menu.add_command(label="Blueprints", command=self.show_blueprint_grid)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menu_bar)

    def create_tabs(self):
        """Create the main tabs for the application"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        # Create tab frames
        self.ore_calculator_tab = ttk.Frame(self.notebook)
        self.ship_calculator_tab = ttk.Frame(self.notebook)
        self.component_calculator_tab = ttk.Frame(self.notebook)
        self.capital_ship_calculator_tab = ttk.Frame(self.notebook)
        self.pi_calculator_tab = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.ore_calculator_tab, text="Ore Calculator")
        self.notebook.add(self.ship_calculator_tab, text="Ship Calculator")
        self.notebook.add(self.component_calculator_tab, text="Component Calculator")
        self.notebook.add(self.capital_ship_calculator_tab, text="Capital Ship Calculator")
        self.notebook.add(self.pi_calculator_tab, text="PI Calculator")
        
        # Create calculator tabs
        self.create_ore_calculator_tab()
        self.create_ship_calculator_tab()
        self.create_component_calculator_tab()
        self.create_capital_ship_calculator_tab()
        self.init_pi_calculator_elements(self.pi_calculator_tab)

    def create_ore_calculator_tab(self):
        """Create the ore calculator tab"""
        # Frame for input controls
        input_frame = ttk.LabelFrame(self.ore_calculator_tab, text="Input")
        input_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Ore selection
        ore_label = ttk.Label(input_frame, text="Select Ore:")
        ore_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        ore_list = list(self.ore_data.keys())
        self.ore_var.set(ore_list[0])
        ore_dropdown = ttk.Combobox(input_frame, textvariable=self.ore_var, values=ore_list, state="readonly")
        ore_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ore_dropdown.bind("<<ComboboxSelected>>", self.on_ore_selected)

        # Quantity input
        quantity_label = ttk.Label(input_frame, text="Enter Quantity:")
        quantity_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.quantity_entry = ttk.Entry(input_frame, textvariable=self.quantity_var, width=15)
        self.quantity_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Refining Efficiency input
        refining_efficiency_label = ttk.Label(input_frame, text="Refining Efficiency (%):")
        refining_efficiency_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.refining_efficiency_entry = ttk.Entry(input_frame, textvariable=self.refining_efficiency_var, width=15)
        self.refining_efficiency_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Calculate button
        calculate_button = ttk.Button(input_frame, text="Calculate Minerals", command=self.calculate_ore_refining)
        calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Frame for results
        results_frame = ttk.LabelFrame(self.ore_calculator_tab, text="Mineral Output")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable results area
        self.ore_results_text = tk.Text(results_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.ore_results_text.yview)
        self.ore_results_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ore_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_ship_calculator_tab(self):
        """Create the ship calculator tab"""
        # Frame for ship selection
        ship_selection_frame = ttk.LabelFrame(self.ship_calculator_tab, text="Select Ship")
        ship_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)
        
        # Faction filter
        faction_label = ttk.Label(ship_selection_frame, text="Faction:")
        faction_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Get unique factions from ships
        factions = ["All"]
        for ship in self.discovered_modules['ships'].values():
            if hasattr(ship, 'faction') and ship.faction not in factions:
                factions.append(ship.faction)
        
        faction_dropdown = ttk.Combobox(ship_selection_frame, textvariable=self.faction_var, values=factions, state="readonly", width=15)
        faction_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        faction_dropdown.bind("<<ComboboxSelected>>", self.filter_ships)
        
        # Ship type filter
        type_label = ttk.Label(ship_selection_frame, text="Ship Type:")
        type_label.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Get unique ship types
        ship_types = ["All"]
        for ship in self.discovered_modules['ships'].values():
            if hasattr(ship, 'ship_type') and ship.ship_type not in ship_types:
                ship_types.append(ship.ship_type)
        
        type_dropdown = ttk.Combobox(ship_selection_frame, textvariable=self.ship_type_var, values=ship_types, state="readonly", width=15)
        type_dropdown.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        type_dropdown.bind("<<ComboboxSelected>>", self.filter_ships)

        # Ship selection
        ship_label = ttk.Label(ship_selection_frame, text="Select Ship:")
        ship_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        # Get filtered ship list (initially all ships)
        self.filtered_ships = [module.display_name for module in self.discovered_modules['ships'].values()]
        
        self.ship_dropdown = ttk.Combobox(ship_selection_frame, textvariable=self.ship_var, values=self.filtered_ships, state="readonly", width=30)
        self.ship_dropdown.grid(row=1, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        self.ship_dropdown.bind("<<ComboboxSelected>>", self.on_ship_selected)
        if self.filtered_ships:
            self.ship_var.set(self.filtered_ships[0])

        # Material Efficiency selection
        me_label = ttk.Label(ship_selection_frame, text="Material Efficiency (ME):")
        me_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        me_dropdown = ttk.Combobox(ship_selection_frame, textvariable=self.me_var, values=list(range(11)), state="readonly")
        me_dropdown.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Calculate button
        calculate_button = ttk.Button(ship_selection_frame, text="Calculate Requirements", command=self.calculate_ship_requirements)
        calculate_button.grid(row=3, column=0, columnspan=4, pady=10)

        # Frame for results
        results_frame = ttk.LabelFrame(self.ship_calculator_tab, text="Ship Requirements")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable results area
        self.ship_results_text = tk.Text(results_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.ship_results_text.yview)
        self.ship_results_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ship_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_component_calculator_tab(self):
        """Create the component calculator tab"""
        # Frame for component selection
        component_selection_frame = ttk.LabelFrame(self.component_calculator_tab, text="Select Component")
        component_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Component selection
        component_label = ttk.Label(component_selection_frame, text="Select Component:")
        component_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        component_list = [module.display_name for module in self.discovered_modules['components'].values()]
        self.component_var.set(component_list[0] if component_list else "")
        component_dropdown = ttk.Combobox(component_selection_frame, textvariable=self.component_var, values=component_list, state="readonly")
        component_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        component_dropdown.bind("<<ComboboxSelected>>", self.on_component_selected)

        # Calculate button
        calculate_button = ttk.Button(component_selection_frame, text="Calculate Requirements", command=self.calculate_component_requirements)
        calculate_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Frame for results
        results_frame = ttk.LabelFrame(self.component_calculator_tab, text="Component Requirements")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable results area
        self.component_results_text = tk.Text(results_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.component_results_text.yview)
        self.component_results_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.component_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_capital_ship_calculator_tab(self):
        """Create the capital ship calculator tab"""
        # Frame for capital ship selection
        capital_ship_selection_frame = ttk.LabelFrame(self.capital_ship_calculator_tab, text="Select Capital Ship")
        capital_ship_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Capital ship selection
        capital_ship_label = ttk.Label(capital_ship_selection_frame, text="Select Capital Ship:")
        capital_ship_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        capital_ship_list = [module.display_name for module in self.discovered_modules['capital_ships'].values()]
        self.capital_ship_var.set(capital_ship_list[0] if capital_ship_list else "")
        capital_ship_dropdown = ttk.Combobox(capital_ship_selection_frame, textvariable=self.capital_ship_var, values=capital_ship_list, state="readonly")
        capital_ship_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        capital_ship_dropdown.bind("<<ComboboxSelected>>", self.on_capital_ship_selected)

        # Material Efficiency selection
        capital_me_label = ttk.Label(capital_ship_selection_frame, text="Material Efficiency (ME):")
        capital_me_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        capital_me_dropdown = ttk.Combobox(capital_ship_selection_frame, textvariable=self.capital_me_var, values=list(range(11)), state="readonly")
        capital_me_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Calculate button
        calculate_button = ttk.Button(capital_ship_selection_frame, text="Calculate Requirements", command=self.calculate_capital_ship_requirements)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame for results
        results_frame = ttk.LabelFrame(self.capital_ship_calculator_tab, text="Capital Ship Requirements")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable results area
        self.capital_ship_results_text = tk.Text(results_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.capital_ship_results_text.yview)
        self.capital_ship_results_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.capital_ship_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def init_pi_calculator_elements(self, pi_tab):
        """Initialize PI calculator elements"""
        # Create frame for input and display
        pi_control_frame = ttk.Frame(pi_tab)
        pi_control_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Create dropdown for PI type selection
        pi_type_frame = ttk.LabelFrame(pi_control_frame, text="Planetary Material Type")
        pi_type_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        self.pi_type_var = tk.StringVar()
        pi_type_combo = ttk.Combobox(pi_type_frame, textvariable=self.pi_type_var, state="readonly", width=20)
        pi_type_combo['values'] = ("P0 (Raw)", "P1 (Basic)", "P2 (Advanced)", "P3 (Processed)")
        pi_type_combo.current(0)
        pi_type_combo.pack(padx=10, pady=10)
        pi_type_combo.bind("<<ComboboxSelected>>", lambda e: self.populate_pi_dropdown(self.pi_type_var.get()))
        
        # Create dropdown for specific PI component
        pi_component_frame = ttk.LabelFrame(pi_control_frame, text="Planetary Material")
        pi_component_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        self.pi_component_var = tk.StringVar()
        self.pi_component_combo = ttk.Combobox(pi_component_frame, textvariable=self.pi_component_var, state="readonly", width=30)
        self.pi_component_combo.pack(padx=10, pady=10)
        self.pi_component_combo.bind("<<ComboboxSelected>>", lambda e: self.on_pi_component_selected())
        
        # Initialize component dropdown
        self.populate_pi_dropdown("P0 (Raw)")
        
        # Create details display area
        pi_details_frame = ttk.LabelFrame(pi_tab, text="Material Details")
        pi_details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add text widget for displaying details with scrollbar
        details_scroll = ttk.Scrollbar(pi_details_frame)
        details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.pi_details_text = tk.Text(pi_details_frame, wrap=tk.WORD, width=70, height=20)
        self.pi_details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Connect scrollbar to text widget
        details_scroll.config(command=self.pi_details_text.yview)
        self.pi_details_text.config(yscrollcommand=details_scroll.set)
        
        # Make text read-only by default
        self.pi_details_text.config(state=tk.DISABLED)

    def populate_pi_dropdown(self, pi_type):
        """Populate the PI component dropdown based on the selected type"""
        pi_list = []
        if pi_type in self.pi_data:
            pi_list = list(self.pi_data[pi_type].keys())
        
        if not pi_list:
            # Fallback to a default list based on type if no data is found
            if pi_type == "P0 (Raw)":
                pi_list = ["Aqueous Liquids", "Autotrophs", "Base Metals", "Carbon Compounds", "Complex Organisms",
                           "Felsic Magma", "Heavy Metals", "Ionic Solutions", "Microorganisms", "Noble Gas",
                           "Noble Metals", "Non-CS Crystals", "Planktic Colonies", "Reactive Gas", "Suspended Plasma"]
            else:
                pi_list = ["No data available"]
        
        # Update the dropdown values
        self.pi_component_combo['values'] = pi_list
        if pi_list:
            self.pi_component_var.set(pi_list[0])
            # Don't call on_pi_component_selected here to avoid initialization issues
        else:
            self.pi_component_var.set("")
            # Only display details if pi_details_text is initialized
            if hasattr(self, 'pi_details_text') and self.pi_details_text:
                self.display_pi_details("No PI components found for the selected type.")
            
    def on_pi_component_selected(self, event=None):
        """Handler for PI component selection change"""
        # Check if pi_details_text is initialized
        if not hasattr(self, 'pi_details_text') or not self.pi_details_text:
            return
            
        selected_component = self.pi_component_var.get()
        if not selected_component or not self.pi_type_var.get():
            self.display_pi_details("No component selected or type invalid.")
            return
            
        if self.pi_type_var.get() in self.pi_data and selected_component in self.pi_data[self.pi_type_var.get()]:
            component_data = self.pi_data[self.pi_type_var.get()][selected_component]
            details = f"Details for {selected_component} (Type: {self.pi_type_var.get()}):\n\n"
            
            if isinstance(component_data, dict):
                for input_name, input_quantity in component_data.items():
                    details += f"{input_name}: {input_quantity}\n"
            else:
                details += f"Value: {component_data}\n"
                
            self.display_pi_details(details)
        else:
            self.display_pi_details(f"No data available for {selected_component}")
            
    def display_pi_details(self, details):
        """Display the details of the selected PI component"""
        self.pi_details_text.config(state=tk.NORMAL)
        self.pi_details_text.delete("1.0", tk.END)
        self.pi_details_text.insert(tk.END, details)
        self.pi_details_text.config(state=tk.DISABLED)

    def on_ore_selected(self, event=None):
        """Handler for ore selection change"""
        # Automatically calculate after selecting an ore
        self.calculate_ore_refining()

    def on_ship_selected(self, event=None):
        """Handler for ship selection change"""
        selected_ship_name = self.ship_var.get()
        for module in self.discovered_modules['ships'].values():
            if module.display_name == selected_ship_name:
                # Set the ownership status in the dropdown if it exists in the module
                if hasattr(module, 'owned_status'):
                    self.ownership_var.set(module.owned_status)
                break

    def on_ownership_selected(self, event=None):
        """Handler for ship blueprint ownership selection change"""
        selected_ship_name = self.ship_var.get()
        ownership_status = self.ownership_var.get()
        for module in self.discovered_modules['ships'].values():
            if module.display_name == selected_ship_name:
                if hasattr(module, 'owned_status'):
                    module.owned_status = ownership_status
                    # Save the ownership status to configuration
                    update_blueprint_ownership(self.blueprint_config, 'ships', selected_ship_name, ownership_status)
                break

    def on_capital_ship_selected(self, event=None):
        """Handler for capital ship selection change"""
        selected_capital_ship_name = self.capital_ship_var.get()
        for module in self.discovered_modules['capital_ships'].values():
            if module.display_name == selected_capital_ship_name:
                # Set the ownership status in the dropdown if it exists in the module
                if hasattr(module, 'owned_status'):
                    self.capital_ownership_var.set(module.owned_status)
                break

    def on_capital_ownership_selected(self, event=None):
        """Handler for capital ship blueprint ownership selection change"""
        selected_capital_ship_name = self.capital_ship_var.get()
        ownership_status = self.capital_ownership_var.get()
        for module in self.discovered_modules['capital_ships'].values():
            if module.display_name == selected_capital_ship_name:
                if hasattr(module, 'owned_status'):
                    module.owned_status = ownership_status
                    # Save the ownership status to configuration
                    update_blueprint_ownership(self.blueprint_config, 'capital_ships', selected_capital_ship_name, ownership_status)
                break

    def on_component_selected(self, event=None):
        """Handler for component selection change"""
        selected_component_name = self.component_var.get()
        for module in self.discovered_modules['components'].values():
            if module.display_name == selected_component_name:
                # Set the ownership status in the dropdown if it exists in the module
                if hasattr(module, 'owned_status'):
                    self.component_ownership_var.set(module.owned_status)
                break

    def on_component_ownership_selected(self, event=None):
        """Handler for component blueprint ownership selection change"""
        selected_component_name = self.component_var.get()
        ownership_status = self.component_ownership_var.get()
        for module in self.discovered_modules['components'].values():
            if module.display_name == selected_component_name:
                if hasattr(module, 'owned_status'):
                    module.owned_status = ownership_status
                    # Save the ownership status to configuration
                    update_blueprint_ownership(self.blueprint_config, 'components', selected_component_name, ownership_status)
                break

    def on_cap_module_selected(self, event=None):
        """Handler for capital component module selection change"""
        selected_module_name = self.cap_module_var.get()
        
        # Find the selected module
        selected_module = None
        for module in self.discovered_modules['components'].values():
            if module.display_name == selected_module_name:
                selected_module = module
                break
        
        if not selected_module:
            return
            
        # Get the capital components associated with this module
        cap_component_list = []
        if 'capital_components' in self.discovered_modules:
            cap_component_list = [name for name in self.discovered_modules['capital_components'].keys()]
        
        # Update the dropdown
        self.cap_component_dropdown['values'] = cap_component_list
        if cap_component_list:
            self.cap_component_var.set(cap_component_list[0])
            self.on_cap_component_selected()
        else:
            self.cap_component_var.set("")

    def on_cap_component_selected(self, event=None):
        """Handler for capital component selection change"""
        selected_component = self.cap_component_var.get()
        
        if not selected_component or 'capital_components' not in self.discovered_modules:
            return
            
        # Get the current ownership status
        if selected_component in self.discovered_modules['capital_components']:
            component_data = self.discovered_modules['capital_components'][selected_component]
            ownership_status = component_data.get('blueprint_owned', 'Unowned')
            self.cap_component_ownership_var.set(ownership_status)
        else:
            self.cap_component_ownership_var.set('Unowned')

    def calculate_ore_refining(self):
        """Calculate minerals from ore refining"""
        ore_type = self.ore_var.get()
        quantity_str = self.quantity_var.get()
        refining_efficiency_str = self.refining_efficiency_var.get()
        
        # Validate quantity
        try:
            quantity = int(quantity_str)
        except ValueError:
            self.status_var.set("Please enter a valid number")
            return
        
        # Validate refining efficiency
        try:
            refining_efficiency = float(refining_efficiency_str)
        except ValueError:
            self.status_var.set("Please enter a valid refining efficiency")
            return
        
        # Get the minerals for the selected ore
        if ore_type in self.ore_data:
            ore_minerals = self.ore_data[ore_type]
            
            # Calculate the refined minerals
            self.ore_results_text.config(state=tk.NORMAL)
            self.ore_results_text.delete(1.0, tk.END)
            
            total_volume = quantity * 100  # Assuming 100m3 per unit
            self.ore_results_text.insert(tk.END, f"Refining {quantity:,} units of {ore_type} (total volume: {total_volume:,} m³)\n\n")
            
            # Display minerals
            self.ore_results_text.insert(tk.END, "Minerals:\n")
            for mineral, amount in ore_minerals.items():
                total = amount * quantity * (refining_efficiency / 100)
                self.ore_results_text.insert(tk.END, f"  {mineral}: {int(total):,}\n")
            
            self.ore_results_text.config(state=tk.DISABLED)
        else:
            self.status_var.set(f"No data available for {ore_type}")

    def calculate_ship_requirements(self):
        """Calculate the requirements for the selected ship"""
        selected_ship_name = self.ship_var.get()
        
        # Convert ME level to integer
        try:
            me_level = int(self.me_var.get())
        except ValueError:
            me_level = 0
        
        # Find the selected ship
        selected_ship = None
        for ship in self.discovered_modules['ships'].values():
            if ship.display_name == selected_ship_name:
                selected_ship = ship
                break
                
        if selected_ship:
            self._update_ship_requirements(selected_ship, me_level, self.ship_results_text, "Ship")
            
    def calculate_capital_ship_requirements(self):
        """Calculate the requirements for the selected capital ship"""
        selected_capital_ship_name = self.capital_ship_var.get()
        
        # Convert ME level to integer
        try:
            me_level = int(self.capital_me_var.get())
        except ValueError:
            me_level = 0
        
        # Find the selected ship
        selected_ship = None
        for ship in self.discovered_modules['capital_ships'].values():
            if ship.display_name == selected_capital_ship_name:
                selected_ship = ship
                break
                
        if selected_ship:
            self._update_ship_requirements(selected_ship, me_level, self.capital_ship_results_text, "Capital Ship")
            
    def _update_ship_requirements(self, ship, me_level, results_text, ship_type):
        """Standardized function to update ship requirements for both regular and capital ships
        
        Args:
            ship: The ship module to calculate requirements for
            me_level: Material efficiency level as integer
            results_text: The text widget to display results in
            ship_type: String describing the type of ship ("Ship" or "Capital Ship")
        """
        # Clear previous results
        results_text.config(state=tk.NORMAL)
        results_text.delete(1.0, tk.END)
        
        # Get blueprint ownership status
        ownership_status = "Unknown"
        if hasattr(ship, 'blueprint_owned'):
            ownership_status = ship.blueprint_owned
        elif hasattr(ship, 'owned_status'):
            ownership_status = ship.owned_status
        
        # Display ship information
        results_text.insert(tk.END, f"{ship_type}: {ship.display_name}\n")
        results_text.insert(tk.END, f"Blueprint Status: {ownership_status}\n")
        results_text.insert(tk.END, f"Material Efficiency: {me_level}%\n\n")
        
        # Calculate ME factor
        me_factor = 1.0 - (me_level / 100.0)
        
        # Display material requirements
        results_text.insert(tk.END, "Material Requirements:\n")
        
        if hasattr(ship, 'materials') and ship.materials:
            # Show materials with ME applied
            for material, base_quantity in ship.materials.items():
                # Apply ME calculation
                quantity = base_quantity * me_factor
                # Round up for materials
                quantity = int(quantity) if quantity == int(quantity) else int(quantity) + 1
                
                results_text.insert(tk.END, f"  • {material}: {quantity:,}\n")
        else:
            results_text.insert(tk.END, "  No material information available.\n")
            
        # Show component requirements if available
        if hasattr(ship, 'components') and ship.components:
            results_text.insert(tk.END, "\nComponent Requirements:\n")
            for component, quantity in ship.components.items():
                results_text.insert(tk.END, f"  • {component}: {quantity}\n")
        
        # Display any additional information
        if hasattr(ship, 'build_time'):
            hours = ship.build_time / 3600  # Convert seconds to hours
            results_text.insert(tk.END, f"\nBuild Time: {hours:.2f} hours\n")
            
        # Display manufacturing facility requirements if available
        if hasattr(ship, 'facility_type'):
            results_text.insert(tk.END, f"Facility Required: {ship.facility_type}\n")
            
        # Set back to read-only
        results_text.config(state=tk.DISABLED)

    def calculate_component_requirements(self):
        """Calculate the requirements for the selected component"""
        selected_component_name = self.component_var.get()
        for module in self.discovered_modules['components'].values():
            if module.display_name == selected_component_name:
                self.update_component_requirements(module)
                break

    def update_component_requirements(self, component):
        """Update the component requirements display with the selected component's information"""
        # Clear the previous content
        self.component_results_text.config(state=tk.NORMAL)
        self.component_results_text.delete(1.0, tk.END)
        
        # Show component name and blueprint status
        blueprint_status = "Unknown"
        if hasattr(component, 'blueprint_owned'):
            blueprint_status = component.blueprint_owned
        elif hasattr(component, 'owned_status'):
            blueprint_status = component.owned_status
            
        self.component_results_text.insert(tk.END, f"Component: {component.display_name}\n")
        self.component_results_text.insert(tk.END, f"Blueprint Status: {blueprint_status}\n\n")
        
        # Show material requirements
        self.component_results_text.insert(tk.END, "Material Requirements:\n")
        if hasattr(component, 'materials') and component.materials:
            for material_name, quantity in component.materials.items():
                self.component_results_text.insert(tk.END, f"  • {material_name}: {quantity:,}\n")
        else:
            self.component_results_text.insert(tk.END, "  No material information available.\n")
        
        # Disable editing
        self.component_results_text.config(state=tk.DISABLED)

    def show_about(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self)
        about_window.title("About EVE Production Calculator")
        about_window.geometry("400x300")
        
        about_text = """EVE Production Calculator
        
        A tool for calculating production requirements for items in EVE Online.
        
        Features:
        - Calculate refining yields for various ores
        - Calculate manufacturing requirements for ships and components
        - Track blueprint ownership
        - PI calculator for planetary interaction resources
        """
        
        about_label = ttk.Label(about_window, text=about_text, wraplength=380, justify=tk.CENTER)
        about_label.pack(padx=10, pady=10, expand=True)
        
        close_button = ttk.Button(about_window, text="Close", command=about_window.destroy)
        close_button.pack(pady=10)

    def reload_application(self):
        """Reload the application"""
        # Save current settings
        self.save_all_blueprint_ownership()
        
        # Show a message that the application will reload
        self.status_var.set("Application reloading...")
        self.update_idletasks()
        
        # Restart the application (this will close the current instance)
        self.destroy()
        # Start a new process with the same command line arguments
        import sys
        import subprocess
        subprocess.Popen([sys.executable] + sys.argv)
    
    def exit_application(self):
        """Exit the application after saving settings"""
        # Save current settings
        self.save_all_blueprint_ownership()
        
        # Close the application
        self.destroy()

    def on_cap_module_selected(self, event=None):
        """Handler for capital component module selection change"""
        selected_module_name = self.cap_module_var.get()
        
        # Find the selected module
        selected_module = None
        for module in self.discovered_modules['components'].values():
            if module.display_name == selected_module_name:
                selected_module = module
                break
        
        if not selected_module:
            return
            
        # Get the capital components associated with this module
        cap_component_list = []
        if 'capital_components' in self.discovered_modules:
            cap_component_list = [name for name in self.discovered_modules['capital_components'].keys()]
        
        # Update the dropdown
        self.cap_component_dropdown['values'] = cap_component_list
        if cap_component_list:
            self.cap_component_var.set(cap_component_list[0])
            self.on_cap_component_selected()
        else:
            self.cap_component_var.set("")

    def on_cap_component_selected(self, event=None):
        """Handler for capital component selection change"""
        selected_component = self.cap_component_var.get()
        
        if not selected_component or 'capital_components' not in self.discovered_modules:
            return
            
        # Get the current ownership status
        if selected_component in self.discovered_modules['capital_components']:
            component_data = self.discovered_modules['capital_components'][selected_component]
            ownership_status = component_data.get('blueprint_owned', 'Unowned')
            self.cap_component_ownership_var.set(ownership_status)
        else:
            self.cap_component_ownership_var.set('Unowned')

    def save_all_blueprint_ownership(self):
        """Save all blueprint ownership to the configuration"""
        try:
            # Save ships
            if 'ships' in self.discovered_modules:
                for ship_name, ship_module in self.discovered_modules['ships'].items():
                    if hasattr(ship_module, 'ownership_var'):
                        if isinstance(ship_module.ownership_var, tk.StringVar):
                            ownership_status = ship_module.ownership_var.get()
                        else:
                            ownership_status = ship_module.ownership_var
                            
                        # Update the module's ownership status
                        if hasattr(ship_module, 'blueprint_owned'):
                            ship_module.blueprint_owned = ownership_status
                        elif hasattr(ship_module, 'owned_status'):
                            ship_module.owned_status = ownership_status
                            
                        # Save to config
                        update_blueprint_ownership(self.blueprint_config, 'ships', ship_name, ownership_status)
            
            self.status_var.set("All blueprint ownership settings saved successfully")
        except Exception as e:
            self.status_var.set(f"Error saving blueprint ownership: {str(e)}")

    def show_blueprint_grid(self):
        """Show the blueprint grid"""
        self.blueprint_manager.show_blueprint_grid()

    def calculate_pi_requirements(self):
        """Calculate the requirements for the selected PI component"""
        selected_component = self.pi_component_var.get()
        
        if not selected_component or not self.pi_type_var.get():
            self.display_pi_details("No component selected or type invalid.")
            return
            
        if self.pi_type_var.get() in self.pi_data and selected_component in self.pi_data[self.pi_type_var.get()]:
            component_data = self.pi_data[self.pi_type_var.get()][selected_component]
            details = f"Details for {selected_component} (Type: {self.pi_type_var.get()}):\n\n"
            
            if isinstance(component_data, dict):
                for input_name, input_quantity in component_data.items():
                    details += f"{input_name}: {input_quantity}\n"
            else:
                details += f"Value: {component_data}\n"
                
            self.display_pi_details(details)
        else:
            self.display_pi_details(f"No data available for {selected_component}")

    def filter_ships(self, event=None):
        """Filter ships based on faction and ship type"""
        selected_faction = self.faction_var.get()
        selected_ship_type = self.ship_type_var.get()
        
        # Filter ships based on selected faction and type
        self.filtered_ships = []
        for ship in self.discovered_modules['ships'].values():
            faction_match = selected_faction == "All" or (hasattr(ship, 'faction') and ship.faction == selected_faction)
            type_match = selected_ship_type == "All" or (hasattr(ship, 'ship_type') and ship.ship_type == selected_ship_type)
            
            if faction_match and type_match:
                self.filtered_ships.append(ship.display_name)
        
        # Update the ship dropdown with filtered ships
        self.ship_dropdown['values'] = self.filtered_ships
        
        # Select the first ship in the filtered list if available
        if self.filtered_ships:
            self.ship_var.set(self.filtered_ships[0])
            self.on_ship_selected()
        else:
            self.ship_var.set("")
            # Clear the requirements display if no ships match the filter
            self.clear_ship_requirements()
    
    def clear_ship_requirements(self):
        """Clear the ship requirements display"""
        self.ship_results_text.config(state=tk.NORMAL)
        self.ship_results_text.delete(1.0, tk.END)
        self.ship_results_text.insert(tk.END, "No ships match the selected filters.")
        self.ship_results_text.config(state=tk.DISABLED)
