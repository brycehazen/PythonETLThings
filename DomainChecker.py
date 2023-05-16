import csv
import socket
import validators

# Lists to store valid and invalid domains
valid_domains = []
invalid_domains = []

# Open the CSV and read the domain names
with open('valid_emails_Justdomains.csv', 'r') as f:
    reader = csv.reader(f)
    domains = list(reader)

# Check each domain
for domain in domains:
    domain = domain[0] # assuming each row has only one domain
    if validators.domain(domain):
        try:
            # Try to get the IP address
            ip = socket.gethostbyname(domain)
            valid_domains.append(domain)
        except socket.gaierror:
            # If getting the IP address fails, the domain is not valid
            invalid_domains.append(domain)
    else:
        invalid_domains.append(domain)

# Write the valid domains to a CSV
with open('checked_valid.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for domain in valid_domains:
        writer.writerow([domain])

# Write the invalid domains to a CSV
with open('checked_NotValid.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for domain in invalid_domains:
        writer.writerow([domain])
