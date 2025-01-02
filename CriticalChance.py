import tkinter as tk
import os
import sys

# Function to handle file paths when packaging the application
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Update the calculate function to include the new checkboxes in the absolute_bonus calculation
def calculate(*args):
    try:
        # Retrieve values from the entry fields and convert them to floats
        base_crit = float(entry_base_crit.get()) / 100 if entry_base_crit.get() else 0
        relative_bonus = float(entry_relative_bonus.get()) / 100 if entry_relative_bonus.get() else 0
        blood_rush_multi = float(entry_blood_rush_multi.get()) / 100 if entry_blood_rush_multi.get() else 0
        gladiator_set_bonus = float(entry_gladiator_set_bonus.get()) / 100 if entry_gladiator_set_bonus.get() else 0
        combo_multi = float(entry_combo_multi.get()) if entry_combo_multi.get() else 0

        # Start with the base Wrathful Advance
        wrathful_advance = float(entry_wrathful_advance.get()) / 100 if entry_wrathful_advance.get() else 0
        multiplier = 2 if not check_helminth.get() else 1
        wrathful_advance *= multiplier

        # Apply the multiplier to the checkboxes' bonuses
        if check_molt_augmented.get(): wrathful_advance += 0.60 * multiplier
        if check_growing_power.get(): wrathful_advance += 0.25 * multiplier
        if check_vome_invocation.get(): wrathful_advance += 0.60 * multiplier
        if check_naramon_school.get(): wrathful_advance += 0.40 * multiplier

        # Initialize absolute_bonus with wrathful_advance
        absolute_bonus = wrathful_advance

        # Add the values of the new checkboxes to the absolute_bonus
        if check_arcane_avenger.get(): absolute_bonus += 0.45
        if check_cats_eye.get(): absolute_bonus += 0.60

        # Calculate the total critical chance
        if combo_multi > 0:
            total_crit_chance = base_crit * (1 + relative_bonus + (blood_rush_multi + gladiator_set_bonus) * (combo_multi - 1)) + absolute_bonus
        else:
            total_crit_chance = base_crit * (1 + relative_bonus) + absolute_bonus

        # Determine the Crit Tier based on the total critical chance
        crit_tier = ""
        crit_tier_number = 0
        if total_crit_chance <= 0:
            crit_tier = "Tier 0 - No hit can crit"
        elif 0 < total_crit_chance < 1:
            crit_tier = "Tier 1 - Chance for a yellow crit"
            crit_tier_number = 1
        elif total_crit_chance == 1:
            crit_tier = "Tier 1 - All hits yellow crit"
            crit_tier_number = 1
        elif 1 < total_crit_chance < 2:
            crit_tier = "Tier 2 - Chance for an orange crit"
            crit_tier_number = 2
        elif total_crit_chance == 2:
            crit_tier = "Tier 2 - All hits orange crit"
            crit_tier_number = 2
        elif 2 < total_crit_chance < 3:
            crit_tier = "Tier 3 - Chance for a red crit (tier 3)"
            crit_tier_number = 3
        elif total_crit_chance == 3:
            crit_tier = "Tier 3 - All hits red crit (tier 3)"
            crit_tier_number = 3
        elif 3 < total_crit_chance < 4:
            crit_tier = "Tier 4 - Chance for a red crit (tier 4)"
            crit_tier_number = 4
        elif total_crit_chance == 4:
            crit_tier = "Tier 4 - All hits red crit (tier 4)"
            crit_tier_number = 4
        elif 4 < total_crit_chance < 5:
            crit_tier = "Tier 5 - Chance for a red crit (tier 5)"
            crit_tier_number = 5
        elif total_crit_chance == 5:
            crit_tier = "Tier 5 - All hits red crit (tier 5)"
            crit_tier_number = 5
        elif 5 < total_crit_chance < 6:
            crit_tier = "Tier 6 - Chance for a red crit (tier 6)"
            crit_tier_number = 6
        elif total_crit_chance == 6:
            crit_tier = "Tier 6 - All hits red crit (tier 6)"
            crit_tier_number = 6
        elif 6 < total_crit_chance < 7:
            crit_tier = "Tier 7 - Chance for a red crit (tier 7)"
            crit_tier_number = 7
        elif total_crit_chance == 7:
            crit_tier = "Tier 7 - All hits red crit (tier 7)"
            crit_tier_number = 7

        # Update the result label with the calculated total critical chance and crit tier
        label_result.config(text=f"Total Critical Chance: {total_crit_chance:.2%}\n{crit_tier}")

        # Retrieve the Modded Crit Multiplier value from the entry field
        modded_crit_multi = float(entry_modded_crit_multi.get()) if entry_modded_crit_multi.get() else 0

        # Calculate the Crit Tier Multiplier using the formula
        crit_tier_multi = 1 + (crit_tier_number * (modded_crit_multi - 1))

        # Calculate Average Damage
        average_crit_multi = 1 + total_crit_chance * (modded_crit_multi - 1)

        # Check if modded_crit_multi has a value greater than 0 before updating the label
        if modded_crit_multi > 0:
            # Update the result label with the calculated Crit Tier Multiplier and Average Multi
            label_result.config(text=f"Total Critical Chance: {total_crit_chance:.2%}\nCrit Tier: {crit_tier}\nCrit Tier Multiplier: {crit_tier_multi:.2f} Average Multi: {average_crit_multi:.2f}")
        else:
            # Update the result label without the Crit Tier Multiplier and Average Multi
            label_result.config(text=f"Total Critical Chance: {total_crit_chance:.2%}\nCrit Tier: {crit_tier}")
    except ValueError:
        label_result.config(text="Please enter valid numbers in all fields.")

def open_new_tab():
    # This function creates a new top-level window ('tab')
    new_window = tk.Toplevel(root)
    new_window.title("Critical Chance Information")

    # Create a text widget for the explanation
    text_info = tk.Text(new_window, wrap='word', height=15, width=50)
    text_info.pack(padx=10, pady=10)

    # Insert the explanation text into the text widget
    explanation = (
        "Relative Increases:\n"
        "Most increases to crit chance are relative to the base chance. "
        "Multiple of these stack additively with each other\n"
        "These are:\n"
        "- True Steel\n"
        "- Sacrificial Steel\n"
        "- Blood Rush\n"
        "- Maiming Strike\n\n"
        "Absolute Increases:\n"
        "A few effects grant absolute amounts of crit chance which are applied after relative bonuses. "
        "These are:\n"
        "- Puncture's status effect 'Weakened'\n"
        "- Arcane Avenger\n"
        "- Cat's Eye\n"
        "- Ballistic Bullseye\n"
        "- Shadow Haze\n"
        "- Covenant\n"
        "- Wrathful Advance\n\n"
        "Relative increases are calculated by adding a percentage of the base crit chance. "
        "For example, if a weapon has a base crit chance of 20% and you apply a mod that offers a 100% relative increase, "
        "the total crit chance becomes 40%.\n\n"
        "Absolute increases are flat additions that are applied after calculating the relative increases. "
        "For example, if the total crit chance after relative increases is 40% and you have an absolute increase of 10%, "
        "the final crit chance becomes 50%.\n\n"
        "Average Damage. "
        "When comparing builds it can be helpful to calculate how much damage the weapon will deal on average, which is effected by how often critical hits occur and at what critical multiplier "
    )
    text_info.insert('1.0', explanation)
    text_info['state'] = 'disabled'  # Make the text read-only

# Create the main window
root = tk.Tk()
root.title("Warframe Melee Critical Chance Calculator")
root.geometry("600x400")  # Set the initial window size


# Load the icon image
icon_image = tk.PhotoImage(file=resource_path("icon.png"))  # Use icon.png or icon.ico

# Set the window icon
root.iconphoto(False, icon_image)

# Create a frame to hold all widgets
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Create labels, entry fields, and checkboxes for the user to input their values
labels = ["Base Crit Chance (%)", "Relative Bonus (%)", "Blood Rush Multiplier (%)", "Gladiator Set Bonus (%)", "Combo Multiplier", "Modded Crit Multiplier"]
entries = []
entry_vars = []
for i, text in enumerate(labels):
    tk.Label(frame, text=text).grid(row=i, column=0, sticky='e', padx=10, pady=5)
    var = tk.StringVar()
    entry = tk.Entry(frame, textvariable=var, width=7)  # Set a smaller width for the entry field
    entry.grid(row=i, column=1, sticky='w', padx=10, pady=5)
    entries.append(entry)
    entry_vars.append(var)

entry_base_crit, entry_relative_bonus, entry_blood_rush_multi, entry_gladiator_set_bonus, entry_combo_multi, entry_modded_crit_multi = entries

# Create the Wrathful Advance entry field separately
tk.Label(frame, text="Wrathful Advance (%)").grid(row=0, column=2, sticky='e', padx=10, pady=5)
var_wrathful_advance = tk.StringVar()
entry_wrathful_advance = tk.Entry(frame, textvariable=var_wrathful_advance, width=7)
entry_wrathful_advance.grid(row=0, column=3, sticky='w', padx=10, pady=5)

check_helminth = tk.BooleanVar(value=True)
tk.Checkbutton(frame, text="Helminth", variable=check_helminth).grid(row=1, column=2, columnspan=2, sticky='w', padx=20, pady=5)

check_molt_augmented = tk.BooleanVar()
tk.Checkbutton(frame, text="Molt Augmented (+60%)", variable=check_molt_augmented).grid(row=2, column=2, columnspan=2, sticky='w', padx=20, pady=5)

check_growing_power = tk.BooleanVar()
tk.Checkbutton(frame, text="Growing Power (+25%)", variable=check_growing_power).grid(row=3, column=2, columnspan=2, sticky='w', padx=20, pady=5)

check_vome_invocation = tk.BooleanVar()
tk.Checkbutton(frame, text="Vome Invocation (+60%)", variable=check_vome_invocation).grid(row=4, column=2, columnspan=2, sticky='w', padx=20, pady=5)

check_naramon_school = tk.BooleanVar()
tk.Checkbutton(frame, text="Madurai School (+40%)", variable=check_naramon_school).grid(row=5, column=2, columnspan=2, sticky='w', padx=20, pady=5)

# Trace the checkboxes to call the calculate function when their state changes
check_molt_augmented.trace_add('write', calculate)
check_growing_power.trace_add('write', calculate)
check_vome_invocation.trace_add('write', calculate)
check_naramon_school.trace_add('write', calculate)
check_helminth.trace_add('write', calculate)

# Trace the entry fields to call the calculate function when their value changes
for var in entry_vars:
    var.trace_add('write', calculate)
var_wrathful_advance.trace_add('write', calculate)

# Create a label to display the result
label_result = tk.Label(frame, text="Total Critical Chance: ")
label_result.grid(row=12, column=0, columnspan=4, pady=10, sticky='ew')

# Create the "Absolute Bonuses:" label above the "Calculate" button
tk.Label(frame, text="Absolute Bonuses:").grid(row=10, column=1, columnspan=2, sticky='w', padx=10, pady=5)

# Add the checkboxes for "Arcane Avenger" and "Cat's Eye"
check_arcane_avenger = tk.BooleanVar()
tk.Checkbutton(frame, text="Arcane Avenger (+45%)", variable=check_arcane_avenger).grid(row=11, column=0, columnspan=2, sticky='w', padx=20, pady=5)

check_cats_eye = tk.BooleanVar()
tk.Checkbutton(frame, text="Cat's Eye (+60%)", variable=check_cats_eye).grid(row=11, column=2, columnspan=2, sticky='w', padx=20, pady=5)

# Trace the new checkboxes to call the calculate function when their state changes
check_arcane_avenger.trace_add('write', calculate)
check_cats_eye.trace_add('write', calculate)

# Load the logo image
original_logo_image = tk.PhotoImage(file=resource_path("information.png"))

# Resize the logo image using subsample
logo_image = original_logo_image.subsample(19, 19)  # Adjust the subsample parameters as needed

# Create a button that will open a new tab when clicked
button_new_tab = tk.Button(frame, image=logo_image, command=open_new_tab, borderwidth=0)
button_new_tab.grid(row=12, column=0, sticky='w', padx=10, pady=10)

# Bind the Enter key to the calculate function
root.bind('<Return>', lambda event=None: calculate())

# Run the application
root.mainloop()