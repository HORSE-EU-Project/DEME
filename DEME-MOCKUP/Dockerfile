# Use an official Python runtime as a parent image
FROM python:3.10

# Set the correct versions of used libraries
ARG PANDAS_VERSION=2.2.2
ARG NUMPY_VERSION=1.23.5

# Set the working directory in the container
ARG APP_DIR="/opt/app"
WORKDIR ${APP_DIR}

# Install any necessary package
RUN pip install fastapi[all] uvicorn "pandas==${PANDAS_VERSION}" requests "numpy==${NUMPY_VERSION}"

# Copy the application
COPY *.py /opt/app/

ENV PATH="/opt/app:${PATH}"

ENTRYPOINT [ "python" ]

RUN echo "Starting DEME mockup"

# Start DEME-mockup
CMD [ "/opt/app/deme_mockup.py" ]