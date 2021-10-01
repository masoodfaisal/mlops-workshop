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
timeout_seconds = 360


# run predicate func every 3 seconds until it returns true
def wait(predicate, timeout):
    print("Waiting for spark cluster to be ready...")
    mustend = time.time() + timeout
    while time.time() < mustend:
        if predicate:
            print("Cluster is ready")
            return True
        time.sleep(3)
    
    print(f"Cluster was not ready after a given timeout {timeout}s")
    return False


# Connect to Openshift
with oc.api_server(server):
    with oc.token(token):
        with oc.project(project), oc.timeout(10*60):
            print('OpenShift client version: {}'.format(oc.get_client_version()))

            print(f"Searching for SparkCluster with name {cluster_prefix}-{cluster_name}...")
            cluster_count = oc.selector(f"{spark_crd_name}/{cluster_prefix}-{cluster_name}").count_existing()
            print(f"SparkCluster found: {cluster_count}")

            # Only create Spark cluster if it doesn't exist
            if cluster_count == 0:

                template_data = {"clustername": f"{cluster_prefix}-{cluster_name}"}
                applied_template = Template(open("spark-cluster.yaml").read())

                print(f"Creating SparkCluster {cluster_prefix}-{cluster_name} ...")
                # print(applied_template.render(template_data))
                oc.create(applied_template.render(template_data))

                ready_pred = oc.selector(f"{spark_crd_name}/{cluster_prefix}-{cluster_name}")\
                    .object().model.status.conditions.can_match({'status': "ready"})

                # wait for cluster to be ready
                ready = wait(ready_pred, timeout_seconds)

                if not ready:
                    sys.exit(1)

                print(f"SparkCluster {cluster_prefix}-{cluster_name} created")
                # task_instance = context['task_instance']
                # Pulls the return_value XCOM from "pushing_task"
                # task_instance.xcom_push(key="spark_cluster", value="ross")
            else:
                print(f"Spark Cluster already exists {cluster_prefix}-{cluster_name}")

            with open('spark-info.txt', 'w') as file:
                    file.write(f"{cluster_prefix}-{cluster_name}")