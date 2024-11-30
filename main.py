"""Module for validating version numbers against specific version requirements."""
import re

# Define the regex
REGEX = (
    r"^(?:[2-9]\d*|\d{2,})\.\d+\.\d+$|"
    r"^1\.(?:1[5-9]|\d{2,})\.\d+$|"
    r"^1\.14\.(?:5[6-9]|\d{2,})$"
)

# Test cases
versions = ["1.14.56", "1.15.0", "2.0.0", "1.14.55", "1.14.50", "1.13.99"]

for version in versions:
    is_valid = bool(re.match(REGEX, version))
    print(f"{version}: {is_valid}")
# This is a comment
# if __name__ == "__main__":
#     pass
