FROM python:3.9-slim

ENV OPNSENSE_APISECRET ""
ENV OPNSENSE_APIKEY ""
ENV HOST "https://opnsense.lan"
ENV CLOUDFLARE_ZONEID ""
ENV CLOUDFLARE_APIKEY ""
ENV DNS_RECORD ""

# Set the working directory
WORKDIR /app

# Copy the script into the container
COPY main.py /app/

# Install dependencies
RUN pip install requests

CMD ["sh", "-c", "python main.py --api-key ${OPNSENSE_APIKEY} --api-secret ${OPNSENSE_APISECRET} --opnsense-ip ${HOST} --zone-id ${CLOUDFLARE_ZONEID} --record-name ${DNS_RECORD} --api-token ${CLOUDFLARE_APIKEY}"]
