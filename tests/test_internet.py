import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE = "https://the-internet.herokuapp.com"


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    yield d
    d.quit()


def wait_for(driver, locator):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))


def click(driver, locator):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator)).click()


def login(driver, user="tomsmith", pwd="SuperSecretPassword!"):
    driver.get(BASE + "/login")
    wait_for(driver, (By.ID, "username")).send_keys(user)
    driver.find_element(By.ID, "password").send_keys(pwd)
    click(driver, (By.CSS_SELECTOR, "button[type='submit']"))


# TC01: Đăng nhập thành công
def test_login_success(driver):
    login(driver)
    WebDriverWait(driver, 10).until(EC.url_contains("/secure"))
    assert "You logged into a secure area!" in wait_for(driver, (By.ID, "flash")).text


# TC02: Đăng nhập sai mật khẩu
def test_login_wrong_password(driver):
    login(driver, pwd="sai_mat_khau")
    assert "Your password is invalid!" in wait_for(driver, (By.ID, "flash")).text


# TC03: Đăng xuất
def test_logout(driver):
    login(driver)
    WebDriverWait(driver, 10).until(EC.url_contains("/secure"))
    click(driver, (By.CSS_SELECTOR, "a[href='/logout']"))
    WebDriverWait(driver, 10).until(EC.url_contains("/login"))
    assert "You logged out of the secure area!" in wait_for(driver, (By.ID, "flash")).text


# TC04: Thêm và xóa phần tử
def test_add_remove_elements(driver):
    driver.get(BASE + "/add_remove_elements/")
    for _ in range(3):
        click(driver, (By.CSS_SELECTOR, "button[onclick='addElement()']"))
    assert len(driver.find_elements(By.CLASS_NAME, "added-manually")) == 3
    click(driver, (By.CLASS_NAME, "added-manually"))
    assert len(driver.find_elements(By.CLASS_NAME, "added-manually")) == 2


# TC05: Checkbox
def test_checkboxes(driver):
    driver.get(BASE + "/checkboxes")
    boxes = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='checkbox']"))
    )
    assert not boxes[0].is_selected()
    assert boxes[1].is_selected()
    boxes[0].click()
    assert boxes[0].is_selected()


# TC06: Dropdown
def test_dropdown(driver):
    driver.get(BASE + "/dropdown")
    select = Select(wait_for(driver, (By.ID, "dropdown")))
    select.select_by_value("2")
    assert select.first_selected_option.text == "Option 2"