FROM ubuntu:16.04

MAINTAINER Juan Soler-Company <juan.soler@upf.edu>

RUN apt-get update && apt-get install -y \
    python-pip \
    apache2 \
    php \ 
    libapache2-mod-php \
    php-mcrypt \
    curl \
    vim
    
RUN pip install -U nltk
RUN pip install numpy scipy
RUN pip install flask lxml

RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN pip install flask-jsonpify

WORKDIR /var/www/html/
ADD forumEnricher.tar.gz .

WORKDIR /home/
RUN mkdir code
ADD code.tar.gz ./code/
WORKDIR ./code/

CMD sh launch.sh
