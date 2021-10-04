import spark_util

cluster_name = spark_util.get_cluster_name()
spark_util.stop_spark_cluster(cluster_name)
