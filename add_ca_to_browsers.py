import os
import platform
import subprocess
import shutil
import tempfile


CA_CERT = """
-----BEGIN CERTIFICATE-----
MIIDHTCCAgWgAwIBAgIUVQqb0MvHsU86wlgXzwbTm5gNuwUwDQYJKoZIhvcNAQEL
BQAwHjEcMBoGA1UEAwwTY2xpZW50LnNlcnZpY2VzLmNvbTAeFw0yNTA0MjMyMzU0
MDlaFw0zNTA0MjEyMzU0MDlaMB4xHDAaBgNVBAMME2NsaWVudC5zZXJ2aWNlcy5j
b20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQClIxgkePMbhbMiC2xZ
i4sEA/mPYH2d6p2KZthPrmPk9UryjmB1pWzSPdxCaRuhpo5gmH6HVBU9ammJI6af
suv1bYNGDd1g0NN1fqmMvx1YrkA/8Jk8qdUQ58+DNZjTNtpJLr8hbzPMMQ3RkHaq
rHT5Jcg59A24pa76Dqt27Fov3YphQ3oR+wAljaFbYq+LmE3RXHQK9DocKkybceKR
tGANgFCZV5fsipJZBTzB9HiG4r1nZb2VVKaAjDE2/PSrvo5KJluSgtx+T95FI2nk
AankgLaRFbhL9OP749aRpqex1PaQLWSo+EIryjYKsXdLWJ0sj5Ckef8FYfvuIBsj
I/OFAgMBAAGjUzBRMB0GA1UdDgQWBBT0Z2nwJQwkptHYgIhM+hTAz5OLbzAfBgNV
HSMEGDAWgBT0Z2nwJQwkptHYgIhM+hTAz5OLbzAPBgNVHRMBAf8EBTADAQH/MA0G
CSqGSIb3DQEBCwUAA4IBAQBMefw1f996rSR4tR7RGogkUH7sxVRbsEOxZtvX3hys
RFBhM7dIymPDX8oWwRpmuBgwiRyMwuUaOFmj3VPRLrNfEM5uanz5Zmdu8FD8pNQK
iS3pI6g8G5Kc8kaT9r7g8Ftn5oqK9tEehRl1NB9L84wErTUUtgzRPtoblRSYqRHI
mKD3q8aX2iquM98acPiE3Wi+s2z7Lc7t4X+ds6fGQESvq89fHm1VrGtZSQ8/61f9
E/EUsyf+Aphhx/EEaQXYvbN4eRwnGegTMTmH80/ZPJXoSStE6fjV3GlDUaA1UU16
5a1OhMQckMxJ3QIuun7h6KDzqrerQ0iwRO1d4r+IiXpb
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
