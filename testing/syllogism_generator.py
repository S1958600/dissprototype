import openpyxl

# Define the possible types of statements
statements = [
    "⊨",
    "⊨¬",
    "⊭¬",
    "⊭"
]

# Define the four types of moods for a syllogism
figures = [
    (("B", "C"), ("A", "B"), ("A", "C")),
    (("C", "B"), ("A", "B"), ("A", "C")),
    (("B", "C"), ("B", "A"), ("A", "C")),
    (("C", "B"), ("B", "A"), ("A", "C"))
]

# Create a new workbook and select the active worksheet
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "all Syllogisms"

# Write the header row
ws.append(["Figure", "Major Premise", "Minor Premise", "Conclusion"])

# Generate all possible syllogisms
for figure in figures:
    for major in statements:
        for minor in statements:
            for conclusion in statements:
                # Create entries for each tuple in the figure
                major_premise = f"{figure[0][0]} {major} {figure[0][1]}"
                minor_premise = f"{figure[1][0]} {minor} {figure[1][1]}"
                conclusion_premise = f"{figure[2][0]} {conclusion} {figure[2][1]}"
                ws.append([major_premise, minor_premise, conclusion_premise])
                
                
# Save the workbook
wb.save("syllogisms.xlsx")
