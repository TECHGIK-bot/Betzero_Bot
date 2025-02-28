from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

# Replace with your bot token and chat ID
BOT_TOKEN = "7057194211:AAF_StFo_FwRn1AR_XOJQurXuYgh5ZvO2b4"
CHAT_ID = "6260151149"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Specify the path to the Chrome binary installed in your Render environment
options.binary_location = "/usr/bin/google-chrome-stable"  # Path to Chrome binary on Render

# Initialize driver with Service object
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Add your bot functionality below



# Correct driver initialization
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


# Open the website
driver.get('https://logigames.bet9ja.com/Games/Launcher?gameId=11000&provider=0&pff=1&skin=201')



def Container():
    Ball_Container = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/footer/div[2]/div[1]/div/div[1]')

    Ball_numbers = []
    for i in range(1, 7):
        container_xpath = f'/html/body/div[1]/div/div/div/footer/div[2]/div[1]/div/div[1]/div[{i}]/div/div'
        container_numbers = driver.find_element(By.XPATH, container_xpath)
        Numbers = container_numbers.text

        # Convert to integer before appending
        try:
            Ball_numbers.append(int(Numbers))
            print(f"Container {i}, Ball-Number is: {int(Numbers)}")
            
        except ValueError:
            print(f"Container {i}, Ball-Number is not a valid integer: {Numbers}")

    return Ball_numbers

def Hot_Numbers():
    Hot_Balls = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div[2]/div[2]/div[1]')
    
    First_Hot_Ball = Hot_Balls.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div[2]/div[2]/div[1]/div[1]/span').text
    Second_Hot_Ball = Hot_Balls.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div[2]/div[2]/div[1]/div[2]/span').text
    Third_Hot_Ball = Hot_Balls.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div[2]/div[2]/div[1]/div[3]/span').text

    # Convert strings to integers
    try:
        Balls = [int(First_Hot_Ball), int(Second_Hot_Ball), int(Third_Hot_Ball)]
        print(Balls)
    except ValueError:
        print("One or more hot balls are not valid integers")
        Balls = []

    return Balls

def send_telegram_message(message):
    """Sends a message to your Telegram bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Telegram notification sent successfully!")
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def checker():
    failure_count = 0
    max_failure_count = 0

    # Initialize the flag for the first run
    waiting_for_container = True

    while True:
        if waiting_for_container:
            # Call the Hot_Numbers function
            Balls = Hot_Numbers()
            print("Hot numbers updated.")
            waiting_for_container = False  # Now wait for the timer to reach 40
        else:
            # Wait for the timer element to be present
            Timer = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/footer/div[2]/div[4]/div/div/div'))
            )

            # Get the timer value
            Time = Timer.text.strip()

            # Check if the timer equals 40
            if Time.isdigit() and int(Time) == 40:
                print(f"Timer matched 40. Current time: {Time}")
                
                # Call the Container function
                Ball_numbers = Container()

                # Check if any of the hot numbers are in the container numbers
                if any(ball in Ball_numbers for ball in Balls):
                    failure_count += 1  # Increment failure count when a match is found
                    print(f"Match found! Failure count incremented to {failure_count}")
                    
                    if failure_count >= 2:
                        message = (
                            f"The bot has failed {failure_count} times.\n"
                            f"Play {Balls} as ball zero in the next round.\n"
                            f"The highest failure count so far is {max_failure_count}."
                        )
                        send_telegram_message(message)

                else:
                    failure_count = 0  # Reset failure count when no match is found
                    print(f"No match found. Failure count reset to {failure_count}")

                # Update the maximum failure count if the current one exceeds it
                if failure_count > max_failure_count:
                    max_failure_count = failure_count
                    print(f"New highest failure count: {max_failure_count}")

                # Wait 10 seconds and prepare to call Hot_Numbers again
                time.sleep(10)
                waiting_for_container = True  # Switch back to update Hot_Numbers


checker()
