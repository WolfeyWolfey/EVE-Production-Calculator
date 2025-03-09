
import tkinter as tk
from tkinter import ttk

# Data from the provided text
ore_data = {
    "Veldspar": {"Tritanium": 400},
    "Scordite": {"Tritanium": 150, "Pyerite": 90},
    "Pyroxeres": {"Pyerite": 90, "Mexallon": 30},
    "Plagioclase": {"Tritanium": 175, "Mexallon": 70},
    "Omber": {"Pyerite": 90, "Isogen": 75},
    "Kernite": {"Mexallon": 60, "Isogen": 120},
    "Jaspet": {"Mexallon": 150, "Nocxium": 50},
    "Hemorphite": {"Isogen": 90, "Nocxium": 240},
    "Hedbergite": {"Pyerite": 450, "Nocxium": 120},
    "Gneiss": {"Pyerite": 2000, "Mexallon": 1500, "Isogen": 800},
    "Dark Ochre": {"Mexallon": 1360, "Isogen": 1200, "Nocxium": 320},
    "Crokite": {"Pyerite": 800, "Mexallon": 2000, "Nocxium": 800},
    "Bistot": {"Pyerite": 3200, "Mexallon": 1200, "Zydrine": 160},
    "Arkonor": {"Pyerite": 3200, "Mexallon": 1200, "Megacyte": 120},
    "Spodumain": {"Tritanium": 48000, "Pyerite": 1000, "Mexallon": 160, "Isogen": 80, "Nocxium": 40},
    "Mercoxit": {"Morphite": 140}
}

retriever_requirements = {
    "Tritanium": 2742672,
    "Pyerite": 755721,
    "Mexallon": 86574,
    "Isogen": 57980,
    "Nocxium": 4937,
    "Zydrine": 2002,
    "Megacyte": 643
}

capital_component_data = {
    "Capital Propulsion Engine": {
        "minerals": {"Tritanium": 457050, "Pyerite": 110416, "Mexallon": 41994, "Isogen": 6938, "Nocxium": 2110, "Zydrine": 604, "Megacyte": 302},
        "pi_materials": {"Self-Harmonizing Power Core": 1}
    },
    "Capital Armor Plates": {
        "minerals": {"Tritanium": 473141, "Pyerite": 111118, "Mexallon": 43324, "Isogen": 7109, "Nocxium": 2141, "Zydrine": 682, "Megacyte": 304},
        "pi_materials": {"Organic Mortar Applicators": 5}
    },
    "Capital Shield Emitter": {
        "minerals": {"Tritanium": 400000, "Pyerite": 100000},  # Example values, needs to be updated with actual data
        "pi_materials": {"Recursive Computing Module": 1}
    },
    "Capital Cargo Bay": {
        "minerals": {"Tritanium": 874902, "Pyerite": 72154, "Mexallon": 24616, "Isogen": 3504, "Nocxium": 998, "Zydrine": 286, "Megacyte": 64},
        "pi_materials": {}
    },
    "Capital Construction Parts": {
        "minerals": {"Tritanium": 349387, "Pyerite": 84399, "Mexallon": 33956, "Isogen": 4594, "Nocxium": 1377, "Zydrine": 242, "Megacyte": 95},
        "pi_materials": {}
    },
    "Capital Ship Maintenance Bay": {
        "minerals": {"Tritanium": 519083, "Pyerite": 170948, "Mexallon": 47981, "Isogen": 8109, "Nocxium": 2215, "Zydrine": 411, "Megacyte": 187},
        "pi_materials": {"Integrity Response Drones": 1}
    }
}

bowhead_requirements = {
    "Capital Propulsion Engine": 10,
    "Capital Armor Plates": 5,
    "Capital Shield Emitter": 5,
    "Capital Cargo Bay": 8,
    "Capital Construction Parts": 5,
    "Capital Ship Maintenance Bay": 7
}


class EveProductionCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("EVE Online Production Calculator")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.ore_refining_tab = ttk.Frame(self.notebook)
        self.retriever_tab = ttk.Frame(self.notebook)
        self.bowhead_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.ore_refining_tab, text="Ore Refining")
        self.notebook.add(self.retriever_tab, text="Retriever Production")
        self.notebook.add(self.bowhead_tab, text="Bowhead Production")

        self.create_ore_refining_tab()
        self.create_retriever_tab()
        self.create_bowhead_tab()

    def create_ore_refining_tab(self):
        # Ore Refining Tab Content
        ore_label = tk.Label(self.ore_refining_tab, text="Select Ore:")
        ore_label.pack()

        ore_list = list(ore_data.keys())
        self.ore_var = tk.StringVar(value=ore_list[0])
        ore_dropdown = tk.OptionMenu(self.ore_refining_tab, self.ore_var, *ore_list)
        ore_dropdown.pack()

        quantity_label = tk.Label(self.ore_refining_tab, text="Enter Quantity:")
        quantity_label.pack()
        self.quantity_entry = tk.Entry(self.ore_refining_tab)
        self.quantity_entry.pack()

        calculate_button = tk.Button(self.ore_refining_tab, text="Calculate Minerals", command=self.calculate_ore_refining)
        calculate_button.pack()

        self.ore_results_label = tk.Label(self.ore_refining_tab, text="")
        self.ore_results_label.pack()

    def create_retriever_tab(self):
        # Retriever Tab Content
        retriever_label = tk.Label(self.retriever_tab, text="Retriever Mineral Requirements:")
        retriever_label.pack()

        self.retriever_results_label = tk.Label(self.retriever_tab, text=self.format_mineral_requirements(retriever_requirements))
        self.retriever_results_label.pack()

    def create_bowhead_tab(self):
        # Bowhead Tab Content
        bowhead_label = tk.Label(self.bowhead_tab, text="Select Bowhead Components:")
        bowhead_label.pack()

        self.component_vars = {}
        for component in bowhead_requirements:
            var = tk.IntVar()
            checkbutton = tk.Checkbutton(self.bowhead_tab, text=component, variable=var)
            checkbutton.pack()
            self.component_vars[component] = var

        calculate_button = tk.Button(self.bowhead_tab, text="Calculate Requirements", command=self.calculate_bowhead_requirements)
        calculate_button.pack()

        self.bowhead_results_label = tk.Label(self.bowhead_tab, text="")
        self.bowhead_results_label.pack()

    def calculate_ore_refining(self):
        ore_type = self.ore_var.get()
        try:
            quantity = int(self.quantity_entry.get())
        except ValueError:
            self.ore_results_label.config(text="Invalid quantity")
            return

        minerals = ore_data.get(ore_type, {})
        if not minerals:
            self.ore_results_label.config(text="Ore not found")
            return

        result_text = ""
        for mineral, amount in minerals.items():
            result_text += f"{mineral}: {amount * quantity}\n"

        self.ore_results_label.config(text=result_text)

    def calculate_bowhead_requirements(self):
        selected_components = [component for component, var in self.component_vars.items() if var.get() == 1]
        total_minerals = {}
        total_pi_materials = {}

        for component in selected_components:
            component_data = capital_component_data.get(component)
            if component_data:
                quantity = bowhead_requirements.get(component, 1)  # Default to 1 if not found

                # Calculate minerals
                for mineral, amount in component_data["minerals"].items():
                    total_minerals[mineral] = total_minerals.get(mineral, 0) + amount * quantity

                # Calculate PI materials
                for pi_material, amount in component_data["pi_materials"].items():
                    total_pi_materials[pi_material] = total_pi_materials.get(pi_material, 0) + amount * quantity

        # Format results
        mineral_text = "Minerals:\n" + self.format_mineral_requirements(total_minerals)
        pi_text = "PI Materials:\n" + "\n".join([f"{item}: {amount}" for item, amount in total_pi_materials.items()])

        self.bowhead_results_label.config(text=mineral_text + "\n" + pi_text)

    def format_mineral_requirements(self, requirements):
        return "\n".join([f"{mineral}: {amount}" for mineral, amount in requirements.items()])


if __name__ == "__main__":
    app = EveProductionCalculator()
    app.mainloop()
