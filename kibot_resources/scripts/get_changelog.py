import argparse
import re
import sys

def parse_changelog(file_path, version, title_only, extra_spaces, separators):
    try:
        with open(file_path, 'r') as f:
            changelog = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    # Regex to match the version block and stop at the next version or any line with square brackets
    version_pattern = re.compile(rf"## \[{version}\] - (\d{{4}}-\d{{2}}-\d{{2}})\n(.*?)(?=## \[|\[Unreleased\]:|\[\d+\.\d+\.\d+\]:|$)", re.DOTALL)
    match = version_pattern.search(changelog)

    if not match:
        print(f"Version {version} not found.")
        return

    date, content = match.groups()

    if title_only:
        print(f"Version {version} - {date}")
    else:

        if separators is not None:
            content = re.sub(r'^(###.*?)$', '_' * separators + r'\n\1', content, flags=re.MULTILINE)

        cleaned_content = re.sub(r'### ', '', content)  # Remove ###

        if extra_spaces:
            cleaned_content = re.sub(r'(?<!\n)\n(?!\n)', '\n\n', cleaned_content)

        print(cleaned_content)

def main():
    parser = argparse.ArgumentParser(description="Extract and format a specific version from CHANGELOG.md")
    parser.add_argument("-v", "--version", required=True, help="Version to extract (e.g., 1.0.1)")
    parser.add_argument("-f", "--file", required=True, help="Path to CHANGELOG.md file")
    parser.add_argument("-t", "--title-only", action="store_true", help="Print the title only")
    parser.add_argument("-s", "--extra-spaces", action="store_true", help="Add extra spaces between lines")
    parser.add_argument("-a", "--separators", type=int, required=False, help="Number of underscores for separators")

    args = parser.parse_args()
    parse_changelog(args.file, args.version, args.title_only, args.extra_spaces, args.separators)

if __name__ == "__main__":
    main()
