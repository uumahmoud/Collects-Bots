FROM uumahmoud/Collects-Bots:slim-buster

#clonning repo 
RUN git clone https://github.com/uumahmoud/Collects-Bots /root/Collects-Bots
#working directory 
WORKDIR /root/jepthon
RUN apk add --update --no-cache p7zip
# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/jepthon/bin:$PATH"

CMD ["python3","-m","jepthon"]
