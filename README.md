# SSL Self-Signed Setup for `client.services.com`

This guide explains how to generate a self-signed SSL certificate for the domain `client.services.com` and configure it with Nginx.

---

## 🔧 Step-by-Step Instructions

### ✅ Step 1: Create OpenSSL Config File

Create a file named `openssl-client.cnf` with the following content:

```ini
[ req ]
default_bits       = 2048
prompt             = no
default_md         = sha256
distinguished_name = dn
req_extensions     = req_ext

[ dn ]
C  = VN
ST = Hanoi
L  = Hanoi
O  = Example Org
OU = Dev
CN = client.services.com

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = client.services.com
DNS.2 = services.com
DNS.3 = *.services.com
```

### ✅ Step 2: Generate CA Certificate (if not available)

```shell
openssl genrsa -out ca_key.pem 2048
openssl req -x509 -new -nodes -key ca_key.pem -sha256 -days 3650 -out ca_cert.pem -subj "/CN=client.services.com"
```

> Lưu ý: CN là domain đang cần ký
> ca_cert.pem là CA certificate, tương đương "root certificate".

### ✅ Step 3: Generate Server Key & CSR (Certificate Signing Request)

```shell
openssl genrsa -out server_key.pem 2048
openssl req -new -key server_key.pem -out server.csr -config openssl-client.cnf

```

### ✅ Step 4: Sign Server Certificate with CA

```shell
openssl x509 -req \
  -in server.csr \
  -CA ca_cert.pem \
  -CAkey ca_key.pem \
  -CAcreateserial \
  -out server_cert.pem \
  -days 365 \
  -sha256 \
  -extfile openssl-client.cnf \
  -extensions req_ext

chmod 600 /etc/nginx/ssl/server_key.pem
chmod 644 /etc/nginx/ssl/server_cert.pem
```

### ✅ Step 5: Nginx Configuration

```shell
cat <<EOF > /etc/nginx/conf.d/test.conf

server {
        listen 443 ssl;

        server_name client.services.com;

        ssl_certificate     /etc/nginx/ssl/server_cert.pem;
        ssl_certificate_key /etc/nginx/ssl/server_key.pem;

        ssl_client_certificate /etc/nginx/ssl/ca_cert.pem;
        ssl_verify_client off;  # Bật nếu yêu cầu client chứng thực

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
                proxy_pass http://localhost:3001;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }
}
server {
        listen 80;

        server_name client.services.com;

        location / {
                proxy_pass http://localhost:3001;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }
}
EOF
```

### ✅ Step 6: Restart Nginx

```shell
sudo nginx -t && sudo systemctl reload nginx
```

### ✅ Step 7: Import ca_cert.pem into Trusted Root CA

```shell
cat ca_cert.pem
```

Sau đó copy nội dung của file `ca_cert.pem` vào biến `CA_CERT`

### ✅ Step 8: Run file `add_ca_browsers.py` as Admin
