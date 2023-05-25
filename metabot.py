import os
from itertools import cycle
import openai
import colorama
import requests
from colorama import Fore, Style
from pyfiglet import Figlet
from time import sleep
import requests

openai.api_key = "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"
colorama.init()


def chat_with_ai(message, user_name):
    prompt = f"{user_name}: {message}\nAI:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()


def open_application(application_name):
    try:
        import subprocess
        subprocess.Popen(application_name)
        print(f"Bot: Opening {application_name}...")
    except OSError:
        print(f"Bot: Unable to open {application_name}. Please check the application name or path.")


def get_user_name():
    try:
        user_name = os.getlogin()
        return user_name
    except OSError:
        print("Bot: Unable to fetch your name. Please try again later.")
        return None


def animate_text(text):
    animation_chars = "|/-\\"
    for char in cycle(animation_chars):
        print(Fore.CYAN + "\r" + char + " " + text + " " + char, end="")
        sleep(0.1)


def prompt_user(user_name):
    user_input = input(Fore.GREEN + user_name + ": " + Style.RESET_ALL)
    if user_input.lower() == "exit":
        print(Fore.YELLOW + "Bot: Exiting..." + Style.RESET_ALL)
        return False
    elif user_input.lower() == "menu":
        print_menu()
    else:
        perform_task(user_input, user_name)
    return True


def print_welcome_message(user_name):
    f = Figlet(font="slant")
    welcome_message = f.renderText("Metabot")
    print(Fore.CYAN + welcome_message + Style.RESET_ALL)
    print(Fore.YELLOW + f"Welcome {user_name}! I'm here to assist you. Ask me anything or type 'menu' to see the available options." + Style.RESET_ALL)
    print(Fore.MAGENTA + "Bot Made By Coderet D Looper" + Style.RESET_ALL)


def print_menu():
    print("Bot: Here are the available options:")
    print("- Greet: Say hello to the bot.")
    print("- Time: Get the current time.")
    print("- Weather: Get the current weather.")
    print("- IP: Get IP address information and location.")
    print("- Open [application name]: Open a specific application.")
    print("- Help: Get assistance with the available tasks.")
    print("- Exit: Terminate the bot.")


def perform_task(task, user_name):
    if task.lower() == "greet":
        print(f"Bot: Hello {user_name}! How can I assist you?")
    elif task.lower() == "time":
        animate_text("Fetching current time...")
        print("\n")
        get_current_time(user_name)
    elif task.lower() == "weather":
        animate_text("Fetching current weather...")
        print("\n")
        get_current_weather(user_name)
    elif task.lower() == "ip":
        animate_text("Fetching IP address information and location...")
        print("\n")
        get_ip_address_info()
    elif task.lower().startswith("open "):
        application_name = task[5:]
        open_application(application_name)
    elif task.lower() == "help":
        print("Bot: I can assist you with various tasks such as providing the current time, weather information, IP address information and location, opening applications, and more. Feel free to ask me anything!")
    else:
        response = chat_with_ai(task, user_name)
        print("Bot:", response)


def get_current_time(user_name):
    # Implementation to fetch current time
    pass


def get_current_weather(user_name):
    api_key = "1b9d8f81de21499b82965123232505"
    base_url = "https://www.weatherapi.com"
    city = input("Enter your city: ")
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if weather_data.get("cod") == 200:
        weather_description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]

        print(f"Bot: The current weather in {city} is {weather_description}.")
        print(f"Bot: Temperature: {temperature}°C, Humidity: {humidity}%")
    else:
        print("Bot: Failed to fetch weather information. Please try again later.")


def get_ip_address_info():
    ip_address = input("Enter IP address (or leave empty for your current IP address): ")
    if not ip_address:
        ip_address = requests.get("https://api.ipify.org").text

    api_key = "YOUR_IPSTACK_API_KEY"
    base_url = f"http://api.ipstack.com/{ip_address}"
    params = {
        "aa4cb093dd4e9e1e5239582f962f7655": api_key
    }
    response = requests.get(base_url, params=params)
    ip_data = response.json()

    if ip_data.get("success"):
        ip_info = {
            "IP Address": ip_data["ip"],
            "Continent": ip_data["continent_name"],
            "Country": ip_data["country_name"],
            "Region": ip_data["region_name"],
            "City": ip_data["city"],
            "Latitude": ip_data["latitude"],
            "Longitude": ip_data["longitude"],
        }

        print("Bot: IP Address Information and Location:")
        for key, value in ip_info.items():
            print(f"- {key}: {value}")
    else:
        print("Bot: Failed to fetch IP address information. Please try again later.")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def run_chatbot():
    user_name = get_user_name()
    if user_name:
        print_welcome_message(user_name)
        sleep(2)
        clear_console()
        while True:
            if not prompt_user(user_name):
                break
            print("\n")
    else:
        print("Bot: Unable to determine your name. Exiting...")


run_chatbot()
