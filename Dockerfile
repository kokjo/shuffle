FROM debian:bullseye

ARG USER=user
ARG PORT=1337
ENV PORT ${PORT}

EXPOSE $PORT

RUN apt-get update -qy && apt-get install -qy python3.9 python3-seccomp socat
RUN useradd -m user

WORKDIR /home/$USER/
ADD challenge.py challenge.py
ADD flag.txt flag.txt

CMD socat tcp-listen:${PORT},reuseaddr,fork exec:"./challenge.py",su=user

