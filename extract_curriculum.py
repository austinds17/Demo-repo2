import sys
import os
from playwright.sync_api import sync_playwright

# Configuration for Selectors
# NOTE: These selectors match the mock_course.html provided in this project.
# For the real Udemy website, you will likely need to update these selectors
# as Udemy uses dynamic class names (e.g., 'ud-accordion-panel-title').
#
# Tips for finding the right selectors:
# 1. Open the course page in your browser.
# 2. Right-click a section title and select "Inspect".
# 3. Look for unique classes or attributes (like data-purpose="section-header").
# 4. Update the dictionary below.

SELECTORS = {
    # Text or selector for the button that expands all curriculum sections
    'expand_button_text': "Expand all sections",

    # The container for a whole section (chapter)
    'section': '.section',

    # The element containing the section title text
    'section_title': '.section-title',

    # The element containing the lecture (episode) title text
    'lecture_title': '.lecture-title'
}

def extract_curriculum(url):
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Handle file paths
        if not url.startswith('http') and not url.startswith('file://'):
            # If it's a local file, ensure absolute path
            if os.path.exists(url):
                url = 'file://' + os.path.abspath(url)

        print(f"Navigating to {url}...")
        try:
            page.goto(url)
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            browser.close()
            return

        # Wait for content to load
        try:
            # We wait for at least one section to appear
            # Use the configured selector
            page.wait_for_selector(SELECTORS['section'], timeout=5000)
        except:
            print(f"Timed out waiting for element '{SELECTORS['section']}'. The page structure might be different or the page took too long to load.")
            print("Tip: Check if the 'section' selector in the script matches the website's HTML.")

        # Try to expand sections
        try:
            # Look for button with text "Expand all sections"
            expand_button = page.locator('button', has_text=SELECTORS['expand_button_text'])
            if expand_button.count() > 0 and expand_button.first.is_visible():
                print(f"Clicking '{SELECTORS['expand_button_text']}'...")
                expand_button.first.click()
                # Wait for animations or DOM updates
                page.wait_for_timeout(2000)
            else:
                print(f"'{SELECTORS['expand_button_text']}' button not found or not visible.")
        except Exception as e:
            print(f"Error trying to expand sections: {e}")

        # Extract data
        sections = page.query_selector_all(SELECTORS['section'])
        if not sections:
            print("No sections found.")
            # Optional: Print page content for debugging
            # print(page.content())
        else:
            print(f"\nFound {len(sections)} sections.\n")

            for section in sections:
                title_el = section.query_selector(SELECTORS['section_title'])
                title = title_el.inner_text().strip() if title_el else "Unknown Section"
                print(f"### {title}")

                # Lectures might be in .lecture-title or .lecture item
                lectures = section.query_selector_all(SELECTORS['lecture_title'])
                for lecture in lectures:
                    print(f"  - {lecture.inner_text().strip()}")
                print("")

        browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_curriculum.py <url_or_file_path>")
        sys.exit(1)

    target = sys.argv[1]
    extract_curriculum(target)
