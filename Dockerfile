FROM python:3.7-slim

#eksik paket kuralım
RUN apt-get update 
RUN apt-get install -y git
RUN \
apt-get install -y g++ && \
###apt-get install -y libstdc++ && \
apt-get install -y python3-dev

#lokalde hazırladıklarımızı taşıyoruz
#COPY .gitconfig /root/.gitconfig 
#COPY .git-credentials /root/.git-credentials

#uygulama calıstırıacagımız konumu belirleyelim
WORKDIR /app

# uygulamamızı clone eyleyelim...
RUN \
cd /app && \
git clone https://github.com/ati-ince/TV-Production-Control-Auto.git 
RUN cd TV-Production-Control-Auto 
RUN python -m pip install -r TV-Production-Control-Auto/requirements.txt

# Bu aşamadan sonra buld kısmı tamamlanmış launch kısmına ulaştık.... 
ENTRYPOINT [ "/bin/sh" ]
CMD [ "TV-Production-Control-Auto/update_ci.sh" ]
