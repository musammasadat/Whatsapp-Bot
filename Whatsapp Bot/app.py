
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyttsx3
import schedule


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


driver.get("https://web.whatsapp.com")
print("Please scan the QR code and log in...")
time.sleep(15)  

def check_unread_messages():
    """Check unread messages"""
    reminder_messages = []

    try:
      
        chats = driver.find_elements(By.XPATH, "//div[@class='_2aBzC']")
        for chat in chats:
            try:
                contact_name = chat.find_element(By.XPATH, ".//span[@title]").text
                new_message = chat.find_element(By.XPATH, ".//div[@class='_1pJ9J']").text  
                if new_message:
                    time_sent = time.strftime("%H:%M", time.localtime())
                    reminder_messages.append(f"You have unread messages from {contact_name} at {time_sent}.")
            except:
               
                continue
    except Exception as e:
        print(f"Error checking messages: {e}")
    
    return reminder_messages

def make_audio_notification(messages):
    """Read out unread messages in Turkish"""
    engine = pyttsx3.init()
    
    
    engine.setProperty('rate', 100)  
    engine.setProperty('volume', 1)  
    voices = engine.getProperty('voices')
    
    
    for voice in voices:
        if "Turkish" in voice.languages:
            engine.setProperty('voice', voice.id)
            break

    if messages:
        for message in messages:
            engine.say(message)
        engine.runAndWait()
    else:
        engine.say("You have no unread messages today.")
        engine.runAndWait()

def send_whatsapp_message(messages):
    """Send a notification to yourself on WhatsApp"""
    try:
        
        driver.get("https://web.whatsapp.com/send?phone=+905xxxxxxxxx")  
        time.sleep(10)  

       
        message_box = driver.find_element(By.XPATH, "//div[@title='Type a message']")
        if messages:
            notification_message = "You have unread messages from the following people:\n" + "\n".join(messages)
            message_box.send_keys(notification_message)
        else:
            message_box.send_keys("You have no unread messages today.")
        
        
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[@data-testid='compose-btn-send']").click()
        print("Message sent successfully.")
    except Exception as e:
        print(f"Error sending message: {e}")

def reminder_task():
    """Check unread messages, make audio notification, and send WhatsApp message"""
    messages = check_unread_messages()
    make_audio_notification(messages)
    send_whatsapp_message(messages)


schedule.every().day.at("09:00").do(reminder_task)
schedule.every().day.at("23:53").do(reminder_task)


while True:
    schedule.run_pending()
    time.sleep(1)
