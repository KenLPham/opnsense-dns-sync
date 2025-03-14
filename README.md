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
                - name: OPNSENSE_IP
                  value: "your_opnsense_ip"
                - name: API_KEY
                  valueFrom:
                    secretKeyRef:
                      name: cloudflare-sync-secrets
                      key: api-key
                - name: API_SECRET
                  valueFrom:
                    secretKeyRef:
                      name: cloudflare-sync-secrets
                      key: api-secret
                - name: ZONE_ID
                  value: "your_zone_id"
                - name: RECORD_NAME
                  value: "your_record_name"
                - name: API_TOKEN
                  value: "your_api_token"
                  valueFrom:
                    secretKeyRef:
                      name: cloudflare-sync-secrets
                      key: api-token
          restartPolicy: OnFailure
          volumes:
            - name: script-volume
              configMap:
                name: cloudflare-sync-script
```

Make sure to create a Kubernetes Secret and ConfigMap for the secrets and script respectively:

```bash
kubectl create secret generic cloudflare-sync-secrets \
  --from-literal=api-key="your_api_key" \
  --from-literal=api-secret="your_api_secret" \
  --from-literal=api-token="your_api_token"
```
