import requests
import threading
from colorama import Fore, Style, init
from fake_useragent import UserAgent
import time

# Colorama ইনিশিয়ালাইজ করা
init(autoreset=True)

class OSINTTracker:
    def __init__(self, username):
        self.username = username
        self.ua = UserAgent()
        self.found_accounts = []
        self.lock = threading.Lock()
        
        # ৫০+ টার্গেট ওয়েবসাইটের লিস্ট (URL প্যাটার্নসহ)
        self.social_sites = {
            "GitHub": "https://github.com/{}",
            "Instagram": "https://www.instagram.com/{}/",
            "Facebook": "https://www.facebook.com/{}",
            "Twitter": "https://twitter.com/{}",
            "Reddit": "https://www.reddit.com/user/{}",
            "YouTube": "https://www.youtube.com/@{}",
            "Pinterest": "https://www.pinterest.com/{}/",
            "Medium": "https://medium.com/@{}",
            "Snapchat": "https://www.snapchat.com/add/{}",
            "Telegram": "https://t.me/{}",
            "TikTok": "https://www.tiktok.com/@{}",
            "Behance": "https://www.behance.net/{}",
            "Dribbble": "https://dribbble.com/{}",
            "Vimeo": "https://vimeo.com/{}",
            "SoundCloud": "https://soundcloud.com/{}",
            "Spotify": "https://open.spotify.com/user/{}",
            "Flickr": "https://www.flickr.com/photos/{}",
            "Quora": "https://www.quora.com/profile/{}",
            "Tumblr": "https://{}.tumblr.com",
            "DeviantArt": "https://www.deviantart.com/{}",
            "Twitch": "https://www.twitch.tv/{}",
            "Steam": "https://steamcommunity.com/id/{}",
            "GitLab": "https://gitlab.com/{}",
            "VK": "https://vk.com/{}",
            "About.me": "https://about.me/{}",
            "Wattpad": "https://www.wattpad.com/user/{}",
            "WordPress": "https://{}.wordpress.com",
            "Blogger": "https://{}.blogspot.com",
            "DailyMotion": "https://www.dailymotion.com/{}",
            "Disqus": "https://disqus.com/by/{}",
            "Patreon": "https://www.patreon.com/{}",
            "ProductHunt": "https://www.producthunt.com/@{}",
            "Slack": "https://{}.slack.com",
            "Imgur": "https://imgur.com/user/{}",
            "ReverbNation": "https://www.reverbnation.com/{}",
            "Bandcamp": "https://bandcamp.com/{}",
            "Codecademy": "https://www.codecademy.com/profiles/{}",
            "Keybase": "https://keybase.io/{}",
            "Last.fm": "https://www.last.fm/user/{}",
            "Letterboxd": "https://letterboxd.com/{}",
            "Roblox": "https://www.roblox.com/user.aspx?username={}",
            "Scratch": "https://scratch.mit.edu/users/{}",
            "Duolingo": "https://www.duolingo.com/profile/{}",
            "Chess.com": "https://www.chess.com/member/{}",
            "Docker Hub": "https://hub.docker.com/u/{}",
            "Gumroad": "https://gumroad.com/{}",
            "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
            "SlideShare": "https://www.slideshare.net/{}",
            "Linktree": "https://linktr.ee/{}",
            "TripAdvisor": "https://www.tripadvisor.com/members/{}"
        }

    def banner(self):
        print(Fore.CYAN + "="*50)
        print(Fore.YELLOW + "      ADVANCED THREADED OSINT USERNAME TRACKER")
        print(Fore.CYAN + "="*50 + "\n")

    def check_site(self, site_name, url_template):
        target_url = url_template.format(self.username)
        headers = {'User-Agent': self.ua.random}
        
        try:
            # অনেক সাইট 403 দেয় যদি হেডারে পর্যাপ্ত তথ্য না থাকে, 
            # তাই timeout এবং allow_redirects ব্যবহার করা হয়েছে।
            response = requests.get(target_url, headers=headers, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                # অতিরিক্ত চেক: কিছু সাইট ইউজার না থাকলেও ২০০ কোড দেয়
                if self.username.lower() in response.text.lower():
                    status = f"{Fore.GREEN}[+] {site_name}: {target_url}"
                    with self.lock:
                        print(status)
                        self.found_accounts.append(f"{site_name}: {target_url}")
                else:
                    print(f"{Fore.RED}[-] {site_name}: Not Found")
            else:
                print(f"{Fore.RED}[-] {site_name}: Not Found")
                
        except requests.exceptions.RequestException:
            print(f"{Fore.YELLOW}[!] {site_name}: Connection Error/Timeout")

    def run(self):
        self.banner()
        print(Fore.WHITE + f"[*] Searching for: {self.username}\n")
        
        threads = []
        for site, url in self.social_sites.items():
            t = threading.Thread(target=self.check_site, args=(site, url))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.save_report()

    def save_report(self):
        print(Fore.CYAN + "\n" + "="*50)
        print(Fore.YELLOW + f"[*] Search Complete! Found: {len(self.found_accounts)} accounts.")
        
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write(f"OSINT Search Report for Username: {self.username}\n")
            f.write("="*50 + "\n")
            for account in self.found_accounts:
                f.write(account + "\n")
        
        print(Fore.GREEN + "[*] Results saved to report.txt")
        print(Fore.CYAN + "="*50)

if __name__ == "__main__":
    try:
        user_input = input(Fore.WHITE + "Enter target username: ").strip()
        if user_input:
            tracker = OSINTTracker(user_input)
            tracker.run()
        else:
            print(Fore.RED + "Invalid Username!")
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Process interrupted by user.")