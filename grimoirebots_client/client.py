import uuid
import os
from apiclient import (
    APIClient,
    endpoint,
    retry_request,
)


@endpoint(base_url=os.getenv("GRIMOIREBOTS_ENDPOINT"))
class Endpoint:
    """
    Endpoints of the Grimoirebots API
    """

    orders = "orders/"
    pending_orders = "orders/pending/"
    order = "orders/{id}"
    order_setup = "orders/{id}/setup.cfg"
    order_projects = "orders/{id}/projects.json"
    reports = "reports/"
    report = "reports/{id}"


class GrimoirebotsClient(APIClient):
    """
    Client for the Grimoirebots API
    """

    def get_all_pending_orders(self) -> dict:
        return self.get(Endpoint.pending_orders)

    @retry_request
    def get_order(self, order_id: uuid.uuid4) -> dict:
        url = Endpoint.order.format(id=order_id)
        return self.get(url)

    @retry_request
    def get_order_projects(self, order_id: uuid.uuid4) -> dict:
        url = Endpoint.order_projects.format(id=order_id)
        return self.get(url)

    @retry_request
    def get_order_setup(self, order_id: uuid.uuid4) -> dict:
        url = Endpoint.order_setup.format(id=order_id)
        return self.get(url)

    def get_all_reports(self) -> dict:
        return self.get(Endpoint.reports)

    @retry_request
    def get_report(self, report_id: uuid.uuid4) -> dict:
        url = Endpoint.report.format(id=report_id)
        return self.get(url)

    @retry_request
    def add_report(self, report_info):
        return self.post(Endpoint.reports, data=report_info)
