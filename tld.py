import os
import sys
import re
import requests
from datetime import datetime, timedelta
from colorama import init as colorama_init
from colorama import Fore, Style
import threading

colorama_init(autoreset=True)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def checkTLD(domain):
    req = requests.get("https://zoxh.com/tld").text
    all_tld = re.findall('/tld/(.*?)"', req)
    if domain in all_tld:
        return True
    else:
        return False

def TLD(domain_tld):
    req = requests.get("https://zoxh.com/tld/{}".format(domain_tld)).text
    total_domain = int(re.findall('href="/tld/{}/(.*?)"'.format(domain_tld), req)[-2])

    print("\nRetrieving domain names for TLD {}...\n".format(domain_tld))

    for i in range(1, total_domain + 1):
        try:
            req_grab = requests.get("https://zoxh.com/tld/{}/{}".format(domain_tld, i)).text
            all_domain = "\n".join(re.findall('/i/(.*?)"', req_grab)).strip("\r\n")
            total_found = len(all_domain.split("\n"))
            print(Fore.RED + "[+] Found {} domain names for TLD {} ({}/{})".format(total_found, domain_tld, i, total_domain) + Style.RESET_ALL)
            open("tld_{}.txt".format(domain_tld), "a").write(all_domain + "\n")
        except:
            pass

    print("\nDomain names for TLD {} retrieved successfully and saved to tld_{}.txt.".format(domain_tld, domain_tld))

def exit_gracefully():
    print('\n\n\t\t[-] Happy Hacking!...')
    sys.exit(0)

def print_banner():
    banner = '''
\t=======================================================================
\t\t\t SICARIOS TLD Grabber v1 - 2023
\t=======================================================================
    '''
    print(Fore.YELLOW + banner + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()

        exptx = '\t\t[+] Enter TLD (for example: com, gov, org, etc..):'
        input_tld = input('\n' + Fore.GREEN + exptx + ' ')

        if checkTLD(input_tld):
            tld_thread = threading.Thread(target=TLD, args=(input_tld,))
            tld_thread.start()

            # Wait for the thread to finish
            tld_thread.join()
        else:
            exit('\n\t\t[-] Unknown TLD')
    except KeyboardInterrupt:
        exit_gracefully()
