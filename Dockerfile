FROM mysterysd/wzmlx:heroku

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt -qq update && \
    apt-get install fontconfig -y -f
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*


COPY . .

RUN pip3 install -r requirements.txt

CMD ["bash", "run.sh"]
