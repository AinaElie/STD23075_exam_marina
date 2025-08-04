FROM debian:bookworm-slim

RUN apt-get update 
RUN apt-get install -y python3
RUN apt-get install -y python3-pip python3-venv
RUN apt-get install -y ocaml opam

RUN opam init -y --disable-sandboxing && \
    opam install -y ocamlfind ounit2 && \
    opam clean

WORKDIR /app

COPY server /app

COPY src /src

RUN eval $(opam env) && cd /src && make

RUN cd /app 
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"  
RUN pip install flask

EXPOSE 5000

CMD ["python3", "server.py"]
