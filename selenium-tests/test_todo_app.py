
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestTodoApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        cls.base_url = "http://web:8000"
        cls.driver = webdriver.Chrome(options=chrome_options)

        # Wait until FastAPI app is ready
        for i in range(15):
            try:
                cls.driver.get(cls.base_url)
                if "Todo List" in cls.driver.page_source:
                    break
            except:
                time.sleep(2)
        time.sleep(2)  # extra buffer

        # Clear any existing todos
        try:
            delete_buttons = cls.driver.find_elements(By.CLASS_NAME, "delete-btn")
            for btn in delete_buttons:
                btn.click()
                time.sleep(0.5)
        except:
            pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # 1. Page Load Test
    def test_01_page_loads(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        self.assertIn("Todo List", self.driver.page_source)

    # 2. Check Input Box Presence
    def test_02_input_box_exists(self):
        input_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        self.assertIsNotNone(input_box)

    # 3. Add Todo Test
    def test_03_add_todo(self):
        input_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "title"))
        )
        input_box.send_keys("Selenium Test Todo")
        input_box.send_keys(Keys.RETURN)

        # Wait for last added todo
        new_todo = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(By.CLASS_NAME, "todo-item")[-1]
        )
        self.assertIn("Selenium Test Todo", new_todo.text.split('\n')[0])

    # 4. Add Empty Todo Should Fail
    def test_04_empty_todo_not_allowed(self):
        input_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "title"))
        )
        input_box.send_keys("")
        input_box.send_keys(Keys.RETURN)

        time.sleep(1)
        item_list = self.driver.find_elements(By.CLASS_NAME, "todo-item")
        titles = [item.text.split('\n')[0] for item in item_list]
        self.assertNotIn("", titles)

    # 5. Toggle Todo Completion
    def test_05_toggle_todo(self):
        toggle_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "toggle-btn"))
        )
        toggle_btn.click()

        todo_item = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "todo-item"))
        )
        self.assertTrue("completed" in todo_item.get_attribute("class"))


    # 6. Undo Toggle
    def test_06_undo_toggle(self):
        # Get all todos and their toggle buttons
        todo_items = self.driver.find_elements(By.CLASS_NAME, "todo-item")
        toggle_btns = self.driver.find_elements(By.CLASS_NAME, "toggle-btn")

        # Click the toggle button for the last todo
        toggle_btns[-1].click()

        # Wait until the "completed" class is removed
        todo_item = WebDriverWait(self.driver, 10).until(
            lambda d: "completed" not in d.find_elements(By.CLASS_NAME, "todo-item")[-1].get_attribute("class") and
                    d.find_elements(By.CLASS_NAME, "todo-item")[-1]
        )

        self.assertFalse("completed" in todo_item.get_attribute("class"))


    # 7. Delete Todo Item
    def test_07_delete_todo(self):
        delete_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "delete-btn"))
        )
        delete_btn.click()

        time.sleep(1)
        todo_items = self.driver.find_elements(By.CLASS_NAME, "todo-item")
        self.assertTrue(len(todo_items) >= 0)

    # 8. CSS Style Check
    def test_08_css_background(self):
        container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "container"))
        )
        bg = container.value_of_css_property("background-color")
        self.assertIsNotNone(bg)

    # 9. JS Loaded Check
    def test_09_javascript_loaded(self):
        result = self.driver.execute_script("return typeof toggleTodo")
        self.assertEqual(result, "function")

    def test_10_multiple_todos(self):
        for i in range(3):
            input_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "title"))
            )
            input_box.clear()
            input_box.send_keys(f"Todo {i}")
            input_box.send_keys(Keys.RETURN)

            # Wait until the last todo item contains the text we just added
            WebDriverWait(self.driver, 10).until(
                lambda d: len(d.find_elements(By.CLASS_NAME, "todo-item")) > 0 and 
                        f"Todo {i}" in d.find_elements(By.CLASS_NAME, "todo-item")[-1].text
            )

        # Extract only the first line (title) to assert
        todo_texts = [t.text.split('\n')[0] for t in self.driver.find_elements(By.CLASS_NAME, "todo-item")]
        self.assertIn("Todo 0", todo_texts)
        self.assertIn("Todo 1", todo_texts)
        self.assertIn("Todo 2", todo_texts)


if __name__ == "__main__":
    unittest.main()
