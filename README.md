# Cloudflare DNS Sync with OPNSense

Sync Cloudflare DNS records using the public API provided by the OPNSense API.

This codebase and documentation was mostly written by AI!

| Argument      | Description                                             |
| ------------- | ------------------------------------------------------- |
| --opnsense-ip | OPNsense router IP                                      |
| --api-key     | OPNsense API key                                        |
| --api-secret  | OPNsense API secret                                     |
| --zone-id     | Cloudflare Zone ID                                      |
| --record-name | Cloudflare DNS record names (not including domain name) |
| --api-token   | Cloudflare API token                                    |

```bash
python main.py \
  --opnsense-ip <OPNSENSE_IP> \
  --api-key <API_KEY> \
  --api-secret <API_SECRET> \
  --zone-id <ZONE_ID> \
  --record-name <RECORD_NAME1> [<RECORD_NAME2> ...] \
  --api-token <API_TOKEN>
```

## Build Docker Image

To build the Docker image for this script, run the following command:

```bash
docker build -t cloudflare-sync .
```

## Example Kubernetes CronJob

To schedule the script to run every hour using a Kubernetes CronJob, you can create a YAML file like this:

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: cloudflare-sync-cronjob
spec:
  schedule: "0 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: cloudflare-sync
              image: cloudflare-sync
              imagePullPolicy: Always
              env:
                - name: HOST
                  value: "your_opnsense_ip"
                - name: OPNSENSE_API_KEY
                  valueFrom:
                    secretKeyRef:
                      name: cloudflare-sync-secrets
                      key: opnsense-api-key
                - name: OPNSENSE_API_SECRET
                  valueFrom:
                    secretKeyRef:
                      name: cloudflare-sync-secrets
                      key: opnsense-api-secret
                - name: CLOUDFLARE_ZONE_ID
                  valueFrom:
                    secretKeyRef:
                      name: cloudflare-sync-secrets
                      key: cloudflare-zone-id
                - name: DNS_RECORD
                  value: "your_dns_record"
                - name: CLOUDFLARE_API_TOKEN
                  valueFrom:
                    secretKeyRef:
                      name: cloudflare-sync-secrets
                      key: cloudflare-api-token
```

Make sure to create a Kubernetes Secret and ConfigMap for the secrets and script respectively:

```bash
kubectl create secret generic cloudflare-sync-secrets \
  --from-literal=opnsense-api-key="your_opnsense_api_key" \
  --from-literal=opnsense-api-secret="your_opnsense_api_secret" \
  --from-literal=cloudflare-zone-id="your_cloudflare_zone_id" \
  --from-literal=cloudflare-api-token="your_cloudflare_api_token"
```
