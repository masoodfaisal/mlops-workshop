import openshift as oc
import os
from jinja2 import Template


#/var/run/secrets/kubernetes.io/serviceaccount
with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as namespace:
    project = namespace.read()
print(f"Project name: {project}")

cluster_name = os.environ["SPARK_CLUSTER"]

#build from source Docker file
with oc.api_server(server):
    with oc.token(token):
        with oc.project(project), oc.timeout(10*60):
            print('OpenShift client version: {}'
                  .format(oc.get_client_version()))
            
            with open('spark-info.txt', 'r') as file:
                cluster_name = file.read()
                
            cluster_count = oc.selector(f"SparkCluster/{cluster_name}").count_existing()
            print(cluster_count)
            if cluster_count > 0:
                oc.oc_action(oc.cur_context(), "delete", cmd_args=["SparkCluster", cluster_name])
            else:
                print(f"Spark Cluster does not exists {cluster_name}")
