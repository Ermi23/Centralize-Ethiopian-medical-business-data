import os
import csv
import logging
import yaml
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import MessageMediaPhoto
import warnings

# Filter out the specific "very new message with ID" warnings
warnings.filterwarnings("ignore", message="Server sent a very new message with ID")

# Ensure logs directory exists
os.makedirs(r'c:\Users\ermias.tadesse\10x\Centralize-Ethiopian-medical-business-data\logs', exist_ok=True)
os.chdir(r'c:\Users\ermias.tadesse\10x\Centralize-Ethiopian-medical-business-data\logs')

# Set up logging
logging.basicConfig(filename='telegram_scraper.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Load configuration
os.chdir(r'c:\Users\ermias.tadesse\10x\Centralize-Ethiopian-medical-business-data\src\scraping')
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

api_id = config['telegram']['api_id']
api_hash = config['telegram']['api_hash']
phone = config['telegram']['phone']

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def scrape_channel(channel, collect_images=False):
    """
    Scrapes messages from a specified Telegram channel.

    Args:
        channel (str): The Telegram channel URL.
        collect_images (bool): Whether to download images from the messages.

    Returns:
        None
    """
    try:
        await client.start(phone)
        logging.info(f'Successfully connected to Telegram for channel: {channel}')
        
        # Get messages from the channel
        messages = await client.get_messages(channel, limit=100)  # Adjust limit as needed
        
        # Ensure data directories exist
        os.makedirs(r'c:\Users\ermias.tadesse\10x\Centralize-Ethiopian-medical-business-data\Data\scraping\data\raw', exist_ok=True)
        if collect_images:
            os.makedirs(r'c:\Users\ermias.tadesse\10x\Centralize-Ethiopian-medical-business-data\Data\scraping\data\raw\media', exist_ok=True)
        
        csv_filename = f'c:\\Users\\ermias.tadesse\\10x\\Centralize-Ethiopian-medical-business-data\\Data\\scraping\\data\\raw\\{channel.replace("https://t.me/", "")}.csv'
        with open(csv_filename, mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            if collect_images:
                writer.writerow(['message_id', 'date', 'sender_id', 'message', 'media_path'])
            else:
                writer.writerow(['message_id', 'date', 'sender_id', 'message'])
            
            for message in messages:
                media_path = None
                if collect_images and message.media and isinstance(message.media, MessageMediaPhoto):
                    media_path = f'c:\\Users\\ermias.tadesse\\10x\\Centralize-Ethiopian-medical-business-data\\Data\\scraping\\data\\raw\\media\\{message.id}.jpg'
                    await message.download_media(media_path)
                if collect_images:
                    writer.writerow([message.id, message.date, message.sender_id, message.message, media_path])
                else:
                    writer.writerow([message.id, message.date, message.sender_id, message.message])
                
        logging.info(f'Successfully scraped and saved data for channel: {channel}')
        
    except SessionPasswordNeededError:
        logging.error('Session password is needed. Please check your credentials and try again.')
    except Exception as e:
        logging.error(f'Error scraping channel {channel}: {str(e)}')

if __name__ == '__main__':
    channels = [
        'https://t.me/DoctorsET',
        'https://t.me/lobelia4cosmetics',
        'https://t.me/yetenaweg',
        'https://t.me/EAHCI',
        'https://et.tgstat.com/medicine'
    ]
    
    image_channels = [
        'https://t.me/Chemed',
        'https://t.me/lobelia4cosmetics'
    ]
    
    with client:
        # Scrape messages from all channels
        for channel in channels:
            client.loop.run_until_complete(scrape_channel(channel))
        
        # Scrape images from specific channels
        for channel in image_channels:
            client.loop.run_until_complete(scrape_channel(channel, collect_images=True))
