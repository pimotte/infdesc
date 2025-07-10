import csv
from collections import defaultdict

# Read the input CSV file
data = defaultdict(lambda: defaultdict(lambda: {'exercise': [], 'chapex': []}))

with open('planning.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        moment, difficulty, kind, number = row
        data[moment][difficulty][kind].append(number)

# Create a list of all difficulties that occur
difficulties = sorted({difficulty for moment in data for difficulty in data[moment]})

# Write the output CSV file
with open('planning2.csv', 'w', newline='', delimiter=';') as file:
    writer = csv.writer(file)
    writer.writerow(['Moment'] + difficulties)
    for moment in sorted(data.keys()):
        row = [moment]
        for difficulty in difficulties:
            content = ""
            
            # Add exercises if any exist
            if data[moment][difficulty]['exercise']:
                exercises = ','.join(data[moment][difficulty]['exercise'])
                content += f"Exercises: {exercises}."
            
            # Add chapter exercises if any exist
            if data[moment][difficulty]['chapex']:
                chapex = ','.join(data[moment][difficulty]['chapex'])
                content += f"Chapter exercises: {chapex}."
            row.append(content)
            
        writer.writerow(row)

print("planning_processed.csv has been created successfully!")