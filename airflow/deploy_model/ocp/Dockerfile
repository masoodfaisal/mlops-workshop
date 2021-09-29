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
COPY Predictor.py model.pkl Transformer.py  /microservice/
ENV PERSISTENCE 0
CMD seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE --grpc-port ${GRPC_PORT} --metrics-port ${METRICS_PORT} --http-port ${HTTP_PORT}