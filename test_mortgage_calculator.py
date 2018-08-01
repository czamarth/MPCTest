from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = 5
FFBINARYPATH = r'C:\Program Files\Mozilla Firefox\Firefox.exe'


def clear_fill_by_id(id, value):
    formField = driver.find_element_by_id(id)
    formField.clear()
    formField.send_keys(value)

def wait_for_element_by_xpath(xpath):
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, xpath)))

def wait_for_element_by_id(id):
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, id)))


def fill_first_screen():
    values = {
        'calculator_widget_amount': '200000',
        'calculator_widget_interest': '5',
        'calculator_widget_HomeValue': '235000'
    }
    for id, value in values.items():
        wait_for_element_by_id(id)
        clear_fill_by_id(id, value)


def click_next():
    driver.find_element_by_css_selector('a.calculator-button.next-button').click()


def click_finish():
    driver.find_element_by_css_selector('li.next.finish > a.calculator-button.finish-button').click()


def fill_second_screen():
    values = {
        'calculator_widget_PropertyTaxes': '2000',
        'calculator_widget_Insurance': '1865',
        'calculator_widget_PMI': '0.52'
    }
    for id, value in values.items():
        wait_for_element_by_id(id)
        clear_fill_by_id(id, value)


def verify_values():
    values = {
        (1, 'Monthly Principal & Interests', '$1,073.64'),
        (4, 'Loan To Value Ratio', '85.11%'),
        (7, 'Total Monthly Payments', '$1,482.39')
    }
    for index, expected_label, expected_value in values:
        xpath_label = "//div[@id='analysisDiv']/table/thead/tr[{index}]/th".format(index=index)
        wait_for_element_by_xpath(xpath_label)
        actual_label = driver.find_element_by_xpath(xpath_label).text
        xpath_value = "//div[@id='analysisDiv']/table/thead/tr[{index}]/td".format(index=index)
        wait_for_element_by_xpath(xpath_value)
        actual_value = driver.find_element_by_xpath(xpath_value).text
        if actual_label != expected_label:
            print(
                "Unexpected label {label} on line {index}, possible page structure change.".format(label=actual_label,
                                                                                                   index=index))
            continue
        if actual_value != expected_value:
            print("Different value {value} for {label}. Expected value {expected_value}".format(value=actual_value,
                                                                                                label=expected_label,
                                                                                                expected_value=expected_value))
        else:
            print("Correct value {value} for {label}".format(value=actual_value, label=actual_label))


binary = FirefoxBinary(FFBINARYPATH)
driver = webdriver.Firefox(firefox_binary=binary)
driver.get('https://www.mortgageloan.com/calculator')

fill_first_screen()
click_next()
fill_second_screen()
click_finish()
verify_values()
driver.close()