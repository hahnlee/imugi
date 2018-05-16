FROM python:3.6

RUN apt-get update && apt-get install -y vim

CMD pip3 install -e .[dev] && sh ./install-hook.sh && /bin/bash
