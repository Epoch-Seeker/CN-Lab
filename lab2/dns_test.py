import socket
import dns.resolver

def dns_queries():
    domain = 'example.com'

    try:
        # Resolve IP address
        ip_address = socket.gethostbyname(domain)
        print(f"A record for {domain}: {ip_address}")

        # Retrieve MX records
        mx_records = dns.resolver.resolve(domain, 'MX')
        print("\nMX Records:")
        for mx in mx_records:
            print(mx.to_text())

        # Retrieve CNAME records (if any)
        try:
            cname_records = dns.resolver.resolve(domain, 'CNAME')
            print("\nCNAME Records:")
            for cname in cname_records:
                print(cname.to_text())
        except dns.resolver.NoAnswer:
            print("\nNo CNAME record found.")

        # Save to file
        with open('dns_query_results.txt', 'w') as file:
            file.write(f"A record: {ip_address}\n")
            file.write("MX Records:\n")
            for mx in mx_records:
                file.write(mx.to_text() + '\n')
            if 'cname_records' in locals():
                file.write("CNAME Records:\n")
                for cname in cname_records:
                    file.write(cname.to_text() + '\n')

        print("\nDNS query results saved to dns_query_results.txt")

    except Exception as e:
        print(f"DNS error: {e}")

if __name__ == '__main__':
    dns_queries()
