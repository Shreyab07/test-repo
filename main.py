import random
import json

code_template = """
def calculate_sum_{n}():
    numbers = {numbers}
    result = sum(numbers)
    print(f"Sum of numbers: {{result}}")

calculate_sum_{n}()
"""

def generate_code_snippets(num_snippets):
    snippets = []
    for i in range(2, num_snippets + 2):
        numbers = ', '.join(str(random.randint(1, 100)) for _ in range(i))
        snippets.append(code_template.format(n=i, numbers=numbers))
    return snippets

# Set the number of code snippets you want
num_code_snippets = 50000  # Adjust as needed

# Generate code snippets
code_snippets = generate_code_snippets(num_code_snippets)

# Save the generated code snippets to a JSON file
json_file_path = "code_snippets.json"

with open(json_file_path, "w") as json_file:
    json.dump({"code_snippets": code_snippets}, json_file, indent=2)

print(f"Total {num_code_snippets} code snippets written to {json_file_path}.")
