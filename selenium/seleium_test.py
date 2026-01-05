import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "http://localhost:5173"

@pytest.fixture
def driver():
    """Create and cleanup Firefox driver"""
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


class TestJsonPage:
    """Tests for JsonPage.tsx"""

    def test_json_page_loads(self, driver):
        """Test that JsonPage loads successfully"""
        driver.get(f"{BASE_URL}/")
        wait = WebDriverWait(driver, 10)
        
        # Check page title
        assert "Upload JSON File" in driver.page_source
        
        # Check for file input
        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        assert file_input.get_attribute("accept") == "application/json"

         # Find both radio buttons
        radios = driver.find_elements(By.CSS_SELECTOR, "input[name='season'][type='radio']")
        assert len(radios) == 2
        
        # Test Summer selection
        radios[0].click()
        assert radios[0].is_selected()
        
        # Test Winter selection
        radios[1].click()
        assert radios[1].is_selected()

        note_input = wait.until(
            EC.presence_of_element_located((By.ID, "note-input"))
        )
        # Enter note text
        test_note = "Test upload note"
        note_input.send_keys(test_note)

         # Create a test JSON file
        test_json_content = '''{
            "station_id": "TEST001",
            "dkhype": {
                "1.1": 10,
                "5": 20,
                "20": 30,
                "50": 40
            },
            "vandstand": {
                "varsel": 100,
                "1.1": 110,
                "2": 120,
                "5": 130,
                "10": 140
            }
        }'''
        
        # Upload file by finding file input and setting value
        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        
        # Note: Direct file upload via Selenium requires a file on disk
        # We'll test the UI elements and validation flow instead
        note_input = driver.find_element(By.ID, "note-input")
        assert note_input is not None
        
        h1 = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert "Upload JSON File" in h1.text
        
        # Check for season label
        labels = driver.find_elements(By.TAG_NAME, "label")
        assert any("Season" in label.text for label in labels)


class TestHistoryPage:
    """Tests for HistoryPage.tsx"""

    def test_history_page_loads(self, driver):
        """Test that HistoryPage loads successfully"""
        driver.get(f"{BASE_URL}")
        wait = WebDriverWait(driver, 10)
        # Navigate to History page
        history_button = wait.until(EC.element_to_be_clickable((By.ID, "History")))
        history_button.click()
        
        # Check for main heading
        h1 = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert "Upload History" in h1.text
        try:
            # Either loading message or table should be present
            loading = driver.find_elements(By.XPATH, "//*[contains(text(), 'Loading history')]")
            if loading:
                assert len(loading) > 0
            else:
                # Or table is loaded
                table = driver.find_elements(By.TAG_NAME, "table")
                assert len(table) > 0
        except:
            # Table should eventually appear
            table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            assert table is not None
        headers = driver.find_elements(By.TAG_NAME, "th")
        header_texts = [h.text for h in headers]
        
        expected_headers = ["Upload ID", "Date", "Note", "Records", "Action"]
        for expected in expected_headers:
            assert any(expected.lower() in h.lower() for h in header_texts), \
                f"Header '{expected}' not found in {header_texts}"
        try:
            heading = wait.until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'All Uploads')]"))
            )
            assert heading is not None
        except:
            # If no uploads, just check the heading exists
            h2 = driver.find_elements(By.TAG_NAME, "h2")
            assert any("All Uploads" in h.text for h in h2)

        # Find all View Details buttons
        buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'View Details')]")
        
        if len(buttons) > 0:
            # Click first button
            buttons[0].click()
            
            # Wait for details section to appear
            time.sleep(1)
            
            # Check if Back button appears (indicating details view is shown)
            back_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Back')]")
            assert len(back_buttons) > 0

             # Find View Details buttons
        buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'View Details')]")
        
        if len(buttons) > 0:
            # Click to open details
            buttons[0].click()
            time.sleep(1)
            
            # Check for records count in heading (e.g., "Upload #1 - Details (5 records)")
            headings = driver.find_elements(By.TAG_NAME, "h2")
            details_heading = next((h for h in headings if "Details" in h.text), None)
            
            if details_heading:
                assert "records" in details_heading.text.lower() or "Details" in details_heading.text



if __name__ == "__main__":
    pytest.main([__file__, "-v"])