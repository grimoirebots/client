import uuid
import os
from apiclient import (
    APIClient,
    endpoint,
    paginated,
    retry_request,
)


# Define endpoints, using the provided decorator.
@endpoint(base_url = os.getenv('GRIMOIREBOTS_ENDPOINT'))
class Endpoint:
    orders = "orders/"
    pending_orders = "orders/pending/"
    order = "orders/{id}"
    reports = "reports/"
    report = "reports/{id}"


# def get_next_page(response, previous_page_url):
#     return response["next"]


# Extend the client for your API integration.
class GrimoirebotsClient(APIClient):

    # @paginated(by_url=get_next_page)
    def get_all_pending_orders(self) -> dict:
        return self.get(Endpoint.pending_orders)

    # @paginated(by_url=get_next_page)
    def get_all_reports(self) -> dict:
        return self.get(Endpoint.reports)

    @retry_request
    def get_report(self, report_id: uuid.uuid4) -> dict:
        url = Endpoint.report.format(id = report_id)
        return self.get(url)

    @retry_request
    def add_report(self, report_info):
        return self.post(Endpoint.reports, data = report_info)
