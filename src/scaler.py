#!/usr/bin/env python

import kubernetes
import logging

def set_logging_level(level=20):
    logger.setlevel(level)

def kubernetes_setup():
    logger.info

def check_for_unscheduled_pods():
    logger.info("Checking for unscheduled pods")

def terraform_scale_up(new_nodes=1):
    logger.info("Scaling up " + str(new_nodes) + " additional nodes")

def terraform_scale_down(down_nodes=1):
    logger.info("Scaling down " + str(down_nodes) + " nodes")

def scaler(interval=30):
    logger.info("Initiating Scaling")