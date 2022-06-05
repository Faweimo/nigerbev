import  pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="module")
def chrome_browser_instance(request):
    """ Provide  a selenium webdriver instance """

    options = Options()
    options.headless = False

    browser = webdriver.Chrome(options=options)
    yield browser

    # browser = webdriver.Firefox(executable_path = "/home/syllabustech/projects/process_management/geckodriver")
    # browser.get("https://www.rcvacademy.com")
    # browser.maximize_window()
    print (browser.title)
    browser.close()