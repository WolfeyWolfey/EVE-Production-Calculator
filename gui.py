import tkinter as tk
from tkinter import ttk, messagebox, Frame
from blueprint_config import update_blueprint_ownership, get_blueprint_ownership

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
        self.capital_component_var = tk.StringVar()
        
        # Initialize variables for calculations
        self.ore_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1000")
        self.refining_efficiency_var = tk.StringVar(value="70")
        self.me_var = tk.StringVar(value="0")
        self.capital_me_var = tk.StringVar(value="0")
        
        # Initialize variables for PI calculator
        self.pi_var = tk.StringVar()
        self.tier_var = tk.StringVar(value="P0 (Raw)")
        self.pi_details_text = None  # Initialize to None first, will be set in create_pi_calculator_tab

        # Initialize variables for blueprint ownership
        self.ownership_var = tk.StringVar(value="Unowned")
        self.capital_ownership_var = tk.StringVar(value="Unowned")
        self.component_ownership_var = tk.StringVar(value="Unowned")
        self.cap_module_var = tk.StringVar()
        self.cap_component_ownership_var = tk.StringVar(value="Unowned")
        
        # Setup the main window
        self.title("EVE Online Production Calculator")
        self.geometry("800x600")

        # Create menu bar
        self.create_menu_bar()
        
        # Create tabs
        self.create_tabs()
        
        # Set up status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu_bar(self):
        """Create the menu bar for the application"""
        menu_bar = tk.Menu(self)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Blueprints", command=self.show_blueprint_grid)
        file_menu.add_command(label="Save Blueprint Ownership", command=self.save_all_blueprint_ownership)
        file_menu.add_command(label="Reload", command=self.reload_application)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menu_bar)

    def create_tabs(self):
        """Create the tabs for the calculator"""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.ore_calculator_tab = ttk.Frame(self.notebook)
        self.ship_calculator_tab = ttk.Frame(self.notebook)
        self.component_calculator_tab = ttk.Frame(self.notebook)
        self.pi_calculator_tab = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.ore_calculator_tab, text="Ore Calculator")
        self.notebook.add(self.ship_calculator_tab, text="Ship Calculator")
        self.notebook.add(self.component_calculator_tab, text="Component Calculator")
        self.notebook.add(self.pi_calculator_tab, text="PI Calculator")

        # Create content for each tab
        self.create_ore_calculator_tab()
        self.create_ship_calculator_tab()
        self.create_component_calculator_tab()
        self.create_pi_calculator_tab()

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

        # Ship selection
        ship_label = ttk.Label(ship_selection_frame, text="Select Ship:")
        ship_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        ship_list = [module.display_name for module in self.discovered_modules['ships'].values()]
        self.ship_var.set(ship_list[0] if ship_list else "")
        ship_dropdown = ttk.Combobox(ship_selection_frame, textvariable=self.ship_var, values=ship_list, state="readonly")
        ship_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ship_dropdown.bind("<<ComboboxSelected>>", self.on_ship_selected)

        # Material Efficiency selection
        me_label = ttk.Label(ship_selection_frame, text="Material Efficiency (ME):")
        me_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        me_dropdown = ttk.Combobox(ship_selection_frame, textvariable=self.me_var, values=list(range(11)), state="readonly")
        me_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Calculate button
        calculate_button = ttk.Button(ship_selection_frame, text="Calculate Requirements", command=self.calculate_ship_requirements)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

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

        # Frame for results
        results_frame = ttk.LabelFrame(self.component_calculator_tab, text="Component Requirements")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable results area
        self.component_results_text = tk.Text(results_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.component_results_text.yview)
        self.component_results_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.component_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_pi_calculator_tab(self):
        """Create the PI calculator tab"""
        # Frame for PI component selection
        pi_selection_frame = ttk.LabelFrame(self.pi_calculator_tab, text="Select PI Component")
        pi_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Tier selection
        tier_label = ttk.Label(pi_selection_frame, text="Select Tier:")
        tier_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        tier_list = ["P0 (Raw)", "P1 (Processed)", "P2 (Refined)", "P3 (Specialized)", "P4 (Advanced)"]
        self.tier_var.set(tier_list[0])
        tier_dropdown = ttk.Combobox(pi_selection_frame, textvariable=self.tier_var, values=tier_list, state="readonly")
        tier_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        tier_dropdown.bind("<<ComboboxSelected>>", self.on_tier_selected)

        # PI Component selection
        pi_label = ttk.Label(pi_selection_frame, text="Select PI Component:")
        pi_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        # Set up the PI dropdown without initializing the list yet
        self.pi_dropdown = ttk.Combobox(pi_selection_frame, textvariable=self.pi_var, state="readonly")
        self.pi_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.pi_dropdown.bind("<<ComboboxSelected>>", self.on_pi_component_selected)

        # Frame for PI component details
        pi_details_frame = ttk.LabelFrame(self.pi_calculator_tab, text="PI Component Details")
        pi_details_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable details area
        self.pi_details_text = tk.Text(pi_details_frame, height=10, width=40, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(pi_details_frame, orient="vertical", command=self.pi_details_text.yview)
        self.pi_details_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pi_details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize the PI component dropdown after all UI elements are created
        self.populate_pi_dropdown("P0 (Raw)")

    def populate_pi_dropdown(self, tier):
        """Populate the PI component dropdown based on the selected tier"""
        tier_to_data = {
            "P0 (Raw)": "p0_materials",
            "P1 (Processed)": "p1_materials",
            "P2 (Refined)": "p2_materials", 
            "P3 (Specialized)": "p3_materials",
            "P4 (Advanced)": "p4_materials"
        }
        
        pi_list = []
        tier_key = tier_to_data.get(tier)
        
        if tier_key and self.pi_data and tier_key in self.pi_data:
            pi_list = list(self.pi_data[tier_key].keys())
        
        if not pi_list:
            # Fallback to a default list based on tier if no data is found
            if tier == "P0 (Raw)":
                pi_list = ["Aqueous Liquids", "Autotrophs", "Base Metals", "Carbon Compounds", "Complex Organisms",
                           "Felsic Magma", "Heavy Metals", "Ionic Solutions", "Microorganisms", "Noble Gas",
                           "Noble Metals", "Non-CS Crystals", "Planktic Colonies", "Reactive Gas", "Suspended Plasma"]
            else:
                pi_list = ["No data available"]
        
        # Update the dropdown values
        self.pi_dropdown['values'] = pi_list
        if pi_list:
            self.pi_var.set(pi_list[0])
            # Don't call on_pi_component_selected here to avoid initialization issues
        else:
            self.pi_var.set("")
            # Only display details if pi_details_text is initialized
            if hasattr(self, 'pi_details_text') and self.pi_details_text:
                self.display_pi_details("No PI components found for the selected tier.")
            
    def on_tier_selected(self, event=None):
        """Handler for tier selection change"""
        selected_tier = self.tier_var.get()
        self.populate_pi_dropdown(selected_tier)
        
    def on_pi_component_selected(self, event=None):
        """Handler for PI component selection change"""
        # Check if pi_details_text is initialized
        if not hasattr(self, 'pi_details_text') or not self.pi_details_text:
            return
            
        selected_component = self.pi_var.get()
        tier_to_data = {
            "P0 (Raw)": "p0_materials",
            "P1 (Processed)": "p1_materials",
            "P2 (Refined)": "p2_materials", 
            "P3 (Specialized)": "p3_materials",
            "P4 (Advanced)": "p4_materials"
        }
        tier_key = tier_to_data.get(self.tier_var.get())
        
        if not selected_component or not tier_key:
            self.display_pi_details("No component selected or tier invalid.")
            return
            
        if tier_key in self.pi_data and selected_component in self.pi_data[tier_key]:
            component_data = self.pi_data[tier_key][selected_component]
            details = f"Details for {selected_component} (Tier: {self.tier_var.get()}):\n\n"
            
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
                self.update_ship_requirements(module, self.me_var.get())
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
                    update_blueprint_ownership('ships', selected_ship_name, ownership_status, self.blueprint_config)
                break

    def on_capital_ship_selected(self, event=None):
        """Handler for capital ship selection change"""
        selected_capital_ship_name = self.capital_ship_var.get()
        for module in self.discovered_modules['capital_ships'].values():
            if module.display_name == selected_capital_ship_name:
                # Set the ownership status in the dropdown if it exists in the module
                if hasattr(module, 'owned_status'):
                    self.capital_ownership_var.set(module.owned_status)
                self.update_capital_ship_requirements(module, self.capital_me_var.get())
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
                    update_blueprint_ownership('capital_ships', selected_capital_ship_name, ownership_status, self.blueprint_config)
                break

    def on_component_selected(self, event=None):
        """Handler for component selection change"""
        selected_component_name = self.component_var.get()
        for module in self.discovered_modules['components'].values():
            if module.display_name == selected_component_name:
                # Set the ownership status in the dropdown if it exists in the module
                if hasattr(module, 'owned_status'):
                    self.component_ownership_var.set(module.owned_status)
                self.update_component_requirements(module)
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
                    update_blueprint_ownership('components', selected_component_name, ownership_status, self.blueprint_config)
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
        
        if selected_module and hasattr(selected_module, 'capital_component_data'):
            # Update the component dropdown with available components
            component_list = list(selected_module.capital_component_data.keys())
            self.cap_component_dropdown['values'] = component_list
            if component_list:
                self.cap_component_var.set(component_list[0])
                self.on_cap_component_selected()
        else:
            self.cap_component_dropdown['values'] = []
            self.cap_component_var.set("")
            self.cap_component_ownership_var.set("Unowned")

    def on_cap_component_selected(self, event=None):
        """Handler for individual capital component selection change"""
        selected_module_name = self.cap_module_var.get()
        selected_component_name = self.cap_component_var.get()
        
        if not selected_component_name:
            return
        
        # Find the selected module and component
        for module in self.discovered_modules['components'].values():
            if module.display_name == selected_module_name:
                if hasattr(module, 'capital_component_data') and selected_component_name in module.capital_component_data:
                    component_data = module.capital_component_data[selected_component_name]
                    # Get current ownership status
                    ownership_status = component_data.get("blueprint_owned", "Unowned")
                    self.cap_component_ownership_var.set(ownership_status)
                break

    def on_cap_component_ownership_selected(self):
        """Handler for individual capital component ownership selection change"""
        selected_module_name = self.cap_module_var.get()
        selected_component_name = self.cap_component_var.get()
        ownership_status = self.cap_component_ownership_var.get()
        
        if not selected_component_name or not selected_module_name:
            return
        
        # Find the selected module and update component ownership
        for module in self.discovered_modules['components'].values():
            if module.display_name == selected_module_name:
                if hasattr(module, 'capital_component_data') and selected_component_name in module.capital_component_data:
                    # Update in memory
                    module.capital_component_data[selected_component_name]["blueprint_owned"] = ownership_status
                    
                    # Save to configuration
                    component_key = f"{selected_module_name}:{selected_component_name}"
                    update_blueprint_ownership('components', component_key, ownership_status, self.blueprint_config)
                    
                    # Show confirmation message
                    self.status_var.set(f"Updated ownership for {selected_component_name} to {ownership_status}")
                break

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
        
        # Add each requirement with ownership status
        if hasattr(component_module, 'capital_component_data'):
            for component_name, component_data in component_module.capital_component_data.items():
                ownership_status = component_data.get("blueprint_owned", "Unowned")
                ownership_text = f"[{ownership_status}]"
                self.component_results_text.insert(tk.END, f"{component_name} {ownership_text}\n")
                
                # Add mineral requirements
                if "minerals" in component_data:
                    self.component_results_text.insert(tk.END, "  Minerals:\n")
                    for mineral, amount in component_data["minerals"].items():
                        self.component_results_text.insert(tk.END, f"    {mineral}: {amount:,}\n")
                
                # Add PI material requirements
                if "pi_materials" in component_data and component_data["pi_materials"]:
                    self.component_results_text.insert(tk.END, "  PI Materials:\n")
                    for material, amount in component_data["pi_materials"].items():
                        self.component_results_text.insert(tk.END, f"    {material}: {amount}\n")
                
                self.component_results_text.insert(tk.END, "\n")
        else:
            self.component_results_text.insert(tk.END, "No component data available\n")
        
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

    def calculate_pi_requirements(self):
        """Calculate the requirements for the selected PI component"""
        pi_component = self.pi_var.get()
        if self.pi_data:
            for level in ['p0_materials', 'p1_materials', 'p2_materials', 'p3_materials', 'p4_materials']:
                if level in self.pi_data and pi_component in self.pi_data[level]:
                    self.pi_details_text.config(state=tk.NORMAL)
                    self.pi_details_text.delete("1.0", tk.END)
                    self.pi_details_text.insert(tk.END, f"Requirements for {pi_component}:\n\n")
                    for material, amount in self.pi_data[level][pi_component].items():
                        self.pi_details_text.insert(tk.END, f"{material}: {amount}\n")
                    self.pi_details_text.config(state=tk.DISABLED)
                    return
        self.pi_details_text.config(state=tk.NORMAL)
        self.pi_details_text.delete("1.0", tk.END)
        self.pi_details_text.insert(tk.END, "No requirements found for the selected PI component.")
        self.pi_details_text.config(state=tk.DISABLED)

    def create_blueprint_management_tab(self):
        """Create the blueprint management tab"""
        # Create a notebook for blueprint management
        blueprint_notebook = ttk.Notebook(self.blueprint_management_tab)
        blueprint_notebook.pack(fill="both", expand=True)
        
        # Create tabs for each type of blueprint
        ships_tab = ttk.Frame(blueprint_notebook)
        capital_ships_tab = ttk.Frame(blueprint_notebook)
        components_tab = ttk.Frame(blueprint_notebook)
        capital_components_tab = ttk.Frame(blueprint_notebook)
        
        # Add tabs to notebook
        blueprint_notebook.add(ships_tab, text="Ships")
        blueprint_notebook.add(capital_ships_tab, text="Capital Ships")
        blueprint_notebook.add(components_tab, text="Components")
        blueprint_notebook.add(capital_components_tab, text="Capital Components")
        
        # Create content for each tab
        self.create_ships_blueprint_tab(ships_tab)
        self.create_capital_ships_blueprint_tab(capital_ships_tab)
        self.create_components_blueprint_tab(components_tab)
        self.create_capital_components_blueprint_tab(capital_components_tab)

    def create_ships_blueprint_tab(self, parent_tab):
        """Create the ships blueprint tab"""
        # Frame for ship blueprint selection
        ship_frame = ttk.LabelFrame(parent_tab, text="Select Ship")
        ship_frame.pack(fill="x", expand=False, padx=10, pady=10)
        
        # Ship selection
        ship_label = ttk.Label(ship_frame, text="Select Ship:")
        ship_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        ship_list = [module.display_name for module in self.discovered_modules['ships'].values()]
        self.ship_var.set(ship_list[0] if ship_list else "")
        ship_dropdown = ttk.Combobox(ship_frame, textvariable=self.ship_var, values=ship_list, state="readonly")
        ship_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Ownership selection
        ownership_label = ttk.Label(ship_frame, text="Blueprint Status:")
        ownership_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        ownership_options = ["Unowned", "Owned", "Invented"]
        self.ownership_var.set(ownership_options[0])
        ownership_dropdown = ttk.Combobox(ship_frame, textvariable=self.ownership_var, values=ownership_options, state="readonly")
        ownership_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Save button
        save_button = ttk.Button(ship_frame, text="Save", command=self.save_ship_ownership)
        save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def create_capital_ships_blueprint_tab(self, parent_tab):
        """Create the capital ships blueprint tab"""
        # Frame for capital ship blueprint selection
        cap_ship_frame = ttk.LabelFrame(parent_tab, text="Select Capital Ship")
        cap_ship_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Capital Ship selection
        cap_ship_label = ttk.Label(cap_ship_frame, text="Select Capital Ship:")
        cap_ship_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        cap_ship_list = [module.display_name for module in self.discovered_modules['capital_ships'].values()]
        self.capital_ship_var.set(cap_ship_list[0] if cap_ship_list else "")
        cap_ship_dropdown = ttk.Combobox(cap_ship_frame, textvariable=self.capital_ship_var, values=cap_ship_list, state="readonly")
        cap_ship_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Ownership selection
        ownership_label = ttk.Label(cap_ship_frame, text="Blueprint Status:")
        ownership_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        ownership_options = ["Unowned", "Owned", "Invented"]
        self.capital_ownership_var.set(ownership_options[0])
        ownership_dropdown = ttk.Combobox(cap_ship_frame, textvariable=self.capital_ownership_var, values=ownership_options, state="readonly")
        ownership_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Save button
        save_button = ttk.Button(cap_ship_frame, text="Save", command=self.save_capital_ship_ownership)
        save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
    def create_components_blueprint_tab(self, parent_tab):
        """Create the components blueprint tab"""
        # Frame for component blueprint selection
        component_frame = ttk.LabelFrame(parent_tab, text="Select Component")
        component_frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Component selection
        component_label = ttk.Label(component_frame, text="Select Component:")
        component_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        component_list = [module.display_name for module in self.discovered_modules['components'].values()]
        self.component_var.set(component_list[0] if component_list else "")
        component_dropdown = ttk.Combobox(component_frame, textvariable=self.component_var, values=component_list, state="readonly")
        component_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Ownership selection
        ownership_label = ttk.Label(component_frame, text="Blueprint Status:")
        ownership_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        ownership_options = ["Unowned", "Owned", "Invented"]
        self.component_ownership_var.set(ownership_options[0])
        ownership_dropdown = ttk.Combobox(component_frame, textvariable=self.component_ownership_var, values=ownership_options, state="readonly")
        ownership_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Save button
        save_button = ttk.Button(component_frame, text="Save", command=self.save_component_ownership)
        save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
    def create_capital_components_blueprint_tab(self, parent_tab):
        """Create the capital components blueprint tab"""
        # Frame for individual capital component selection
        cap_component_selection_frame = ttk.LabelFrame(parent_tab, text="Select Individual Capital Component")
        cap_component_selection_frame.pack(fill="x", expand=False, padx=10, pady=10)
        
        # Component module selection
        cap_module_label = ttk.Label(cap_component_selection_frame, text="Select Component Module:")
        cap_module_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        component_list = [module.display_name for module in self.discovered_modules['components'].values()]
        self.cap_module_var.set(component_list[0] if component_list else "")
        cap_module_dropdown = ttk.Combobox(cap_component_selection_frame, textvariable=self.cap_module_var, values=component_list, state="readonly")
        cap_module_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        cap_module_dropdown.bind("<<ComboboxSelected>>", self.on_cap_module_selected)
        
        # Individual component selection
        cap_component_label = ttk.Label(cap_component_selection_frame, text="Select Component:")
        cap_component_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Initially empty, will be populated on module selection
        self.cap_component_var.set("")
        self.cap_component_dropdown = ttk.Combobox(cap_component_selection_frame, textvariable=self.cap_component_var, state="readonly")
        self.cap_component_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.cap_component_dropdown.bind("<<ComboboxSelected>>", self.on_cap_component_selected)
        
        # Ownership selection for individual component
        cap_component_ownership_label = ttk.Label(cap_component_selection_frame, text="Blueprint Status:")
        cap_component_ownership_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.cap_component_ownership_var.set("Unowned")
        cap_component_ownership_dropdown = ttk.Combobox(cap_component_selection_frame, textvariable=self.cap_component_ownership_var, values=["Unowned", "Owned", "Invented"], state="readonly")
        cap_component_ownership_dropdown.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Save button
        save_button = ttk.Button(cap_component_selection_frame, text="Save", command=self.save_capital_component_ownership)
        save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        # Initialize individual capital components
        if component_list:
            self.on_cap_module_selected()
        
        # Close button
        close_button = ttk.Button(parent_tab, text="Close", command=parent_tab.destroy)
        close_button.pack(pady=10)

    def save_ship_ownership(self):
        """
        This method is no longer used - replaced by the grid view
        Kept for backward compatibility
        """
        pass
        
    def save_capital_ship_ownership(self):
        """
        This method is no longer used - replaced by the grid view
        Kept for backward compatibility
        """
        pass
        
    def save_component_ownership(self):
        """
        This method is no longer used - replaced by the grid view
        Kept for backward compatibility
        """
        pass
        
    def save_capital_component_ownership(self):
        """
        This method is no longer used - replaced by the grid view
        Kept for backward compatibility
        """
        pass

    def update_module_ownership(self, module, ownership_status):
        """Update ownership status for a module and save it"""
        module_type = None
        module_name = None
        
        # Determine module type from where it's found in discovered_modules
        for category, modules in self.discovered_modules.items():
            if category in ['ships', 'capital_ships', 'components']:
                for name, mod in modules.items():
                    if mod == module:
                        module_type = category
                        module_name = name
                        break
                if module_type:
                    break
        
        if module_type and module_name:
            # Update ownership in the module based on which attribute it has
            if hasattr(module, 'blueprint_owned'):
                module.blueprint_owned = ownership_status
            elif hasattr(module, 'owned_status'):
                module.owned_status = ownership_status
            else:
                # Add the attribute if it doesn't exist
                module.owned_status = ownership_status
                
            # Save to config
            update_blueprint_ownership(self.blueprint_config, module_type, module_name, ownership_status)
            self.status_var.set(f"Updated ownership for {module.display_name} to {ownership_status}")
        else:
            self.status_var.set(f"Could not determine module type for {getattr(module, 'display_name', 'unknown module')}")
            
    def update_cap_component_ownership(self, component_name, component_data, ownership_status):
        """Update ownership status for a capital component"""
        if 'capital_components' in self.discovered_modules and component_name in self.discovered_modules['capital_components']:
            # Update the ownership in the component data
            component_data['ownership_var'].set(ownership_status)
            self.discovered_modules['capital_components'][component_name]['blueprint_owned'] = ownership_status
            # Save to config
            update_blueprint_ownership(self.blueprint_config, 'capital_components', component_name, ownership_status)
            self.status_var.set(f"Updated ownership for {component_name} to {ownership_status}")
        else:
            self.status_var.set(f"Component {component_name} not found")
            
    def save_all_blueprint_ownership(self):
        """Save all blueprint ownership to the configuration"""
        try:
            # Save ships
            if 'ships' in self.discovered_modules:
                for ship_name, ship_module in self.discovered_modules['ships'].items():
                    if hasattr(ship_module, 'ownership_var'):
                        ownership_status = ship_module.ownership_var.get()
                        # Update ownership in the module based on which attribute it has
                        if hasattr(ship_module, 'blueprint_owned'):
                            ship_module.blueprint_owned = ownership_status
                        elif hasattr(ship_module, 'owned_status'):
                            ship_module.owned_status = ownership_status
                        update_blueprint_ownership(self.blueprint_config, 'ships', ship_name, ownership_status)
            
            # Save capital ships
            if 'capital_ships' in self.discovered_modules:
                for ship_name, ship_module in self.discovered_modules['capital_ships'].items():
                    if hasattr(ship_module, 'ownership_var'):
                        ownership_status = ship_module.ownership_var.get()
                        # Update ownership in the module based on which attribute it has
                        if hasattr(ship_module, 'blueprint_owned'):
                            ship_module.blueprint_owned = ownership_status
                        elif hasattr(ship_module, 'owned_status'):
                            ship_module.owned_status = ownership_status
                        update_blueprint_ownership(self.blueprint_config, 'capital_ships', ship_name, ownership_status)
            
            # Save components
            if 'components' in self.discovered_modules:
                for comp_name, comp_module in self.discovered_modules['components'].items():
                    if hasattr(comp_module, 'ownership_var'):
                        ownership_status = comp_module.ownership_var.get()
                        # Update ownership in the module based on which attribute it has
                        if hasattr(comp_module, 'blueprint_owned'):
                            comp_module.blueprint_owned = ownership_status
                        elif hasattr(comp_module, 'owned_status'):
                            comp_module.owned_status = ownership_status
                        update_blueprint_ownership(self.blueprint_config, 'components', comp_name, ownership_status)
            
            # Save capital components
            if 'capital_components' in self.discovered_modules:
                for comp_name, comp_data in self.discovered_modules['capital_components'].items():
                    if 'ownership_var' in comp_data:
                        ownership_status = comp_data['ownership_var'].get()
                        comp_data['blueprint_owned'] = ownership_status
                        update_blueprint_ownership(self.blueprint_config, 'capital_components', comp_name, ownership_status)
            
            self.status_var.set("All blueprint ownership settings saved successfully")
        except Exception as e:
            self.status_var.set(f"Error saving blueprint ownership: {str(e)}")
    
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
        for module_name, module in self.discovered_modules['components'].items():
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

    def show_blueprint_grid(self):
        """Show blueprint ownership in an Excel-like grid"""
        blueprint_window = tk.Toplevel(self)
        blueprint_window.title("Blueprint Ownership Management")
        blueprint_window.geometry("800x600")
        
        # Create a notebook for categorized blueprint management
        blueprint_notebook = ttk.Notebook(blueprint_window)
        blueprint_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs for different blueprint types
        ships_tab = ttk.Frame(blueprint_notebook)
        capital_ships_tab = ttk.Frame(blueprint_notebook)
        components_tab = ttk.Frame(blueprint_notebook)
        capital_components_tab = ttk.Frame(blueprint_notebook)
        
        # Add tabs to notebook
        blueprint_notebook.add(ships_tab, text="Ships")
        blueprint_notebook.add(capital_ships_tab, text="Capital Ships")
        blueprint_notebook.add(components_tab, text="Components")
        blueprint_notebook.add(capital_components_tab, text="Capital Components")
        
        # Create grids for each tab
        self.create_ship_blueprint_grid(ships_tab)
        self.create_capital_ship_blueprint_grid(capital_ships_tab)
        self.create_component_blueprint_grid(components_tab)
        self.create_capital_component_blueprint_grid(capital_components_tab)
        
        # Add save button
        save_button = ttk.Button(blueprint_window, text="Save All", command=self.save_all_blueprint_ownership)
        save_button.pack(pady=10)
        
    def create_ship_blueprint_grid(self, parent_tab):
        """Create a grid for ship blueprints"""
        # Create a frame with scrollbar
        frame = ttk.Frame(parent_tab)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create a frame inside the canvas to hold the grid
        grid_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        
        # Create header row
        ttk.Label(grid_frame, text="Blueprint Name", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(grid_frame, text="Unowned", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(grid_frame, text="Owned", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(grid_frame, text="Invented", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
        
        # Add separator
        separator = ttk.Separator(grid_frame, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=2)
        
        # Populate grid with ships
        row = 2
        if 'ships' in self.discovered_modules:
            for ship_name, ship_module in self.discovered_modules['ships'].items():
                # Create a variable to track the radio button state
                if not hasattr(ship_module, 'ownership_var'):
                    # Check if the module has blueprint_owned or owned_status attribute
                    if hasattr(ship_module, 'blueprint_owned'):
                        blueprint_status = ship_module.blueprint_owned
                    elif hasattr(ship_module, 'owned_status'):
                        blueprint_status = ship_module.owned_status
                    else:
                        blueprint_status = "Unowned"
                    
                    ship_module.ownership_var = tk.StringVar(value=blueprint_status)
                
                # Add ship name and radio buttons
                ttk.Label(grid_frame, text=ship_module.display_name).grid(row=row, column=0, padx=5, pady=2, sticky="w")
                ttk.Radiobutton(grid_frame, variable=ship_module.ownership_var, value="Unowned", 
                               command=lambda m=ship_module: self.update_module_ownership(m, "Unowned")).grid(row=row, column=1, padx=5, pady=2)
                ttk.Radiobutton(grid_frame, variable=ship_module.ownership_var, value="Owned", 
                               command=lambda m=ship_module: self.update_module_ownership(m, "Owned")).grid(row=row, column=2, padx=5, pady=2)
                ttk.Radiobutton(grid_frame, variable=ship_module.ownership_var, value="Invented", 
                               command=lambda m=ship_module: self.update_module_ownership(m, "Invented")).grid(row=row, column=3, padx=5, pady=2)
                
                row += 1
        
        # Configure the canvas to adjust scrolling based on the grid size
        grid_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
    def create_capital_ship_blueprint_grid(self, parent_tab):
        """Create a grid for capital ship blueprints"""
        # Create a frame with scrollbar
        frame = ttk.Frame(parent_tab)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create a frame inside the canvas to hold the grid
        grid_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        
        # Create header row
        ttk.Label(grid_frame, text="Blueprint Name", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(grid_frame, text="Unowned", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(grid_frame, text="Owned", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(grid_frame, text="Invented", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
        
        # Add separator
        separator = ttk.Separator(grid_frame, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=2)
        
        # Populate grid with capital ships
        row = 2
        if 'capital_ships' in self.discovered_modules:
            for ship_name, ship_module in self.discovered_modules['capital_ships'].items():
                # Create a variable to track the radio button state
                if not hasattr(ship_module, 'ownership_var'):
                    # Check if the module has blueprint_owned or owned_status attribute
                    if hasattr(ship_module, 'blueprint_owned'):
                        blueprint_status = ship_module.blueprint_owned
                    elif hasattr(ship_module, 'owned_status'):
                        blueprint_status = ship_module.owned_status
                    else:
                        blueprint_status = "Unowned"
                    
                    ship_module.ownership_var = tk.StringVar(value=blueprint_status)
                
                # Add ship name and radio buttons
                ttk.Label(grid_frame, text=ship_module.display_name).grid(row=row, column=0, padx=5, pady=2, sticky="w")
                ttk.Radiobutton(grid_frame, variable=ship_module.ownership_var, value="Unowned", 
                               command=lambda m=ship_module: self.update_module_ownership(m, "Unowned")).grid(row=row, column=1, padx=5, pady=2)
                ttk.Radiobutton(grid_frame, variable=ship_module.ownership_var, value="Owned", 
                               command=lambda m=ship_module: self.update_module_ownership(m, "Owned")).grid(row=row, column=2, padx=5, pady=2)
                ttk.Radiobutton(grid_frame, variable=ship_module.ownership_var, value="Invented", 
                               command=lambda m=ship_module: self.update_module_ownership(m, "Invented")).grid(row=row, column=3, padx=5, pady=2)
                
                row += 1
        
        # Configure the canvas to adjust scrolling based on the grid size
        grid_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
    def create_component_blueprint_grid(self, parent_tab):
        """Create a grid for component blueprints"""
        # Create a frame with scrollbar
        frame = ttk.Frame(parent_tab)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create a frame inside the canvas to hold the grid
        grid_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        
        # Create header row
        ttk.Label(grid_frame, text="Blueprint Name", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(grid_frame, text="Unowned", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(grid_frame, text="Owned", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(grid_frame, text="Invented", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
        
        # Add separator
        separator = ttk.Separator(grid_frame, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=2)
        
        # Populate grid with components
        row = 2
        if 'components' in self.discovered_modules:
            for comp_name, comp_module in self.discovered_modules['components'].items():
                # Create a variable to track the radio button state
                if not hasattr(comp_module, 'ownership_var'):
                    # Check if the module has blueprint_owned or owned_status attribute
                    if hasattr(comp_module, 'blueprint_owned'):
                        blueprint_status = comp_module.blueprint_owned
                    elif hasattr(comp_module, 'owned_status'):
                        blueprint_status = comp_module.owned_status
                    else:
                        blueprint_status = "Unowned"
                    
                    comp_module.ownership_var = tk.StringVar(value=blueprint_status)
                
                # Add component name and radio buttons
                ttk.Label(grid_frame, text=comp_module.display_name).grid(row=row, column=0, padx=5, pady=2, sticky="w")
                ttk.Radiobutton(grid_frame, variable=comp_module.ownership_var, value="Unowned", 
                               command=lambda m=comp_module: self.update_module_ownership(m, "Unowned")).grid(row=row, column=1, padx=5, pady=2)
                ttk.Radiobutton(grid_frame, variable=comp_module.ownership_var, value="Owned", 
                               command=lambda m=comp_module: self.update_module_ownership(m, "Owned")).grid(row=row, column=2, padx=5, pady=2)
                ttk.Radiobutton(grid_frame, variable=comp_module.ownership_var, value="Invented", 
                               command=lambda m=comp_module: self.update_module_ownership(m, "Invented")).grid(row=row, column=3, padx=5, pady=2)
                
                row += 1
        
        # Configure the canvas to adjust scrolling based on the grid size
        grid_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
    def create_capital_component_blueprint_grid(self, parent_tab):
        """Create a grid for capital component blueprints"""
        # Create a frame with scrollbar
        frame = ttk.Frame(parent_tab)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create a frame inside the canvas to hold the grid
        grid_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        
        # Create header row
        ttk.Label(grid_frame, text="Blueprint Name", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(grid_frame, text="Unowned", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(grid_frame, text="Owned", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(grid_frame, text="Invented", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
        
        # Add separator
        separator = ttk.Separator(grid_frame, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=2)
        
        # Populate grid with capital components
        row = 2
        if 'capital_components' in self.discovered_modules:
            for comp_name, comp_data in self.discovered_modules['capital_components'].items():
                # Create a variable to track the radio button state
                if 'ownership_var' not in comp_data:
                    comp_data['ownership_var'] = tk.StringVar(value=comp_data.get('blueprint_owned', 'Unowned'))
                
                # Add component name and radio buttons
                ttk.Label(grid_frame, text=comp_name).grid(row=row, column=0, padx=5, pady=2, sticky="w")
                ttk.Radiobutton(grid_frame, variable=comp_data['ownership_var'], value="Unowned",
                               command=lambda n=comp_name, d=comp_data: self.update_cap_component_ownership(n, d, "Unowned")).grid(row=row, column=1, padx=5, pady=2)
                ttk.Radiobutton(grid_frame, variable=comp_data['ownership_var'], value="Owned",
                               command=lambda n=comp_name, d=comp_data: self.update_cap_component_ownership(n, d, "Owned")).grid(row=row, column=2, padx=5, pady=2)
                ttk.Radiobutton(grid_frame, variable=comp_data['ownership_var'], value="Invented",
                               command=lambda n=comp_name, d=comp_data: self.update_cap_component_ownership(n, d, "Invented")).grid(row=row, column=3, padx=5, pady=2)
                
                row += 1
        
        # Configure the canvas to adjust scrolling based on the grid size
        grid_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

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
