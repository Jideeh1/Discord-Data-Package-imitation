import requests
from collections import Counter
import re
import emoji

# Note: You have to have a discord bot inside the server to fetch their
# mesasges. Otherwise, it won't read anything.
# Please take a look at Line 74 to customize filtered out words.

# Insert your bot token here
BOT_TOKEN = ''

# Channel ID where messages will be fetched from
CHANNEL_ID = ''

# Target user ID to filter messages
USER_ID = ''

# Discord API URL
url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
#url = f"https://discord.com/channels/{CHANNEL_ID}/{CHANNEL_ID}"

# Headers with Authorization
headers = {
    'Authorization': f'Bot {BOT_TOKEN}',
    'Content-Type': 'application/json'
}

# Parameters for the API request
params = {
    'limit': 100  # Number of messages to fetch (max 100 per request)
}

# Pagination setup
last_message_id = None
all_user_messages = []
total_messages = 0  # Initialize total message count

# Fetch messages in a loop to handle pagination
while True:
    if last_message_id:
        params['before'] = last_message_id  # Fetch messages before the last message ID
    
    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Failed to fetch messages: {response.status_code}")
        break
    
    messages = response.json()
    if not messages:
        break  # No more messages available
    
    total_messages += len(messages)  # Add to the total message count
    
    # Filter and collect messages from the user
    user_messages = [msg['content'] for msg in messages if msg['author']['id'] == USER_ID]
    all_user_messages.extend(user_messages)
    
    # Update the last message ID for pagination
    last_message_id = messages[-1]['id']

# Analyze favorite words, cursed words, and emojis
def extract_emojis(text):
    return [char for char in text if char in emoji.EMOJI_DATA]

def clean_text(text):
    return re.findall(r'\b\w+\b', text.lower())


# This can honestly be better
# Load a list of common stop words
stop_words = {
    "the", "and", "is", "in", "to", "a", "of", "for", "on", "with", "at", "by", 
    "it", "this", "that", "an", "as", "from", "or", "but", "are", "was", "be", 
    "not", "we", "they", "you", "i", "he", "she", "his", "her", "their", "our", 
    "has", "have", "had", "can", "do", "will", "would", "should", "could", "my",
    "what", "https", "1020182328275906600", "s", "icant", "me", "kekw", "929662755508740136",
    "com", "view", "tenor", "gif", "t", "so", "wuthering", "one", "even", "eat", "wuwa",
    "waves", "if", "fish", "gundam", "pork", "taste", "si", "mo", "chicken", "bones",
    "meat", "youtu", "sa", "when", "m", "spicy", "food", "cleo", "beef", "seed", "5",
    "days", "d", "just", "anime", "ramen", "get", "takes", "something", "ba", "your", "than",
    "eating", "momo", "now", "yao", "paul", "don", "na", "then", "ate", "crying", "frozen",
    "u", "about", "half", "some"
}

# Load a list of common curse words
curse_words = {"damn", "hell", "shit", "fuck", "fucking", "bitch", "ass", "crap"}

# Word and emoji analysis
all_words = []
all_emojis = []
all_curse_words = []

for message in all_user_messages:
    all_words.extend(clean_text(message))
    all_emojis.extend(extract_emojis(message))
    all_curse_words.extend([word for word in clean_text(message) if word in curse_words])

# Filter out stop words
filtered_words = [word for word in all_words if word not in stop_words]

# Count occurrences
word_counts = Counter(filtered_words)
emoji_counts = Counter(all_emojis)
curse_word_counts = Counter(all_curse_words)

# Get the top 5 results
top_words = word_counts.most_common(20)
top_curse_words = curse_word_counts.most_common(10)
top_emojis = emoji_counts.most_common(10)

# Display results
print(f"\nTotal messages in channel: {total_messages}")

print("\n--- User's Favorite Words ---")
for word, count in top_words:
    print(f"{word}: {count} times")

print("\n--- User's Favorite Cursed Words ---")
if top_curse_words:
    for word, count in top_curse_words:
        print(f"{word}: {count} times")
else:
    print("No cursed words found.")

print("\n--- User's Top Emojis ---")
if top_emojis:
    for em, count in top_emojis:
        print(f"{em}: {count} times")
else:
    print("No emojis found.")

while True:
    user_input = input("Press Enter to exit...")  # Wait for the user to press Enter
    if user_input == "":
        break  # Exit the loop when Enter is pressed
