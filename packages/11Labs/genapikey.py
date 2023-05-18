import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymailtm import MailTm, Message
import re
import time

while True:
    try:
        print("Generating Email...")
        # Generate a temporary email address using pymailtm
        mail_client = MailTm().get_account()
        mail_address = mail_client.address
        print("Email Generated!")

        # Get the current directory and construct the path to chromedriver
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chromedriver_path = os.path.join(dir_path, "chromedriver.exe")

        # Start a new Chrome browser session using chromedriver
        driver = webdriver.Chrome(executable_path=chromedriver_path)

        # Navigate to the sign-up page
        driver.get("https://beta.elevenlabs.io/sign-up")
        driver.set_window_size(1920, 1080)
        time.sleep(4)
        print("Site Opened!")

        # Find the email input field and fill it with the generated email address
        email_input = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div/div[2]/form/div[1]/div/input')
        email_input.send_keys(mail_address)
        print("Email Inputed...")

        time.sleep(0.5)

        # Find the password input field and fill it with chosen password
        password_input = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div/div[2]/form/div[2]/div/input')
        password_input.send_keys("Awesomepassword123")
        print("Password Inputed...")

        # Agree to TOS
        driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div/div[2]/form/div[3]/input').click()
        print("TOS Agreed To...")

        time.sleep(0.5)

        # Sign up
        driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div/div[2]/form/div[5]/button').click()
        print("Successfully Created Account!")

        print("Waiting For Verification Email...")
        # Wait for the verification email to arrive
        while True:
            time.sleep(1)
            new_message: Message = mail_client.wait_for_message()
            if "Verify your email" in new_message.subject:
                verification_url = re.findall(r'https:\/\/beta\.elevenlabs\.io.+', new_message.text)[0]
                break

        # Open the verification URL in a new tab
        driver.execute_script("window.open('" + verification_url + "', '_blank');")
        print("Email Verified!")

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(2)

        # Close window
        driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[2]/div/div/div[1]/div[1]/button').click()

        time.sleep(1)

        print("Signing In...")
        # Sign in
        driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div/div[2]/div[3]/a[1]').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[2]/div/div/div[2]/div/form/div[2]/input').send_keys(mail_address)
        driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[2]/div/div/div[2]/div/form/div[3]/input').send_keys("Awesomepassword123")
        time.sleep(0.5)
        driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[2]/div/div/div[2]/div/form/div[4]/button').click()
        print("Signed In!")

        time.sleep(2)

        print("Going To Account Settings...")
        # Click account
        driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div/div[2]/div[3]/div/button').click()

        time.sleep(1)

        # Click profile
        driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div/div[2]/div[3]/div[2]/div[2]/a[1]').click()

        time.sleep(1)

        print("Grabbing API Key...")
        # Reveal and grab api key
        driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/button[1]').click()
        time.sleep(0.5)
        api_key_input = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/input')
        api_key = api_key_input.get_attribute("value")
        print("API Key Grabbed...")

        # Add API key to txt file
        with open('./packages/11Labs/apikeys.txt', 'a') as file:
            file.write(api_key + '\n')

        print("API Key Added To apikeys.txt!")

        # Close the browser window
        driver.quit()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Restarting...")
        continue