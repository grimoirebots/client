from apiclient import (
    NoAuthentication,
    JsonResponseHandler,
    JsonRequestFormatter,
)
from apiclient.exceptions import APIClientError

# Initialize the client with the correct authentication method,
# response handler and request formatter.
from grimoirebots_client.client import GrimoirebotsClient

import json
import configparser
import logging
import os
import sys
import docker

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

docker_client = docker.from_env()
volume = docker_client.volumes.get('grimoirebots-data')
volume_path = volume.attrs['Mountpoint']

GRIMOIREBOTS_ENDPOINT = os.getenv("GRIMOIREBOTS_ENDPOINT")

def main():

    parser = configparser.ConfigParser()

    client = GrimoirebotsClient(
        authentication_method = NoAuthentication(),
        response_handler = JsonResponseHandler,
        request_formatter = JsonRequestFormatter,
    )

    logger.info(f'Retrieving pending orders from {GRIMOIREBOTS_ENDPOINT}')
    pending_orders = client.get_all_pending_orders()

    logger.info(f'Retrieved {len(pending_orders)} orders')
    for order in pending_orders:
        order_id = order['id']

        logger.info(f'Processing order {order_id}')

        logger.info(f'Retrieving projects.json for order {order_id}')
        projects = client.get_order_projects(order_id=order['id'])
        projects_file_path = f'reports/{order_id}/projects.json'
        os.makedirs(os.path.dirname(projects_file_path), exist_ok=True)
        with open(projects_file_path, 'w') as projects_file:
            json.dump(projects, projects_file)
        logger.info(f'File projects.json for order {order_id} saved at {projects_file_path}')

        logger.info(f'Retrieving setup.cfg for order {order_id}')
        setup = client.get_order_setup(order_id=order['id'])
        parser.clear()
        parser.read_dict(setup)
        setup_file_path = f'reports/{order_id}/setup.cfg'
        os.makedirs(os.path.dirname(setup_file_path), exist_ok=True)
        with open(setup_file_path, 'w') as setup_file:
            parser.write(setup_file)
        logger.info(f'File setup.cfg for order {order_id} saved at {setup_file_path}')

        logger.info("Starting GrimoireLab container")
        docker_client.containers.run("grimoirelab/grimoirelab:0.10.0",
                                     name=f'grimoirelab-{order_id}',
                                     volumes=[f'{volume_path}/{order_id}:/home/grimoire/conf'],
                                     auto_remove=True, network_mode='host', detach=True)
        logger.info(f'Analysis for {order_id} has finished')

        report_info = {
            "order": order_id,
            "report": f'The order {order_id} has started'
        }

        logger.info(f'Creating report for order {order_id}')
        report = client.add_report(report_info)
        report_id = report['id']
        logger.info(f'Report {report_id} created for order {order_id}')

if __name__ == '__main__':
    main()
