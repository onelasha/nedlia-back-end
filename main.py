import re

# Define the regex
regex = r"^(?:[2-9]\d*|\d{2,})\.\d+\.\d+$|^1\.(?:1[5-9]|\d{2,})\.\d+$|^1\.14\.(?:5[6-9]|\d{2,})$"

# Test cases
versions = ["1.14.56", "1.15.0", "2.0.0", "1.14.55", "1.14.50", "1.13.99"]

for version in versions:
    is_valid = bool(re.match(regex, version))
    print(f"{version}: {is_valid}")
