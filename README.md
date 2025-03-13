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
python script.py \
  --opnsense-ip <OPNSENSE_IP> \
  --api-key <API_KEY> \
  --api-secret <API_SECRET> \
  --zone-id <ZONE_ID> \
  --record-name <RECORD_NAME> \
  --api-token <API_TOKEN>
```
