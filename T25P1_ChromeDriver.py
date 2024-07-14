from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class IMDB:
    # locators
    expandAll = "//span[contains(text(),'Expand all')]"
    name_locator = "//input[@id='text-input__3']"
    birthdateFrom = "//input[@id='text-input__10']"
    birthdateTo = "//input[@id='text-input__11']"
    birthday = "//input[@id='text-input__4']"
    awards = "//button[@data-testid='test-chip-id-golden_globe_nominated']"
    search_topic = "//select[@id='within-topic-dropdown-id']"
    topic_input = "//input[@id='text-input__5']"
    results = "//button//span[text()='See results']"
    results_locator = "//div[@class = 'ipc-html-content-inner-div']"

    # Initializing driver and defining wait with some timeout value
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 30)

    def __init__(self, url):
        self.url = url

    def webPageAccess(self):
        try:
            self.driver.maximize_window()
            self.driver.get(self.url)
        except TimeoutException as e:
            print(e)

    def clickExpandAll(self):
        try:
            # after loading need to scroll down the web page to enter details for fetching results
            self.driver.execute_script("window.scrollBy(0,500)", "")
            # Expanding all controls to enter data
            expand_button = self.wait.until(EC.presence_of_element_located((By.XPATH, self.expandAll)))
            expand_button.click()
        except TimeoutException as e:
            print(e)

    # Method to pass input for name field using explicit wait conditions
    def nameInput(self):
        try:
            name = self.wait.until(EC.presence_of_element_located((By.XPATH, self.name_locator)))
            # Passing name value
            name.send_keys("Macaulay")
        except TimeoutException as e:
            print(e)

    # Method to pass input for birthyear fields using explicit wait conditions
    def birthyear_range(self):
        try:
            BdateFrom = self.wait.until(EC.presence_of_element_located((By.XPATH, self.birthdateFrom)))
            BdateTo = self.wait.until(EC.presence_of_element_located((By.XPATH, self.birthdateTo)))
            BdateFrom.send_keys("1960-01")
            BdateTo.send_keys("1989-12")
        except TimeoutException as e:
            print(e)

    # Method to pass input for birthday field using explicit wait conditions
    def birthday_input(self):
        try:
            Bday = self.wait.until(EC.presence_of_element_located((By.XPATH, self.birthday)))
            Bday.send_keys("08-26")
        except TimeoutException as e:
            print(e)

    # Method to select award options
    def awardOption_input(self):
        try:
            # need to scroll down further to make the elements visible
            self.driver.execute_script("window.scrollBy(0,800)", "")
            # award options are not clickable with error "not scrolled as its not in view", so tried to execute javascript
            awardOptions = self.driver.find_element(By.XPATH, self.awards)
            self.driver.execute_script("arguments[0].click();", awardOptions)
        except TimeoutException as e:
            print(e)

    # Method to select drop down option
    def topicOptionSelect(self):
        try:
            # Tried with select class dint work, so used javascript to select the drop down value
            self.driver.execute_script("return document.getElementById('within-topic-dropdown-id').selectedIndex = '2'")
            # with javascript, it was changing to default option. so tried to trigger the change manually using dispatchEvent method
            self.driver.execute_script("""
                                   var select = document.getElementById('within-topic-dropdown-id');
                                   var event = new Event('change', { bubbles: true });
                                   select.dispatchEvent(event);
                               """)
        except TimeoutException as e:
            print(e)

    # Method for passing page topic values using explicit wait conditions
    def topicInputText(self):
        try:
            tInput = self.wait.until(EC.presence_of_element_located((By.XPATH, self.topic_input)))
            tInput.send_keys("New York City")
        except TimeoutException as e:
            print(e)

    # Method for fetching results by clicking on "See results button" using explicit wait condition
    def resultsClick(self):
        try:
            resultsButton = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.results)))
            resultsButton.click()
            # Waiting for results to load and taking screenshot to verify the output
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.results_locator)))
            self.driver.save_screenshot("results.png")
        except TimeoutException as e:
            print(e)

    def shutdown(self):
        try:
            self.driver.quit()
            print("Completed accessing the web page successfully")
        except:
            print("Error")


if __name__ == "__main__":
    url = "https://www.imdb.com/search/name/"
    oimdb = IMDB(url)
    oimdb.webPageAccess()
    oimdb.clickExpandAll()
    oimdb.nameInput()
    oimdb.birthyear_range()
    oimdb.birthday_input()
    oimdb.awardOption_input()
    oimdb.topicOptionSelect()
    oimdb.topicInputText()
    oimdb.resultsClick()
    oimdb.shutdown()
