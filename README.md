# Udemy Curriculum Extractor

This project extracts chapter and episode names from a Udemy course curriculum.

## Prerequisites

- Python 3.7+
- Playwright

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

## Usage

Run the script with the URL of the course or a local HTML file:

```bash
python extract_curriculum.py <url_or_file_path>
```

## Testing

A `mock_course.html` file is provided to test the script.

```bash
python extract_curriculum.py mock_course.html
```

## Note on Selectors

The script is configured with selectors that match `mock_course.html`. Udemy's website uses dynamic class names that change frequently. To use this script on a real Udemy course, you will likely need to update the `SELECTORS` dictionary in `extract_curriculum.py` with the current selectors from the Udemy course page.
