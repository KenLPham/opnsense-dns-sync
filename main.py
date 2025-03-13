import argparse
import requests
import logging
import ipaddress
from requests.auth import HTTPBasicAuth

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def http_request(url, api_key, api_secret):
    """ Sends an authenticated request to the OPNsense API. """
    try:
        logger.debug(f"Requesting {url}")
        response = requests.get(url, auth=HTTPBasicAuth(api_key, api_secret), verify=False)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return None

def get_opnsense_public_ip(opnsense_ip, api_key, api_secret):
    """
    Fetches the public IP address of the WAN interface on an OPNsense router using the API.
    """
    url = f"{opnsense_ip}/api/interfaces/overview/interfacesInfo"
    response = http_request(url, api_key, api_secret)
    
    if response is None:
        logger.error("Failed to retrieve interface data.")
        return None

    logger.debug(f"API Response: {response}")

    for interface in response.get("rows", []):
        if interface.get("identifier") == "wan":
            for gateway in interface.get("ipv4", []):
                ipaddr = gateway.get("ipaddr", "").split("/")[0]
                try:
                    if ipaddress.ip_address(ipaddr).version == 4:
                        logger.info(f"Public IP found: {ipaddr}")
                        return ipaddr
                except ValueError:
                    logger.warning(f"Invalid IP format: {ipaddr}")
    
    logger.error("Public IP not found.")
    return None

def get_cloudflare_dns_ip(zone_id, record_name, api_token):
    """ Fetches the current IP address of a Cloudflare DNS record. """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json().get("result", [])
        for record in result:
            if record_name in record.get("name"):
                return record["id"], record["content"]
    except requests.RequestException as e:
        logger.error(f"Error fetching DNS record from Cloudflare: {e}")
    return None, None

def update_cloudflare_dns(zone_id, record_id, record_name, new_ip, api_token):
    """ Updates the Cloudflare DNS record with a new IP address. """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
    data = {"type": "A", "name": record_name, "content": new_ip, "ttl": 1, "proxied": False}
    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        logger.info("Successfully updated Cloudflare DNS record.")
    except requests.RequestException as e:
        logger.error(f"Error updating Cloudflare DNS record: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Fetches the public IP from an OPNsense router and updates a Cloudflare DNS record if needed.\n"
            "To enable OPNsense API: \n"
            "1. Log in to OPNsense and go to System > Access > Users.\n"
            "2. Create an API key and enable REST API in System > Settings > Administration.\n"
            "3. Use HTTPS for API access.\n\n"
            "To generate a Cloudflare API Token: \n"
            "1. Go to https://dash.cloudflare.com/profile/api-tokens.\n"
            "2. Create a new API Token with 'Edit' permissions for DNS records.\n"
        )
    )
    parser.add_argument("--opnsense-ip", required=True, help="OPNsense router IP or URL (e.g., https://192.168.1.1)")
    parser.add_argument("--api-key", required=True, help="OPNsense API key")
    parser.add_argument("--api-secret", required=True, help="OPNsense API secret")
    parser.add_argument("--zone-id", required=True, help="Cloudflare Zone ID")
    parser.add_argument("--record-name", nargs='+', required=True, help="Cloudflare DNS record names (not including domain name)")
    parser.add_argument("--api-token", required=True, help="Cloudflare API token")
    args = parser.parse_args()
    
    public_ip = get_opnsense_public_ip(args.opnsense_ip, args.api_key, args.api_secret)
    if public_ip is None:
        logger.error("Failed to retrieve public IP.")
        exit(1)

    for record_name in args.record_name:
        record_id, cloudflare_ip = get_cloudflare_dns_ip(args.zone_id, record_name, args.api_token)
        if record_id is None:
            logger.error(f"Failed to fetch Cloudflare DNS record for {record_name}.")
            continue
        if public_ip != cloudflare_ip:
            logger.info(f"IP mismatch detected for {record_name}. Updating Cloudflare ({cloudflare_ip} -> {public_ip})")
            update_cloudflare_dns(args.zone_id, record_id, record_name, public_ip, args.api_token)
        else:
            logger.info(f"Cloudflare DNS record for {record_name} is already up to date. No update needed.")
