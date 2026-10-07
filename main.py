import json, base64, hashlib
from urllib.request import urlopen
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

URL = "https://raw.githubusercontent.com/Fenix1998x/GEN-SERVIDORES-NUEVO-24-08-2027/refs/heads/main/Fenix"
CRYPTO_PASS = "🔥🔥🔥vpnfenix⭐️⭐️⭐️"
ACCESS_PASS = "JT"
NAJU = "FenxM22_07!89Dev"
HEADER = b"WakkoDev"
SALT_LEN = 8

KEY_MAP = {
    "p0PgL3l0d89mnssz7ImPJA==": "Nombre",
    "66P9ZUEM1ju4WGhv856BSg==": "Info",
    "ACqWMY4zuZWzSEs8cZMXIw==": "Bandera",
    "U7V8DoP4cYkXJjCnpqW6nQ==": "IP",
    "p9ZPlMv9V7gDszRoUaNaJw==": "Puerto",
    "maGFM5lWW4YSDpfPQBmdRA==": "SSL",
    "SbDP19AbQur0YtkkyRlVMA==": "Proxy",
    "vXfVafVdyaCRTDj6uBT6lg==": "PuertoProxy",
    "PFFSWRJKZmOcNLTZxFwgjQ==": "Payload",
    "tmSbWiCK1hvytJ9f3gflkQ==": "SNI",
    "mtw364P3ZslP2CZYuHTCHQ==": "Usuario",
    "Fo3TT4oONvv69IQIMg1aLg==": "Contraseña",
    "UxdyIntdYykCdV76crKnwg==": "Clave",
    "l7MIgkbuXMmGaaQGd54F2w==": "DNS",
    "QSln2zKCBJvqH9qV4M0ifg==": "DNS2",
}

def gen_key(pwd, salt):
    data = b""
    prev = b""
    while len(data) < 48:
        prev = hashlib.md5(prev + pwd.encode() + salt).digest()
        data += prev
    return data[:32], data[32:]

def decifrar_datos(b64texto, pwd):
    raw = base64.b64decode(b64texto)
    salt = raw[len(HEADER):][:SALT_LEN]
    datos = raw[len(HEADER)+SALT_LEN:]
    clave, iv = gen_key(pwd, salt)
    c = AES.new(clave, AES.MODE_CBC, iv)
    return unpad(c.decrypt(datos), 16).decode("utf-8")

def decifrar_valor(texto, secreto):
    if not texto: return ""
    try:
        b = base64.urlsafe_b64decode(texto + "==")
        iv, dats = b[:16], b[16:]
        k = hashlib.sha256(secreto.encode()).digest()
        c = AES.new(k, AES.MODE_CBC, iv)
        res = unpad(c.decrypt(dats), 16).decode("utf-8")
        return "".join(chr((ord(x)-5-65)%26+65 if x.isupper() else (ord(x)-5-97)%26+97) if x.isalpha() else x for x in res)
    except:
        return texto

def renombrar(d):
    if isinstance(d, dict):
        return {KEY_MAP.get(k,k): renombrar(v) for k,v in d.items()}
    if isinstance(d, list):
        return [renombrar(x) for x in d]
    return d

print("="*40)
print("   🔐 FENIX DESCIFRADOR")
print("="*40)

clave = input("Escribe la contraseña: ").strip()
if clave != ACCESS_PASS:
    print("❌ Incorrecta")
    exit()

print("\n🔄 Descargando...")
datos_brutos = urlopen(URL).read().decode().strip()
print("🔓 Descifrando...")
texto = decifrar_datos(datos_brutos, CRYPTO_PASS)
obj = json.loads(texto)

if "Servers" in obj:
    for s in obj["Servers"]:
        for k in list(s.keys()):
            if isinstance(s[k], str):
                s[k] = decifrar_valor(s[k], NAJU)

obj = renombrar(obj)

print("\n✅ ¡LISTO! Resultado:\n")
print(json.dumps(obj, indent=2, ensure_ascii=False))
print("\n" + "="*40)
