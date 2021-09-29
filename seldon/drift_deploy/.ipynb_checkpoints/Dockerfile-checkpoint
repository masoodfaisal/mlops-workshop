#FROM python:3.7-slim
#RUN mkdir /microservice
#WORKDIR /microservice
#COPY requirements.txt /microservice/
#RUN pip install -r requirements.txt


# EXPOSE 5000
#
FROM registry.access.redhat.com/ubi8/python-38

WORKDIR /microservice
RUN pip install alibi_detect
RUN pip install seldon-core
RUN pip install joblib
RUN pip install scikit-learn
RUN pip install category_encoders
RUN pip install dill
USER root
RUN dnf install -y mesa-libGL
USER 1001
# ADD CustomerChurnDriftPredictor /microservice/CustomerChurnDriftPredictor
COPY CustomerChurnDriftPredictor.py model.pkl CustomerChurnDriftTransformer.py CustomerChurnDriftPredictor.sav /microservice/
RUN cp model.pkl CustomerChurnDriftPredictor.sav
ENV PERSISTENCE 0
CMD seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE --grpc-port ${GRPC_PORT} --metrics-port ${METRICS_PORT} --http-port ${HTTP_PORT}