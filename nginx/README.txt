Replace your domain address with "n8n.ca" as the Server Name, followed by your certificate and private key for SSL/TLS access in nginx.conf file.

server_name n8n.ca;
ssl_certificate /etc/nginx/ssl/n8n.ca.crt;
ssl_certificate_key /etc/nginx/ssl/n8n.ca.key;