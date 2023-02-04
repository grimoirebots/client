from apiclient import (
    NoAuthentication,
    JsonResponseHandler,
    JsonRequestFormatter,
)
from apiclient.exceptions import APIClientError

# Initialize the client with the correct authentication method,
# response handler and request formatter.
from .client import GrimoirebotsClient

client = GrimoirebotsClient(
    authentication_method = NoAuthentication(),
    response_handler = JsonResponseHandler,
    request_formatter = JsonRequestFormatter,
)

pending_orders = client.get_all_pending_orders()

for order in pending_orders:
    order_id = order['id']
    order_data_source_url = order['data_source_url']

    report_info = {
        "order": order_id,
        "report": f'The order {order_id} is requesting to analyze {order_data_source_url}'
    }

    client.add_report(report_info)
