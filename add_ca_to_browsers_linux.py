import os
import platform
import subprocess
import shutil
import tempfile

CA_CERT = """
-----BEGIN CERTIFICATE-----
MIIFFTCCAv2gAwIBAgIUHAi5oJV1juN7LO2B0GELEjoHkAIwDQYJKoZIhvcNAQEL
BQAwGjEYMBYGA1UEAwwPY2VydC50aW5hLmxvY2FsMB4XDTI1MDIyODA3MDQ1M1oX
DTM1MDIyNjA3MDQ1M1owGjEYMBYGA1UEAwwPY2VydC50aW5hLmxvY2FsMIICIjAN
BgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAxpUcCqHWPU4eE1TSqrJVfxHjnXeE
K22lkbmplQE4hBjS2zTbpJBnVIBbEtmBZZ70UhIsn4Gvhh34feKo/iDJHRn5OLmG
lrs7Rp3L9vnI4EeQN3orwcmgJd72/Pr9jtRlk1nl53noCaqCu9trNSzd/iSVldKt
tmkHCv8Lua0LRL/WO5cv3GpDKeGrlEayDHYI74gPp+aCzjB2ZaFgfRBA9BNIqLWc
6FS3FeTV3fnf5bQ2LdkNl3NmA6rvnb+A5R5GFiHZTqOSSJ2/QdyXNNN3Qm5K1UOe
7VEqLBomdCGichUuFU6uz6b16OaTmNpg6RkbHQB/ASnmfPnO5i0EslSrR2398uK8
It3Ahq//Aw+xVuyXx1LblUuA8fAUoIIHst+2ey7k7jYFrtN20+EDUSkz5uJLwboI
cVJiOhkypkGOQwWKtPj6tlZYgl57Jab+liEJhVC+t6MWIhv82McaI6wKjGUbNqGH
Z+twfDrw/MIR+xCxCIMCKQ1f544VEgvWebJ+q17NVx1P79wb7/A/dGTNPX+Ah7/U
5J2nE48xEXhSl2FW/KMyaz43NXdtHv54WCvf0W0cpWTIa4FLuUtq6y1zoDa2/kGn
FQB6vEolf0XOdXj1Wg5/oKYKEQsLwxup9mK3IsyiuvEZNjSgfe0rakmF8QmtK0xR
7UhZ5t+YwrV4WfMCAwEAAaNTMFEwHQYDVR0OBBYEFF8YgbV2WLQt7+vRnXj5xjDX
QEyIMB8GA1UdIwQYMBaAFF8YgbV2WLQt7+vRnXj5xjDXQEyIMA8GA1UdEwEB/wQF
MAMBAf8wDQYJKoZIhvcNAQELBQADggIBAKnrIvNfcedEffqZVK2BYpecy+LlbFwv
VZA25RgQpyAqfO8Y9vRkTW9XdtxoRutrZxliyY5I1im8J56c8gwbjFNevLi6u3Co
eZeVUC4vlFk06p7gxCTbjZS/8B/BpGbMBxm/if42Qpvn/zjSi7xJgfDwcKEsF7Qb
eK8G7dBI/lGqygx4MWsjJ8PcEubuyQkHQjfmdW22+XX0UuHw5b3jRvEJbpO/MJCl
x+wWsoGp52EFunIIDura5rCLZhV9p7Qz6BvnNuQCyAUN8Z4whF99G2bIifu39fVh
wsM5BTQ997FlDko7qQOMBykbVAxZkM00oO7OK7wKZ7MPwakmdbNYZ/GBLmi4QaPo
WI3c2RNYlpymGfPDNW5tiw5M3RJzC7VgQjUu7B5Od2NFfbZrs14RwLtE2pbz34Fk
Zru2SwBpYsK0QS7Rs+k71mZzSFyatRtjv92td6EzwQR5err2P9bADtHFrOgPqgqD
NPGNHgk8mKcO4hI+/EStOu5/xL1PZoghLSIyeSVdcAu+YGHljwlochnurLPX9lbJ
/cuogCc04s3gywhRNCKI6r+csHgOxFzR5dSPiq59Q/M9lHaakrhKpFHyFFQhDKqi
lNVJnXfU6LVMyhnIxesPSZ/Ppv4z63G12LqbL2gT/6vDLllaXXGI5C0YyP/Pjl32
QK4aNQw5NZSN
-----END CERTIFICATE-----
"""
CA_NAME = "cert.tina.local"
NSS_DB = os.path.expanduser("~/.pki/nssdb")

# Xác định hệ điều hành
OS_TYPE = platform.system()

# Tạo file CA trong thư mục tạm
def create_ca_file():
    """Tạo file chứng chỉ CA ở thư mục tạm phù hợp với hệ điều hành"""
    temp_dir = tempfile.gettempdir()  # Tự động lấy thư mục tạm của hệ thống
    ca_path = os.path.join(temp_dir, "ca_cert.crt")

    with open(ca_path, "w") as f:
        f.write(CA_CERT)
    
    print(f"[+] CA file đã được tạo tại: {ca_path}")
    return ca_path

def install_ca_linux(ca_path):
    """Thêm CA vào hệ thống Linux"""
    print("[+] Thêm CA vào Linux...")

    # Xác định thư mục lưu chứng chỉ
    target_path = f"/usr/local/share/ca-certificates/{CA_NAME}.crt"
    
    # Copy file đến thư mục hệ thống
    shutil.copy(ca_path, target_path)

    # Cập nhật chứng chỉ
    subprocess.run(["sudo", "update-ca-certificates"], check=True)
    print("[✅] CA đã được thêm vào hệ thống Linux!")

def install_ca_firefox_linux(ca_path):
    """Thêm CA vào Firefox trên Linux"""
    print("[+] Thêm CA vào Firefox trên Linux...")

    firefox_profiles_path = os.path.expanduser("~/.mozilla/firefox/")
    if not os.path.exists(firefox_profiles_path):
        print("[❌] Firefox không được tìm thấy!")
        return

    for profile in os.listdir(firefox_profiles_path):
        cert_db_path = os.path.join(firefox_profiles_path, profile)
        if os.path.isdir(cert_db_path):
            subprocess.run([
                "certutil", "-A", "-n", CA_NAME, "-t", "CT,c,C",
                "-i", ca_path, "-d", f"sql:{cert_db_path}"
            ], check=True)
    
    print("[✅] CA đã được thêm vào Firefox trên Linux!")

def install_ca_chrome_linux(ca_path):
    """Thêm CA vào Google Chrome trên Linux"""
    print("[+] Thêm CA vào Google Chrome trên Linux...")
    
    if not os.path.exists(NSS_DB):
        print("[+] Tạo thư mục NSS database...")
        os.makedirs(NSS_DB, exist_ok=True)
        subprocess.run(["certutil", "-N", "-d", f"sql:{NSS_DB}", "--empty-password"], check=True)
    
    subprocess.run([
        "certutil", "-A", "-n", CA_NAME, "-t", "CT,c,C", "-i", ca_path, "-d", f"sql:{NSS_DB}"
    ], check=True)
    print("[✅] CA đã được thêm vào Google Chrome.")

def main():
    """Chạy cài đặt CA trên Linux"""
    print("[🔹] Bắt đầu thêm CA vào hệ thống Linux và trình duyệt...")

    # Tạo file CA trước khi thêm vào hệ thống
    ca_path = create_ca_file()

    # Cài đặt CA cho Linux
    if OS_TYPE == "Linux":
        install_ca_linux(ca_path)
        install_ca_firefox_linux(ca_path)
        install_ca_chrome_linux(ca_path)

    print("[✅] Hoàn tất! CA đã được thêm vào hệ thống & trình duyệt.")

if __name__ == "__main__":
    main()
