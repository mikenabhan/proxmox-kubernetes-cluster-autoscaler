 #!/usr/bin/env python3

from kubernetes import client, config
import logging
import os

unschedulable_pods = {}

def set_logging_level():
    logging.basicConfig(level=logging.INFO)
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
    # print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    # print(ret.items[0].metadata.name)
    # print(ret.items[0].status.conditions)
    for i in ret.items:
        # print(i.metadata.name)
        if i.metadata.name == "unschedulable-pod":
            # print(i)
            # print(i.status)
            for status in i.status.conditions:
                if status.type == "PodScheduled" and status.status == "False" and status.reason == "Unschedulable":
                    if "Insufficient cpu" in status.message or "Insufficient memory" in status.message:
                        # print(status.message)
                        unschedulable_pods[i.metadata.name]=i.metadata.namespace
    logging.info(str(len(unschedulable_pods)) + " pods are unschedulable")                    
    return len(unschedulable_pods)
    # for i in ret.items:
    #     print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def terraform_scale_up(new_nodes=1):
    logging.info("Scaling up " + str(new_nodes) + " additional nodes")

def terraform_scale_down(down_nodes=1):
    logging.info("Scaling down " + str(down_nodes) + " nodes")

def scaler(interval=30):
    logging.info("Initiating Scaling")


set_logging_level()
kubernetes_setup()
check_for_unscheduled_pods()
print(unschedulable_pods)