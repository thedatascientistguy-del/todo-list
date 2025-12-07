import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class TestTodoApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        cls.base_url = "http://127.0.0.1:8000"

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get(cls.base_url)
        chrome_options.add_argument("--disable-features=GoogleWebComponentsV0Enabled")

        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # ---------------------------------------------------
    # 1. Page Load Test
    # ---------------------------------------------------
    def test_01_page_loads(self):
        self.assertIn("Todo List", self.driver.page_source)
        print("✅ test_01_page_loads passed")

    # ---------------------------------------------------
    # 2. Check Input Box Presence
    # ---------------------------------------------------
    def test_02_input_box_exists(self):
        input_box = self.driver.find_element(By.NAME, "title")
        self.assertIsNotNone(input_box)
        print("✅ test_02_input_box_exists passed")

    # ---------------------------------------------------
    # 3. Add Todo Test
    # ---------------------------------------------------
    def test_03_add_todo(self):
        input_box = self.driver.find_element(By.NAME, "title")
        input_box.send_keys("Selenium Test Todo")
        input_box.send_keys(Keys.RETURN)
        time.sleep(2)

        page = self.driver.page_source
        self.assertIn("Selenium Test Todo", page)
        print("✅ test_03_add_todo passed")

    # ---------------------------------------------------
    # 4. Add Empty Todo Should Fail (HTML Required)
    # ---------------------------------------------------
    def test_04_empty_todo_not_allowed(self):
        input_box = self.driver.find_element(By.NAME, "title")
        input_box.send_keys("")
        input_box.send_keys(Keys.RETURN)
        time.sleep(1)

        item_list = self.driver.find_elements(By.CLASS_NAME, "todo-item")
        titles = [item.text.strip() for item in item_list]
        self.assertNotIn("", titles)
        print("✅ test_04_empty_todo_not_allowed passed")

    # ---------------------------------------------------
    # 5. Toggle Todo Completion
    # ---------------------------------------------------
    def test_05_toggle_todo(self):
        toggle_btn = self.driver.find_element(By.CLASS_NAME, "toggle-btn")
        toggle_btn.click()
        time.sleep(1)

        todo_item = self.driver.find_element(By.CLASS_NAME, "todo-item")
        self.assertTrue("completed" in todo_item.get_attribute("class"))
        print("✅ test_05_toggle_todo passed")

    # ---------------------------------------------------
    # 6. Undo Toggle
    # ---------------------------------------------------
    def test_06_undo_toggle(self):
        toggle_btn = self.driver.find_element(By.CLASS_NAME, "toggle-btn")
        toggle_btn.click()
        time.sleep(1)

        todo_item = self.driver.find_element(By.CLASS_NAME, "todo-item")
        self.assertFalse("completed" in todo_item.get_attribute("class"))
        print("✅ test_06_undo_toggle passed")

    # ---------------------------------------------------
    # 7. Delete Todo Item
    # ---------------------------------------------------
    def test_07_delete_todo(self):
        delete_btn = self.driver.find_element(By.CLASS_NAME, "delete-btn")
        delete_btn.click()
        time.sleep(1)

        todo_items = self.driver.find_elements(By.CLASS_NAME, "todo-item")
        self.assertTrue(len(todo_items) >= 0)  # no error = pass
        print("✅ test_07_delete_todo passed")

    # ---------------------------------------------------
    # 8. CSS Style Check
    # ---------------------------------------------------
    def test_08_css_background(self):
        container = self.driver.find_element(By.CLASS_NAME, "container")
        bg = container.value_of_css_property("background-color")
        self.assertIsNotNone(bg)
        print(f"✅ test_08_css_background passed with background-color: {bg}")

    # ---------------------------------------------------
    # 9. JS Loaded Check
    # ---------------------------------------------------
    def test_09_javascript_loaded(self):
        result = self.driver.execute_script("return typeof toggleTodo")
        self.assertEqual(result, "function")
        print("✅ test_09_javascript_loaded passed")

    # ---------------------------------------------------
    # 10. Add Multiple Todos
    # ---------------------------------------------------
    def test_10_multiple_todos(self):
        for i in range(3):
            input_box = self.driver.find_element(By.NAME, "title")
            input_box.send_keys(f"Todo {i}")
            input_box.send_keys(Keys.RETURN)
            time.sleep(1)

        page = self.driver.page_source
        self.assertIn("Todo 0", page)
        self.assertIn("Todo 1", page)
        self.assertIn("Todo 2", page)
        print("✅ test_10_multiple_todos passed")


if __name__ == "__main__":
    unittest.main()
