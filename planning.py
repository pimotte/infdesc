import csv
from collections import defaultdict


def parse_section(kind, number):
    """Return (section_label, exercise_number) for display purposes.

    Exercises:
      0.x   -> section 'H0',  number x
      A.B.x -> section 'A.B', number x

    Chapter exercises (chapex):
      A.x   -> section 'A.E', number x
    """
    if kind == 'exercise':
        if number.startswith('0.'):
            return ('H0', number[2:])
        section, _, num = number.rpartition('.')
        return (section, num)
    else:  # chapex
        section, _, num = number.rpartition('.')
        return (f"{section}.E", num)


def section_sort_key(section):
    """Numerical sort key for section labels like H0, 0.E, 1.1, 1.E, B.3."""
    if section == 'H0':
        return (0.0, 0.0)
    parts = section.split('.')
    try:
        first = float(parts[0])
    except ValueError:
        # Letters like 'B' sort after numbers
        first = 1000.0 + ord(parts[0][0])
    if parts[1] == 'E':
        second = float('inf')
    else:
        second = float(parts[1])
    return (first, second)


# Read the input CSV file
# data[moment][difficulty][section] = [num, ...]
data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

with open('planning.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        moment, difficulty, kind, number = row
        section, num = parse_section(kind, number)
        data[moment][difficulty][section].append(num)

# Column order matching target
DIFFICULTIES = ['Essentieel', 'Aanbevolen', 'Bonus']

# Write the output CSV file
with open('planning_processed.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['Week'] + DIFFICULTIES)
    for moment in sorted(data.keys()):
        row = [moment]
        for difficulty in DIFFICULTIES:
            sections = data[moment][difficulty]
            if not sections:
                row.append('')
                continue
            lines = []
            for section in sorted(sections.keys(), key=section_sort_key):
                nums = ', '.join(sections[section])
                lines.append(f"in {section}: {nums}")
            row.append('\n'.join(lines))
        writer.writerow(row)

print("planning_processed.csv has been created successfully!")
