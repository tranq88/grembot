from dotenv import load_dotenv
import os


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

BOT_TEST_SERVER = int(os.getenv('BOT_TEST_SERVER'))
BTS_TEMP_CHANNEL = int(os.getenv('BTS_TEMP_CHANNEL'))

GREMLIN_ID = int(os.getenv('GREMLIN_ID'))
GREMLIN_TEMP_CHANNEL = int(os.getenv('GREMLIN_TEMP_CHANNEL'))
