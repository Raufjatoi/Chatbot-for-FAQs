import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import os
import wikipedia
import requests
import random

# Set page title and icon
st.set_page_config(page_title="Simple FAQ Chatbot", page_icon="🤖")

# Define the knowledge base (Questions and Answers)
knowledge_base = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hello! How can I help you?",
    "hey": "Hey there! How can I assist you?",
    "how are you": "I'm doing well, thank you for asking!",
    "what is your name": "I'm a simple FAQ chatbot.",
    "how can I improve my mental health": "There are many ways to improve mental health, such as exercising regularly, practicing mindfulness, and seeking support from loved ones or professionals.",
    "where can I find mental health resources": "You can find mental health resources online, through community centers, or by consulting with healthcare professionals.",
    "what should I do if I feel anxious": "If you feel anxious, it's helpful to practice relaxation techniques, take deep breaths, and consider speaking with a therapist.",
    "what are the symptoms of depression": "Symptoms of depression include persistent sadness, loss of interest in activities, changes in appetite or sleep patterns, and feelings of worthlessness.",
    "thank you": "You're welcome!",
            "hi": "Hello there! How can I help you?",
            "hello": "Hi! What can I do for you today?",
            "hey": "Hey! How can I assist you?",
            "hola": "Hola! ¿En qué puedo ayudarte?",
            "howdy": "Howdy! What can I do for you?",
            "greetings": "Greetings! How can I assist you?",
            "huh": "What happened? How can I assist you?",
            "what's up": "Not much, just here to help you!",
            "sup": "Not much, just here to assist you!",
            "yo": "Yo! How can I help you today?",
            "hey there": "Hey there! What can I do for you?",
            "good morning": "Good morning! How can I assist you today?",
            "good afternoon": "Good afternoon! How can I help you?",
            "good evening": "Good evening! What can I do for you?",
            "how are you": "I'm doing well, thank you for asking. How can I assist you?",
            "how's it going": "It's going well! How can I help you today?",
            "what can you do": "I can assist you with a variety of tasks. Feel free to ask me anything!",
            "thank you": "You're welcome! If you need anything else, just let me know.",
            "thanks": "You're welcome! How else may I assist you?",
            "bye": "Goodbye! Have a great day!",
            "goodbye": "Goodbye! Take care!",
            "see you later": "See you later! Let me know if you need anything else.",
            "adios": "Adiós! Que tengas un buen día!",
         
    "idk": "No worries, I can help you with that!",
    "idc": "It's okay, I'm here to help!",
    "lol": "Haha! What's so funny?",
    "brb": "Sure, I'll be here when you get back!",
    "ttyl": "Talk to you later!",
    "btw": "By the way, how can I assist you?",
    "omg": "Oh my! How can I help?",
    "yw": "You're welcome!",
    "ikr": "I know, right?",
    "tbh": "To be honest, I'm here to help you with anything!",
    "smh": "I understand, how can I assist you?",
    "np": "No problem at all!",
    "fyi": "For your information, I'm here to help with any questions you have!",
    "jk": "Just kidding! How can I assist you?",
    "rn": "Right now, I'm ready to help you!",
    "gg": "Good game! How can I assist you next?",
    "bff": "Best friends forever! How can I assist you?",
    "rofl": "Rolling on the floor laughing! What's so funny?",
    "thx": "You're welcome! How else can I help?",
    "gr8": "Great! How can I assist you?",
    "u2": "You too! How can I help you?",
    "lmk": "Let me know how I can assist you!",
    "wtf": "Oh no! How can I assist you?",
    "yo": "Yo! How can I help you today?",
    "nah": "Alright, let me know if you need anything else.",
    "yolo": "You only live once! How can I assist you today?",
    "ik": "I know! How can I help you?",
    "nvm": "Never mind! Let me know if you need anything else.",
    "pls": "Sure, please let me know how I can assist you!",
    "ppl": "People are great! How can I help you?",
    "hru": "im fine wbu ? ",
    "im good" : "ohh nice ",
    "what is dit": "dit stands for diploma in information technoly ",
    
    "goodnight": "Goodnight! Sleep well!",
    "evening": "Good evening! How can I assist you?",
    "morning": "Good morning! How can I help you today?",
    "afternoon": "Good afternoon! What can I do for you?",
    "how do you do": "I'm doing well, thank you. How can I assist you?",
    "long time no see": "Indeed, it's been a while! How can I help you today?",
    "welcome": "Thank you! How can I assist you?",
    "what's new": "Not much, just here to help you! What's new with you?",
    "how's everything": "Everything is good, thanks! How can I assist you?",
    "howdy partner": "Howdy, partner! What can I do for you?",
    "salutations": "Salutations! How can I assist you?",
    "how goes it": "It's going well! How can I help you?",
    "what's happening": "Not much, just here to assist you!",
    "what's good": "Everything's good! How can I help you?",
    "yo yo": "Yo yo! How can I help you today?",
    "how are you doing": "I'm doing well, thank you. How can I assist you?",
    "what's the word": "Not much, just here to help you! What's the word?",
    "yo bro": "Yo bro! How can I help you?",
    "hey man": "Hey man! What can I do for you?",
    "g'day": "G'day! How can I assist you?",
    "how's it hanging": "It's hanging well! How can I help you?",
    "top of the morning": "Top of the morning to you! How can I assist you?",
    "hiya": "Hiya! How can I help you?",
    "wassup": "Wassup! How can I assist you?",
    "hello there": "Hello there! How can I help you?",
    "how's life": "Life is good! How can I assist you?",
    "good day": "Good day! How can I help you?",
    "pleasure to meet you": "Pleasure to meet you too! How can I assist you?",
    "yo dude": "Yo dude! How can I help you?",
    "good to see you": "Good to see you too! How can I assist you?",
    "what's cracking": "Not much, just here to help! What's cracking with you?",
    "how's your day": "My day is going well, thank you. How can I assist you?",
    "good to hear from you": "Good to hear from you too! How can I help you?",
    "all good": "All good here! How can I assist you?",
    "yo yo yo": "Yo yo yo! How can I help you today?",
    "what's cooking": "Not much, just here to assist you! What's cooking with you?",
    "holla": "Holla! How can I help you?",
    "how's it looking": "It's looking good! How can I assist you?",
    "hey buddy": "Hey buddy! What can I do for you?",
    "cheers": "Cheers! How can I assist you?",
    "hiya mate": "Hiya mate! How can I help you?",
    "hey you": "Hey you! How can I assist you?",
    "what's up dude": "Not much, just here to help! What's up with you?",
    "yo what's up": "Yo! Not much, just here to help. How can I assist you?",
    "how are things": "Things are good! How can I help you?",
    "how's your day going": "My day is going well, thank you. How can I assist you?",
    "what's popping": "Not much, just here to assist you! What's popping with you?",
    "hey pal": "Hey pal! What can I do for you?",
    "how's it going mate": "It's going well, mate! How can I assist you?",
    "hey there friend": "Hey there, friend! How can I help you?",
    "what is 2+2": "2+2 is 4.",
    "what is the square root of 16": "The square root of 16 is 4.",
    "solve for x: 2x + 3 = 7": "To solve for x: 2x + 3 = 7, subtract 3 from both sides to get 2x = 4, then divide both sides by 2 to get x = 2.",
    "what is pi": "Pi (π) is approximately 3.14159, and it's the ratio of the circumference of a circle to its diameter.",
    "convert 100 meters to kilometers": "100 meters is 0.1 kilometers.",
    "what is the derivative of x^2": "The derivative of x^2 is 2x.",
    "integrate x^3": "The integral of x^3 is (1/4)x^4 + C, where C is the constant of integration.",
    "what is the area of a circle": "The area of a circle is πr^2, where r is the radius.",
    "how many sides does a hexagon have": "A hexagon has 6 sides.",
    "what is the formula for the Pythagorean theorem": "The Pythagorean theorem formula is a^2 + b^2 = c^2.",
    "convert 45 degrees to radians": "45 degrees is π/4 radians.",
    "what is the factorial of 5": "The factorial of 5 is 5! = 5 × 4 × 3 × 2 × 1 = 120.",
    "what is the sum of the angles in a triangle": "The sum of the angles in a triangle is 180 degrees.",
    "what is 7 times 8": "7 times 8 is 56.",
    "how many milliliters in a liter": "There are 1000 milliliters in a liter.",
    "what is the perimeter of a rectangle": "The perimeter of a rectangle is 2(length + width).",
    "what is the value of e": "The value of e (Euler's number) is approximately 2.71828.",
    "what is a prime number": "A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.",
    "how many inches in a foot": "There are 12 inches in a foot.",
    "convert 100 Fahrenheit to Celsius": "100 Fahrenheit is approximately 37.78 Celsius.",
    "what is the volume of a sphere": "The volume of a sphere is (4/3)πr^3, where r is the radius.",
    "what is the circumference of a circle": "The circumference of a circle is 2πr, where r is the radius.",
    "how many seconds in an hour": "There are 3600 seconds in an hour.",
    "what is the quadratic formula": "The quadratic formula is x = (-b ± √(b^2 - 4ac)) / 2a.",
    "what is an isosceles triangle": "An isosceles triangle is a triangle with at least two sides of equal length.",
    "simplify (x + 2)(x - 3)": "Simplifying (x + 2)(x - 3) gives x^2 - x - 6.",
    "what is the mode in statistics": "The mode is the value that appears most frequently in a data set.",
    "what is the median in statistics": "The median is the middle value in a data set when the numbers are arranged in order.",
    "what is the mean in statistics": "The mean is the average of a set of numbers, calculated by dividing the sum of the values by the number of values.",
    "what is the standard deviation": "The standard deviation is a measure of the amount of variation or dispersion in a set of values.",
    "what is a right angle": "A right angle is an angle of 90 degrees.",
    "how many degrees in a circle": "There are 360 degrees in a circle.",
    "what is 10 to the power of 3": "10 to the power of 3 is 1000",
    "who are you": "I'm a chatbot designed to assist you with various tasks and answer your questions.",
    "what is your purpose": "My purpose is to help users by providing information and assistance.",
    "where are you from": "I exist in the digital realm, here to assist you wherever you are!",
    "what is the capital of France": "The capital of France is Paris.",
    "who is the president of the United States": "As of my last update, the President of the United States is Joe Biden.",
    "what is the population of China": "As of my last update, the population of China is over 1.4 billion people.",
    "how many continents are there": "There are seven continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia.",
    "what is the tallest mountain in the world": "Mount Everest is the tallest mountain in the world, located in the Himalayas.",
    "what is the largest ocean": "The Pacific Ocean is the largest ocean on Earth.",
    "what is the speed of light": "The speed of light in a vacuum is approximately 299,792 kilometers per second.",
    "what is the boiling point of water": "The boiling point of water at standard atmospheric pressure is 100 degrees Celsius or 212 degrees Fahrenheit.",
    "what is the currency of Japan": "The currency of Japan is the Japanese yen.",
    "what is the chemical symbol for gold": "The chemical symbol for gold is Au.",
    "what is the capital of Australia": "The capital of Australia is Canberra.",
    "what is the formula for water": "The chemical formula for water is H2O.",
    "what is the distance from the Earth to the Moon": "The average distance from the Earth to the Moon is about 384,400 kilometers.",
    "what is the largest animal in the world": "The blue whale is the largest animal in the world.",
    "what is the tallest building in the world": "As of my last update, the tallest building in the world is the Burj Khalifa in Dubai, United Arab Emirates",
    "what is the capital of Canada": "The capital of Canada is Ottawa.",
    "what is the largest desert in the world": "The largest desert in the world is the Sahara Desert.",
    "what is the longest river in the world": "The longest river in the world is the Nile River.",
    "what is the tallest tree in the world": "The tallest tree in the world is Hyperion, a coast redwood tree located in California, USA.",
    "what is the hottest place on Earth": "The hottest place on Earth is the Lut Desert in Iran, where temperatures can reach extreme levels.",
    "what is the chemical symbol for oxygen": "The chemical symbol for oxygen is O2.",
    "what is the atomic number of carbon": "The atomic number of carbon is 6.",
    "what is the largest planet in the solar system": "The largest planet in the solar system is Jupiter.",
    "what is the smallest country in the world": "The smallest country in the world is Vatican City.",
    "what is the highest mountain range in the world": "The highest mountain range in the world is the Himalayas.",
    "what is the largest lake in the world": "The largest lake in the world by surface area is the Caspian Sea.",
    "what is the capital of Brazil": "The capital of Brazil is Brasília.",
    "what is the currency of India": "The currency of India is the Indian Rupee.",
    "what is the chemical symbol for sodium": "The chemical symbol for sodium is Na.",
    "what is the capital of Russia": "The capital of Russia is Moscow.",
    "what is the speed of sound": "The speed of sound in air at room temperature is approximately 343 meters per second.",
    "what is the boiling point of mercury": "The boiling point of mercury is 356.7 degrees Celsius or 674.1 degrees Fahrenheit.",
    "what is the formula for photosynthesis": "The general formula for photosynthesis is 6CO2 + 6H2O + light energy -> C6H12O6 + 6O2.",
    "what is the capital of China": "The capital of China is Beijing.",
    "what is the capital of France": "The capital of France is Paris.",
    "what is the currency of Japan": "The currency of Japan is the Japanese Yen.",
    "what is the chemical symbol for gold": "The chemical symbol for gold is Au.",
    "what is the population of the United States": "As of the latest data, the population of the United States is over 330 million people.",
    "what is the tallest mountain in the world": "The tallest mountain in the world is Mount Everest, located in the Himalayas.",
    "what is the largest ocean in the world": "The largest ocean in the world is the Pacific Ocean.",
    "what is the chemical symbol for water": "The chemical symbol for water is H2O.",
    "what is the population of China": "As of the latest data, the population of China is over 1.4 billion people, making it the most populous country in the world.",
    "what is the distance from the Earth to the Sun": "The average distance from the Earth to the Sun, known as an astronomical unit (AU), is approximately 93 million miles or 150 million kilometers.",
    "what is the chemical symbol for carbon dioxide": "The chemical symbol for carbon dioxide is CO2.",
    "what is the population of India": "As of the latest data, the population of India is over 1.3 billion people.",
    "what is the tallest building in the world": "The tallest building in the world is the Burj Khalifa, located in Dubai, United Arab Emirates.",
    "what is the chemical symbol for iron": "The chemical symbol for iron is Fe.",
    "what is the population of Russia": "As of the latest data, the population of Russia is over 145 million people.",
    "what is the longest mountain range in the world": "The longest mountain range in the world is the Andes, located in South America.",
    "what is the chemical symbol for hydrogen": "The chemical symbol for hydrogen is H.",
    "what is the population of Brazil": "As of the latest data, the population of Brazil is over 210 million people.",
    "what is the tallest waterfall in the world": "The tallest waterfall in the world is Angel Falls, located in Venezuela.",
    "what is the chemical symbol for silver": "The chemical symbol for silver is Ag.",
    "what is the population of Japan": "As of the latest data, the population of Japan is over 126 million people.",

    "what is the capital of Australia": "The capital of Australia is Canberra.",
    "what is the currency of the United Kingdom": "The currency of the United Kingdom is the British Pound Sterling (GBP).",
    "what is the chemical symbol for carbon monoxide": "The chemical symbol for carbon monoxide is CO.",
    "what is the population of Germany": "As of the latest data, the population of Germany is over 83 million people.",
    "what is the deepest ocean trench": "The deepest ocean trench is the Mariana Trench, located in the western Pacific Ocean.",
    "what is the chemical symbol for nitrogen": "The chemical symbol for nitrogen is N.",
    "what is the population of Mexico": "As of the latest data, the population of Mexico is over 126 million people.",
    "what is the largest animal on Earth": "The largest animal on Earth is the blue whale.",
    "what is the chemical symbol for calcium": "The chemical symbol for calcium is Ca.",
    "what is the population of Nigeria": "As of the latest data, the population of Nigeria is over 206 million people.",
    "what is the largest island in the world": "The largest island in the world is Greenland.",
    "what is the chemical symbol for potassium": "The chemical symbol for potassium is K.",
    "what is the population of France": "As of the latest data, the population of France is over 67 million people.",
    "what is the longest glacier in the world": "The longest glacier in the world is the Lambert Glacier in Antarctica.",
    "what is the chemical symbol for aluminum": "The chemical symbol for aluminum is Al.",
    "what is the population of Egypt": "As of the latest data, the population of Egypt is over 104 million people.",
    "what is the deepest point in the ocean": "The deepest point in the ocean is the Challenger Deep, located in the Mariana Trench.",
    "what is the chemical symbol for uranium": "The chemical symbol for uranium is U.",
    "what is the population of Italy": "As of the latest data, the population of Italy is over 60 million people.",
    "what is the largest bird in the world": "The largest bird in the world is the ostrich.",
    "what is the capital of Russia": "The capital of Russia is Moscow.",
    "what is the currency of Japan": "The currency of Japan is the Japanese Yen.",
    "what is the chemical symbol for gold": "The chemical symbol for gold is Au.",
    "what is the population of the United States": "As of the latest data, the population of the United States is over 330 million people.",
    "what is the tallest mountain in the world": "The tallest mountain in the world is Mount Everest, located in the Himalayas.",
    "what is the largest ocean in the world": "The largest ocean in the world is the Pacific Ocean.",
    "what is the chemical symbol for water": "The chemical symbol for water is H2O.",
    "what is the population of China": "As of the latest data, the population of China is over 1.4 billion people, making it the most populous country in the world.",
    "what is the distance from the Earth to the Sun": "The average distance from the Earth to the Sun, known as an astronomical unit (AU), is approximately 93 million miles or 150 million kilometers.",
    "what is the chemical symbol for carbon dioxide": "The chemical symbol for carbon dioxide is CO2.",
    "what is the population of India": "As of the latest data, the population of India is over 1.3 billion people.",
    "what is the tallest building in the world": "The tallest building in the world is the Burj Khalifa, located in Dubai, United Arab Emirates.",
    "what is the chemical symbol for iron": "The chemical symbol for iron is Fe.",
    "what is the population of Russia": "As of the latest data, the population of Russia is over 145 million people.",
    "what is the longest mountain range in the world": "The longest mountain range in the world is the Andes, located in South America.",
    "what is the chemical symbol for hydrogen": "The chemical symbol for hydrogen is H.",
    "what is the population of Brazil": "As of the latest data, the population of Brazil is over 210 million people.",
    "what is the tallest waterfall in the world": "The tallest waterfall in the world is Angel Falls, located in Venezuela.",
    "what is the chemical symbol for silver": "The chemical symbol for silver is Ag.",
    "what is the population of Japan": "As of the latest data, the population of Japan is over 126 million people.",
    "what is the capital of Pakistan": "The capital of Pakistan is Islamabad.",
    "what is the currency of Pakistan": "The currency of Pakistan is the Pakistani Rupee (PKR).",
    "what is the population of Pakistan": "As of the latest data, the population of Pakistan is over 220 million people.",
    "what is the largest mountain range in Pakistan": "The largest mountain range in Pakistan is the Karakoram Range, which includes some of the world's highest peaks such as K2.",
    "what is the national animal of Pakistan": "The national animal of Pakistan is the Markhor, a type of wild goat native to the mountainous regions of Pakistan.",
    "what is the famous food of Pakistan": "Some famous foods of Pakistan include biryani, nihari, kebabs, and chapli kebabs, as well as various types of bread like naan and roti.",
    "what is the official language of Pakistan": "The official language of Pakistan is Urdu.",
    "what is the national sport of Pakistan": "The national sport of Pakistan is Field Hockey.",
    "what is the national flower of Pakistan": "The national flower of Pakistan is Jasmine.",
    "what is the national monument of Pakistan": "The national monument of Pakistan is Minar-e-Pakistan.",
    "when is Independence Day in Pakistan": "Independence Day in Pakistan is celebrated on August 14th.",
    "what is the national anthem of Pakistan": "The national anthem of Pakistan is Qaumi Taranah.",
    "what is the area of Pakistan": "Pakistan covers an area of 881,913 square kilometers.",
    "which countries border Pakistan": "Pakistan shares borders with India, Afghanistan, Iran, and China.",
    "what are the major rivers in Pakistan": "Some major rivers in Pakistan include the Indus River, Jhelum River, Chenab River, Ravi River, and Sutlej River.",
    "what is the climate of Pakistan": "The climate of Pakistan varies from tropical to temperate.",
    "what are the religions in Pakistan": "The majority religion in Pakistan is Islam, while minority religions include Hinduism, Christianity, Sikhism, and others.",

    "what is the capital of India": "The capital of India is New Delhi.",
    "what is the currency of India": "The currency of India is the Indian Rupee (INR).",
    "what is the population of India": "As of the latest data, the population of India is over 1.3 billion people.",
    "what is the largest mountain range in India": "The largest mountain range in India is the Himalayas, home to some of the world's highest peaks including Mount Everest.",
    "what is the national animal of India": "The national animal of India is the Bengal Tiger.",
    "what is the famous food of India": "Some famous foods of India include biryani, curry, samosas, dosas, and roti.",
    "what is the official language of India": "India has 22 officially recognized languages, with Hindi and English being the official languages at the national level.",
    "what is the national sport of India": "The national sport of India is Field Hockey, although cricket is also widely popular.",
    "what is the national flower of India": "The national flower of India is the Lotus.",
    "what is the national monument of India": "The national monument of India is the Red Fort (Lal Qila) in Delhi.",
    "when is Independence Day in India": "Independence Day in India is celebrated on August 15th.",
    "what is the national anthem of India": "The national anthem of India is Jana Gana Mana.",
    "what is the area of India": "India covers an area of 3.287 million square kilometers.",
    "which countries border India": "India shares borders with Pakistan, China, Nepal, Bhutan, Bangladesh, and Myanmar.",
    "what are the major rivers in India": "Some major rivers in India include the Ganges, Yamuna, Brahmaputra, and Indus.",
    "what is the climate of India": "The climate of India varies from tropical in the south to temperate in the north.",
    "what are the religions in India": "India is a diverse country with various religions including Hinduism, Islam, Christianity, Sikhism, Buddhism, and Jainism, among others.",
    "what is the capital of China": "The capital of China is Beijing.",
    "what is the currency of China": "The currency of China is the Chinese Yuan Renminbi (CNY).",
    "what is the population of China": "As of the latest data, the population of China is over 1.4 billion people, making it the most populous country in the world.",
    "what is the largest mountain range in China": "The largest mountain range in China is the Himalayas, which also extends into neighboring countries like India and Nepal.",
    "what is the national animal of China": "The national animal of China is the Giant Panda.",
    "what is the famous food of China": "Some famous foods of China include dumplings, noodles, Peking duck, and Kung Pao chicken.",
    "what is the official language of China": "The official language of China is Standard Mandarin.",
    "what is the national sport of China": "The national sport of China is table tennis, also known as ping pong.",
    "what is the national flower of China": "The national flower of China is the Peony.",
    "what is the national monument of China": "The national monument of China is the Great Wall of China.",
    "when is National Day in China": "National Day in China is celebrated on October 1st.",
    "what is the area of China": "China covers an area of approximately 9.6 million square kilometers.",
    "which countries border China": "China shares borders with 14 countries including India, Russia, Mongolia, Pakistan, and others.",
    "what are the major rivers in China": "Some major rivers in China include the Yangtze River, Yellow River, and Pearl River.",
    "what is the climate of China": "The climate of China varies from tropical in the south to subarctic in the north.",
    "what are the religions in China": "The main religions practiced in China include Buddhism, Taoism, Islam, and Christianity.",

    "what is the capital of Japan": "The capital of Japan is Tokyo.",
    "what is the currency of Japan": "The currency of Japan is the Japanese Yen (JPY).",
    "what is the population of Japan": "As of the latest data, the population of Japan is over 126 million people.",
    "what is the largest mountain range in Japan": "The largest mountain range in Japan is the Japanese Alps.",
    "what is the national animal of Japan": "The national animal of Japan is the Green Pheasant.",
    "what is the famous food of Japan": "Some famous foods of Japan include sushi, ramen, tempura, and yakitori.",
    "what is the official language of Japan": "The official language of Japan is Japanese.",
    "what is the national sport of Japan": "The national sport of Japan is Sumo wrestling.",
    "what is the national flower of Japan": "The national flower of Japan is the Cherry Blossom (Sakura).",
    "what is the national monument of Japan": "The national monument of Japan is Mount Fuji.",
    "when is National Foundation Day in Japan": "National Foundation Day in Japan is celebrated on February 11th.",
    "what is the area of Japan": "Japan covers an area of approximately 377,975 square kilometers.",
    "which countries border Japan": "Japan is an island nation and does not share land borders with any other country.",
    "what are the major rivers in Japan": "Some major rivers in Japan include the Shinano River, Tone River, and Ishikari River.",
    "what is the climate of Japan": "The climate of Japan varies from subtropical in the south to temperate in the north.",
    "what are the religions in Japan": "The main religions practiced in Japan include Shintoism and Buddhism.",

    "what is Naruto about": "Naruto follows the journey of Naruto Uzumaki, a young ninja seeking recognition and dreaming of becoming the Hokage, the village leader.",
    "how many episodes does Naruto have": "Naruto has 220 episodes.",
    "when was Naruto released": "Naruto was released in 2002.",
    "what is the IMDb rating of Naruto": "The IMDb rating of Naruto is 8.3/10.",

    "what is One Piece about": "One Piece follows Monkey D. Luffy and his pirate crew in their quest to find the One Piece treasure and become the Pirate King.",
    "how many episodes does One Piece have": "One Piece has over 1000 episodes.",
    "when was One Piece released": "One Piece was released in 1999.",
    "what is the IMDb rating of One Piece": "The IMDb rating of One Piece is 8.7/10.",

    "what is Attack on Titan about": "Attack on Titan depicts humanity's struggle for survival against giant humanoid creatures known as Titans, set in a world where humanity resides within enormous walled cities to protect themselves from Titans.",
    "how many episodes does Attack on Titan have": "Attack on Titan has 75 episodes.",
    "when was Attack on Titan released": "Attack on Titan was released in 2013.",
    "what is the IMDb rating of Attack on Titan": "The IMDb rating of Attack on Titan is 8.9/10.",

    "what is Dragon Ball Z about": "Dragon Ball Z follows the adventures of Goku and his friends as they defend Earth against villains and search for the Dragon Balls.",
    "how many episodes does Dragon Ball Z have": "Dragon Ball Z has 291 episodes.",
    "when was Dragon Ball Z released": "Dragon Ball Z was released in 1989.",
    "what is the IMDb rating of Dragon Ball Z": "The IMDb rating of Dragon Ball Z is 8.7/10.",

    "what is Death Note about": "Death Note follows high school student Light Yagami after he discovers a supernatural notebook that allows him to kill anyone by writing their name while picturing their face.",
    "how many episodes does Death Note have": "Death Note has 37 episodes.",
    "when was Death Note released": "Death Note was released in 2006.",
    "what is the IMDb rating of Death Note": "The IMDb rating of Death Note is 9.0/10.",

    "what is Fullmetal Alchemist: Brotherhood about": "Fullmetal Alchemist: Brotherhood follows two brothers, Edward and Alphonse Elric, as they seek the Philosopher's Stone to restore their bodies after a failed alchemical experiment.",
    "how many episodes does Fullmetal Alchemist: Brotherhood have": "Fullmetal Alchemist: Brotherhood has 64 episodes.",
    "when was Fullmetal Alchemist: Brotherhood released": "Fullmetal Alchemist: Brotherhood was released in 2009.",
    "what is the IMDb rating of Fullmetal Alchemist: Brotherhood": "The IMDb rating of Fullmetal Alchemist: Brotherhood is 9.1/10.",

    "what is My Hero Academia about": "My Hero Academia is set in a world where people with superpowers, known as Quirks, are common. It follows Izuku Midoriya, a Quirkless boy who dreams of becoming a hero.",
    "how many episodes does My Hero Academia have": "My Hero Academia has 106 episodes.",
    "when was My Hero Academia released": "My Hero Academia was released in 2016.",
    "what is the IMDb rating of My Hero Academia": "The IMDb rating of My Hero Academia is 8.4/10.",

    "what is Sword Art Online about": "Sword Art Online follows players trapped in a virtual reality MMORPG where death in the game means death in real life.",
    "how many episodes does Sword Art Online have": "Sword Art Online has 98 episodes.",
    "when was Sword Art Online released": "Sword Art Online was released in 2012.",
    "what is the IMDb rating of Sword Art Online": "The IMDb rating of Sword Art Online is 7.6/10.",

    "what is Demon Slayer: Kimetsu no Yaiba about": "Demon Slayer: Kimetsu no Yaiba follows Tanjiro Kamado, a young boy who becomes a demon slayer to avenge his family and cure his sister, Nezuko, who has been turned into a demon.",
    "how many episodes does Demon Slayer: Kimetsu no Yaiba have": "Demon Slayer: Kimetsu no Yaiba has 26 episodes.",
    "when was Demon Slayer: Kimetsu no Yaiba released": "Demon Slayer: Kimetsu no Yaiba was released in 2019.",
    "what is the IMDb rating of Demon Slayer: Kimetsu no Yaiba": "The IMDb rating of Demon Slayer: Kimetsu no Yaiba is 8.7/10.",

    "what is Hunter x Hunter about": "Hunter x Hunter follows Gon Freecss as he becomes a Hunter to find his father and uncover the secrets of the Hunter world.",
    "how many episodes does Hunter x Hunter have": "Hunter x Hunter has 148 episodes.",
    "when was Hunter x Hunter released": "Hunter x Hunter was released in 2011.",
    "what is the IMDb rating of Hunter x Hunter": "The IMDb rating of Hunter x Hunter is 8.9/10.",
    "what is Titanic about": "Titanic is a romantic disaster film directed by James Cameron, depicting the ill-fated maiden voyage of the RMS Titanic. It follows the love story between Jack Dawson, a poor artist, and Rose DeWitt Bukater, a young woman from a wealthy family.",
    "when was Titanic released": "Titanic was released in 1997.",
    "what is the IMDb rating of Titanic": "The IMDb rating of Titanic is 7.8/10.",

    "what is Avatar about": "Avatar is a science fiction film directed by James Cameron, set in the mid-22nd century when humans are colonizing the alien world of Pandora. The story follows a paraplegic Marine named Jake Sully, who becomes torn between following orders and protecting the indigenous Na'vi people.",
    "when was Avatar released": "Avatar was released in 2009.",
    "what is the IMDb rating of Avatar": "The IMDb rating of Avatar is 7.8/10.",

    "what is The Dark Knight about": "The Dark Knight is a superhero film directed by Christopher Nolan, based on the DC Comics character Batman. It follows Batman's struggle to dismantle organized crime in Gotham City with the help of Lieutenant James Gordon and district attorney Harvey Dent, while facing the chaotic Joker.",
    "when was The Dark Knight released": "The Dark Knight was released in 2008.",
    "what is the IMDb rating of The Dark Knight": "The IMDb rating of The Dark Knight is 9.0/10.",

    "what is Inception about": "Inception is a science fiction action film directed by Christopher Nolan, exploring the concept of dreams within dreams. It follows a skilled thief who is capable of entering the dreams of others to steal their secrets.",
    "when was Inception released": "Inception was released in 2010.",
    "what is the IMDb rating of Inception": "The IMDb rating of Inception is 8.8/10.",

    "what is Interstellar about": "Interstellar is a science fiction film directed by Christopher Nolan, following a group of astronauts who travel through a wormhole near Saturn in search of a new habitable planet for humanity, as Earth faces environmental collapse.",
    "when was Interstellar released": "Interstellar was released in 2014.",
    "what is the IMDb rating of Interstellar": "The IMDb rating of Interstellar is 8.6/10.",

    "what is Avengers: Endgame about": "Avengers: Endgame is a superhero film directed by Anthony and Joe Russo, serving as the culmination of the Marvel Cinematic Universe's Infinity Saga. It follows the Avengers as they attempt to undo the damage caused by Thanos and restore balance to the universe.",
    "when was Avengers: Endgame released": "Avengers: Endgame was released in 2019.",
    "what is the IMDb rating of Avengers: Endgame": "The IMDb rating of Avengers: Endgame is 8.4/10.",

    "what is Gladiator about": "Gladiator is a historical epic directed by Ridley Scott, set in ancient Rome and following the journey of a betrayed Roman general who seeks revenge against the corrupt emperor who murdered his family and sent him into slavery.",
    "when was Gladiator released": "Gladiator was released in 2000.",
    "what is the IMDb rating of Gladiator": "The IMDb rating of Gladiator is 8.5/10.",

    "what is The Shawshank Redemption about": "The Shawshank Redemption is a drama film directed by Frank Darabont, based on the Stephen King novella 'Rita Hayworth and Shawshank Redemption.' It follows the story of Andy Dufresne, a banker who is sentenced to life in Shawshank State Penitentiary for the murder of his wife and her lover, despite his claims of innocence.",
    "when was The Shawshank Redemption released": "The Shawshank Redemption was released in 1994.",
    "what is the IMDb rating of The Shawshank Redemption": "The IMDb rating of The Shawshank Redemption is 9.3/10.",

    "what is 3 Idiots about": "3 Idiots is a comedy-drama film directed by Rajkumar Hirani, based on the novel 'Five Point Someone' by Chetan Bhagat. It follows the friendship of three engineering students at an Indian engineering college and addresses the pressures of the Indian education system.",
    "when was 3 Idiots released": "3 Idiots was released in 2009.",
    "what is the IMDb rating of 3 Idiots": "The IMDb rating of 3 Idiots is 8.4/10.",

    "what is Dangal about": "Dangal is a biographical sports drama film directed by Nitesh Tiwari, based on the true story of wrestler Mahavir Singh Phogat and his daughters Geeta Phogat and Babita Kumari. It follows their journey to become world-class wrestlers despite societal and familial obstacles.",
    "when was Dangal released": "Dangal was released in 2016.",
    "what is the IMDb rating of Dangal": "The IMDb rating of Dangal is 8.4/10.",

    "what is PK about": "PK is a satirical comedy-drama film directed by Rajkumar Hirani, starring Aamir Khan as an alien who lands on Earth and questions religious superstitions and practices. It explores themes of spirituality, humanity, and cultural differences.",
    "when was PK released": "PK was released in 2014.",
    "what is the IMDb rating of PK": "The IMDb rating of PK is 8.1/10.",

    "what is Bajrangi Bhaijaan about": "Bajrangi Bhaijaan is a drama film directed by Kabir Khan, starring Salman Khan as a devout Hanuman devotee who embarks on a journey to reunite a mute Pakistani girl with her family in Pakistan.",
    "when was Bajrangi Bhaijaan released": "Bajrangi Bhaijaan was released in 2015.",
    "what is the IMDb rating of Bajrangi Bhaijaan": "The IMDb rating of Bajrangi Bhaijaan is 8.0/10.",
    "what is the capital of the United States": "The capital of the United States is Washington, D.C.",
    "what is the largest city in the United States": "The largest city in the United States is New York City.",
    "what is the population of the United States": "As of the latest data, the population of the United States is over 331 million people.",
    "what is the currency of the United States": "The currency of the United States is the United States Dollar (USD).",
    "what is the official language of the United States": "The United States does not have an official language at the federal level, but English is the most commonly spoken language.",

    "what is the capital of the United Kingdom": "The capital of the United Kingdom is London.",
    "what is the largest city in the United Kingdom": "The largest city in the United Kingdom is also London.",
    "what is the population of the United Kingdom": "As of the latest data, the population of the United Kingdom is over 68 million people.",
    "what is the currency of the United Kingdom": "The currency of the United Kingdom is the British Pound Sterling (GBP).",
    "what is the official language of the United Kingdom": "The official language of the United Kingdom is English.",
    "what is America": "America, officially known as the United States of America (USA), is a country located primarily in North America. It is comprised of 50 states, a federal district (Washington, D.C.), five major self-governing territories, and various possessions. The USA is the world's third-largest country by total area and population. It is known for its diverse culture, strong economy, and significant influence on global affairs.",
    "what is the capital of America": "The capital of America is Washington, D.C.",
    "what is the largest city in America": "The largest city in America is New York City.",
    "what is the population of America": "As of the latest data, the population of America is over 331 million people.",
    "what is the currency of America": "The currency of America is the United States Dollar (USD).",
    "what is the official language of America": "The United States does not have an official language at the federal level, but English is the most commonly spoken language.",

    "what is England": "England is a country that is part of the United Kingdom (UK) located in Europe. It shares land borders with Scotland to the north and Wales to the west and is bounded by the North Sea to the east and the English Channel to the south. England is the largest country of the UK both by land area and population. It is known for its rich history, cultural heritage, and influential contributions to literature, science, and politics.",
    "what is the capital of England": "The capital of England is London.",
    "what is the largest city in England": "The largest city in England is also London.",
    "what is the population of England": "As of the latest data, the population of England is over 56 million people.",
    "what is the currency of England": "The currency of England is the British Pound Sterling (GBP).",
    "what is the official language of England": "The official language of England is English.",
    "welcome greetings":"hello guests , nice to have you",
}

# NLTK resources for tokenization and stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Function to preprocess text
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in string.punctuation and token not in stop_words]
    return tokens

# Function to find best answer based on token overlap
def find_best_answer(user_question):
    user_tokens = preprocess_text(user_question)
    max_overlap = 0
    best_answer = "Sorry, I couldn't find a good answer. Please try asking in a different way."

    for question, answer in knowledge_base.items():
        question_tokens = preprocess_text(question)
        overlap = len(set(user_tokens) & set(question_tokens))

        if overlap >= 1:  # Adjust overlap threshold as needed
            return answer

    # If no answer found in knowledge base, try external APIs
    external_answer = get_external_answer(user_question)
    if external_answer:
        return external_answer

    return best_answer

# Function to get answer from Wikipedia API
def get_wikipedia_answer(query):
    try:
        wikipedia.set_lang("en")  # Set Wikipedia language
        summary = wikipedia.summary(query, sentences=1)  # Get summary of the article
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found for '{query}'. Please be more specific."
    except wikipedia.exceptions.PageError as e:
        return f"No Wikipedia page found for '{query}'."

# Function to get answer from Stack Overflow API
def get_stackoverflow_answer(query):
    url = "https://api.stackexchange.com/2.3/search"
    params = {
        "order": "desc",
        "sort": "relevance",
        "intitle": query,
        "site": "stackoverflow"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data['items']:
            answer = data['items'][0]['title'] + ": " + data['items'][0]['link']
            return answer
        else:
            return f"No relevant Stack Overflow posts found for '{query}'."
    except requests.exceptions.RequestException as e:
        return f"Error occurred: {str(e)}"

# Function to fetch external answer from Wikipedia or Stack Overflow
def get_external_answer(user_question):
    external_answer = None
    # First try Wikipedia
    external_answer = get_wikipedia_answer(user_question)
    if not external_answer:
        # If no answer from Wikipedia, try Stack Overflow
        external_answer = get_stackoverflow_answer(user_question)
    return external_answer

# Function to save conversation history
def save_conversation(user_question, bot_answer):
    history_file = 'conversation_history.txt'
    with open(history_file, 'a', encoding='utf-8') as file:
        file.write(f"User: {user_question}\n")
        file.write(f"Bot: {bot_answer}\n\n")

# Function to fetch a random joke from an API
def fetch_random_joke():
    joke_api_url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(joke_api_url)
        if response.status_code == 200:
            data = response.json()
            return f"{data['setup']} {data['punchline']}"
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

# Function to fetch a random meme template from an API
def fetch_random_meme_template():
    meme_api_url = "https://api.imgflip.com/get_memes"
    try:
        response = requests.get(meme_api_url)
        if response.status_code == 200:
            data = response.json()
            random_meme = random.choice(data['data']['memes'])  # Select a random meme template
            return random_meme['url']
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

# Streamlit UI customization
st.title("Simple FAQ Chatbot")
st.markdown("Welcome to the Simple FAQ Chatbot. Ask me anything!")

# Text input for user question
user_question = st.text_input("You:")

# Process question and get answer
if user_question:
    best_answer = find_best_answer(user_question)
    st.write(f"**Answer:** {best_answer}")

    # Save conversation history
    save_conversation(user_question, best_answer)

# Display conversation history in sidebar
st.sidebar.title("Conversation History")
history_file = 'conversation_history.txt'

if os.path.exists(history_file):
    with open(history_file, 'r', encoding='utf-8') as file:
        conversation_history = file.read()
        st.sidebar.text_area("Previous Conversations:", value=conversation_history, height=400)
else:
    st.sidebar.text("No conversation history yet.")

# Button to fetch a random joke
if st.button("Tell me a Joke"):
    st.markdown("### Random Joke")
    random_joke = fetch_random_joke()
    if random_joke:
        st.write(random_joke)
    else:
        st.error("Failed to fetch a random joke. Please try again later.")

# Button to generate a random meme
if st.button("Generate a Random Meme"):
    st.markdown("### Random Meme")
    meme_url = fetch_random_meme_template()
    if meme_url:
        st.image(meme_url, use_column_width=True)
    else:
        st.error("Failed to fetch a random meme template. Please try again later.")

# Button to try translation model (example link)
if st.button("Try Translation Model"):
    st.markdown("### Translation Model")
    st.markdown("Explore translation capabilities using [https://lan-trans.streamlit.app/]")

# Footer
st.markdown("---")
st.markdown("By [Rauf](https://personal-web-page-lemon.vercel.app/index.html)")
