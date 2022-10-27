#!/usr/bin/env python3

from kubernetes import client, config, watch
import logging
import os
import time
import subprocess

unschedulable_pods = {}
scaleup_wait_stabilization_minutes = 5
scaledown_wait_stabilization_minutes = 10

def set_logging_level():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("Setting Log Level to INFO")
    

def kubernetes_setup():
    logging.info("Validating Kubeconfig")
    # config.load_kube_config(
    # # os.path.join(os.environ["KUBECONFIG"], '.kube/config'))
    # os.path.join(os.environ["HOME"], '.kube/config'))
    config.load_kube_config()

def check_for_unscheduled_pods():
    logging.info("Checking for unscheduled pods")
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        if i.metadata.name == "unschedulable-pod":

            for status in i.status.conditions:
                if status.type == "PodScheduled" and status.status == "False" and status.reason == "Unschedulable":
                    if "Insufficient cpu" in status.message or "Insufficient memory" in status.message:
                        unschedulable_pods[i.metadata.name]=i.metadata.namespace
    logging.info(f"{len(unschedulable_pods)} pods are unschedulable due to memory or CPU")                      
    return len(unschedulable_pods)


def terraform_scale_up(new_nodes=1):
    logging.info(f"Scaling up {str(new_nodes)} additional nodes")
    start_ready_nodes = get_ready_nodes()
    start_pending_nodes = get_pending_nodes()
    try:
        print(f"Applying terraform")
    except:
        print(f"Terraform Failed to Apply")    

    new_pending_nodes = get_pending_nodes()
    loops = 0 #delete these test cases
    while new_pending_nodes <= start_pending_nodes:
        
        new_pending_nodes = get_pending_nodes()
        logging.info("Waiting 10s for new node to to contact k8s api")
        time.sleep(10)
        if loops < 1: #delete these test cases
            loops += 1 #delete these test cases
        else: #delete these test cases
            new_pending_nodes += 1 #delete these test cases
    if new_pending_nodes > start_pending_nodes:
        while get_ready_nodes() < start_ready_nodes + new_nodes:
            logging.info("Waiting 10s for new node to be ready")
            time.sleep(10)




def terraform_scale_down(down_nodes=1):
    logging.info(f"Scaling down {str(down_nodes)} nodes")

def scaler(interval=30):
    logging.info("Initiating Scaling")
    while True:
        pod_num = check_for_unscheduled_pods()
        if pod_num > 0:
            terraform_scale_up()
        time.sleep(5)
        
def get_pending_nodes():
    pending_nodes = 0
    logging.info("Getting pending nodes")
    v1 = client.CoreV1Api()
    nodes = v1.list_node(watch=False)
    for node in nodes.items:
        # print(node.metadata.name)
        for status in node.status.conditions:
            if status.type == "Ready" and status.status == "False":
                logging.info(f"{node.metadata.name} is pending")
                pending_nodes = pending_nodes + 1
    logging.info(f"{str(pending_nodes)} nodes are pending")
    return pending_nodes

def get_ready_nodes():
    ready_nodes = 0
    logging.info("Getting ready nodes")
    v1 = client.CoreV1Api()
    nodes = v1.list_node(watch=False)
    for node in nodes.items:
        # print(node.metadata.name)
        for status in node.status.conditions:
            if status.type == "Ready" and status.status == "True":
                logging.info(f"{node.metadata.name} is ready")
                ready_nodes = ready_nodes + 1
    logging.info(f"{str(ready_nodes)} nodes are ready")
    return ready_nodes
    # print(nodes.items)

set_logging_level()
kubernetes_setup()
# check_for_unscheduled_pods()
# print(unschedulable_pods)

scaler()

# print(get_pending_nodes())
# print(get_ready_nodes())
