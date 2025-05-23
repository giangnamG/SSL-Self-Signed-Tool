import os
import platform
import subprocess
import shutil
import tempfile


CA_CERT = """
-----BEGIN CERTIFICATE-----
MIICxTCCAa0CFFqn1+OmcVNyc20RHQlD9auIy876MA0GCSqGSIb3DQEBCwUAMB8x
HTAbBgNVBAMMFGdpdGxhYi5jeXBlYWNlLmxvY2FsMB4XDTI1MDUxNjA2MjI1MloX
DTM1MDUxNDA2MjI1MlowHzEdMBsGA1UEAwwUZ2l0bGFiLmN5cGVhY2UubG9jYWww
ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCQDZDeCVuJfu15AYh/RwNj
7mWgPr9BlSKYpjL01NBD89Ub3ldop8DIRzPW2QFgtgH68CyYVKpXQu+uj8vhsOvC
KQenjdjA9Auxjwddq2hCKz/98Ut5/O4zUHe+DQWvFVCc2rbdLDoUauTLgRBDsL4E
0sBJSRPBDBo/wsamtugQW3jECVrVOsAsNNrfXmoekQAVWOQZi/Q/XxVCRzx2DQ6y
RwuxhIq3RqUsdzqasVJhHu87pGa7SGTIMsBkvrkPW0WDKoDDb63TXVUpQ4gzbXb3
dUBSpTdKdDKM91DT7o0WWPYVhd1AAnLx0ryMTkeknp8vmEo3E6uo68/TptlzG25p
AgMBAAEwDQYJKoZIhvcNAQELBQADggEBAIAcMgpFiEhBBhBhYmqcUI6gqiF3vOtr
0mmtFvb5nHv4N+VfBgXni+ziXSBBUTzc9wMKoZuJOqfplWBmSxxt9nfQVU9F3lWE
ygYjjmPUC/Qr6oPBuj6h5kNapMZeqXf2qgc896fDBcrTDhvgzh05iEqBJmRqHF9u
vXJFA4l9QCthb3bHtfdIoGeAg9cFQDCdrWAmQDgOulruaCNKOwz2fIukNU+j4+ml
WkSaENGjclydtE27BCMh/k7ElTfPTQQHkiBgu4r2ox1Svhiy+D0JhF7FXsq9hi8b
kGWas8RKNbgiROpu8FhuZa1iWnCkncRQq7rT1oHP/DXdKuNEmBh4Fw4=
-----END CERTIFICATE-----
"""
CA_NAME = "Cypeace"

# Xác định hệ điều hành
OS_TYPE = platform.system()

# Tạo file CA trong thư mục tạm
def create_ca_file():
    """Tạo file chứng chỉ CA ở thư mục tạm phù hợp với hệ điều hành"""
    temp_dir = tempfile.gettempdir()  # Tự động lấy thư mục tạm của hệ thống
    ca_path = os.path.join(temp_dir, "ca_cert.pem")

    with open(ca_path, "w") as f:
        f.write(CA_CERT)
    
    print(f"[+] CA file đã được tạo tại: {ca_path}")
    return ca_path

def install_ca_linux(ca_path):
    """Thêm CA vào hệ thống Linux"""
    print("[+] Thêm CA vào Linux...")
    target_path = f"/usr/local/share/ca-certificates/{CA_NAME}.crt"
    shutil.copy(ca_path, target_path)
    os.system("sudo update-ca-certificates")

def install_ca_macos(ca_path):
    """Thêm CA vào macOS"""
    print("[+] Thêm CA vào macOS...")
    os.system(f"sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain {ca_path}")

def install_ca_windows(ca_path):
    """Thêm CA vào Windows"""
    print("[+] Thêm CA vào Windows...")
    subprocess.run(["certutil", "-addstore", "Root", ca_path], check=True)

def install_ca_firefox(ca_path):
    """Thêm CA vào Firefox"""
    print("[+] Thêm CA vào Firefox...")

    if OS_TYPE == "Linux":
        firefox_profiles_path = os.path.expanduser("~/.mozilla/firefox/")
    elif OS_TYPE == "Windows":
        firefox_profiles_path = os.path.expandvars(r"%APPDATA%\Mozilla\Firefox\Profiles")
    else:
        return  # Không hỗ trợ Firefox trên macOS

    if not os.path.exists(firefox_profiles_path):
        print("[❌] Firefox không được tìm thấy!")
        return

    for profile in os.listdir(firefox_profiles_path):
        cert_db_path = os.path.join(firefox_profiles_path, profile)
        if os.path.isdir(cert_db_path):
            subprocess.run([
                "certutil", "-A", "-n", CA_NAME, "-t", "CT,c,C",
                "-i", ca_path, "-d", f"sql:{cert_db_path}"
            ], check=False)

def install_ca_chrome(ca_path):
    """Thêm CA vào Chrome"""
    print("[+] Thêm CA vào Chrome...")
    if OS_TYPE == "Linux":
        install_ca_linux(ca_path)
    elif OS_TYPE == "Windows":
        install_ca_windows(ca_path)
    elif OS_TYPE == "Darwin":
        install_ca_macos(ca_path)

def main():
    """Chạy cài đặt CA trên tất cả trình duyệt & hệ thống"""
    print("[🔹] Bắt đầu thêm CA vào hệ thống và trình duyệt...")

    # Tạo file CA trước khi thêm vào hệ thống
    ca_path = create_ca_file()

    # Thêm CA vào hệ thống
    if OS_TYPE == "Linux":
        install_ca_linux(ca_path)
    elif OS_TYPE == "Windows":
        install_ca_windows(ca_path)
    elif OS_TYPE == "Darwin":
        install_ca_macos(ca_path)

    # Thêm CA vào Firefox và Chrome
    install_ca_firefox(ca_path)
    install_ca_chrome(ca_path)

    print("[✅] Hoàn tất! CA đã được thêm vào hệ thống & trình duyệt.")

if __name__ == "__main__":
    main()
