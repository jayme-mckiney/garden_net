FROM python:3.8-slim as build
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
	build-essential gcc 

WORKDIR /usr/app
RUN python -m venv /usr/venv
ENV PATH="/usr/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.8-slim
RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python
RUN mkdir /usr/control_center && chown python:python /usr/control_center && \
	mkdir /usr/venv && chown python:python /usr/venv &&  \
	mkdir /usr/logs && chown python:python /usr/logs
WORKDIR /usr/control_center
USER 999
COPY --from=build /usr/venv /usr/venv
COPY . .
ENV PATH="/usr/venv/bin:$PATH"
CMD ["python", "wsgi.py"]