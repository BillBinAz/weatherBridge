import datetime as dt
import logging

from onepasswordconnectsdk.client import (
    new_client_from_environment
)
AUTOMATION_VAULT_ID = "q37tw26x3pi47zs5fzavl4o2vu"


def get_credentials(item_id):

    try:
        # creating client using OP_CONNECT_TOKEN and OP_CONNECT_HOST environment variables
        connect_client = new_client_from_environment()
        item = connect_client.get_item(item_id, AUTOMATION_VAULT_ID)
        return item.fields
    except Exception as e:
        logging.error("Unable to get credentials " + str(e))
        print(dt.datetime.now().time(), "Unable to get credentials " + str(e))
    return
