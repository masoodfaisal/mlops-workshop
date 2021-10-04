import openshift as oc
import os
import sys
import time
from jinja2 import Template

print("Start OCP things...")

# Get the Openshift API URL
server = "https://" + os.environ["KUBERNETES_SERVICE_HOST"] + ":" + os.environ["KUBERNETES_SERVICE_PORT"] 

print(server)

print("Retrieving Openshift token information...")
# Get the Openshift auth token
with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as file:
    token = file.read()
# print(f"Openshift Token{token}")

print("Retrieving Openshift project information...")
# Get the current Openshift project name
with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as namespace:
    project = namespace.read()
print(f"Project name: {project}")

spark_crd_name = "SparkCluster"
cluster_prefix = "spark-cluster"
cluster_name = os.environ["SPARK_CLUSTER"]
worker_nodes = os.environ["WORKER_NODES"]

if os.getenv("worker_nodes") is None:
    worker_nodes = "2"

timeout_seconds = 300


# evaluate predicate func every 5 seconds until it returns true
def wait(predicate, timeout):
    mustend = time.time() + timeout
    time.sleep(5)
    while time.time() < mustend:
        try:
            if predicate(1) : return True
        except Exception as ex:
            print(ex)
        time.sleep(5)
    return False

# Connect to Openshift
with oc.api_server(server):
    with oc.token(token):
        with oc.project(project), oc.timeout(10*60):
            print('OpenShift client version: {}'.format(oc.get_client_version()))

            print(f"Searching for SparkCluster with name {cluster_prefix}-{cluster_name}...")
            cluster_count = oc.selector(f"{spark_crd_name}/{cluster_prefix}-{cluster_name}").count_existing()
            print(f"SparkCluster found: {cluster_count}")

            with open('spark-info.txt', 'w') as file:
                file.write(f"{cluster_prefix}-{cluster_name}\n")
                file.write(f"{worker_nodes}")

            # Only create Spark cluster if it doesn't exist
            if cluster_count > 0:
                print(f"Spark Cluster already exists {cluster_prefix}-{cluster_name}")
                sys.exit(0)

            template_data = {"clustername": f"{cluster_prefix}-{cluster_name}", "workernodes": f"{worker_nodes}"}
            applied_template = Template(open("spark-cluster.yaml").read())

            print(f"Creating SparkCluster {cluster_prefix}-{cluster_name} ...")
            # print(applied_template.render(template_data))
            oc.create(applied_template.render(template_data))

            # predicate function to check if the master node and all worker nodes are ready
            cluster_ready = lambda _: \
            oc.selector(f"replicationcontroller/{cluster_prefix}-{cluster_name}-m")\
            .object().model.status.can_match({ 'readyReplicas': 1 }) &\
            oc.selector(f"replicationcontroller/{cluster_prefix}-{cluster_name}-w")\
            .object().model.status.can_match({ 'readyReplicas': int(worker_nodes) })

            # wait for cluster to be ready
            print("Waiting for spark cluster to be ready...")
            ready = wait(cluster_ready, timeout_seconds)

            if not ready:
                print(f"Cluster was not ready after a given timeout {timeout}s")
                sys.exit(1)

            print(f"SparkCluster {cluster_prefix}-{cluster_name} is ready.")

