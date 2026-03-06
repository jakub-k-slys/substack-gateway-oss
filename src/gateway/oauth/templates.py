"""HTML templates for the two-phase login flow."""

_LOGIN_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Substack Gateway — Sign in (1/2)</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #f5f5f0; min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
    }}
    .card {{
      background: #fff; border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,.08);
      padding: 40px 36px; width: 100%; max-width: 380px;
    }}
    .step {{ font-size: .78rem; color: #999; font-weight: 600;
             letter-spacing: .05em; text-transform: uppercase; margin-bottom: 6px; }}
    h1 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; color: #111; }}
    .sub {{ font-size: .9rem; color: #666; margin-bottom: 28px; }}
    label {{ display: block; font-size: .85rem; font-weight: 600;
             color: #333; margin-bottom: 6px; }}
    input[type=email], input[type=password] {{
      width: 100%; padding: 10px 12px;
      border: 1.5px solid #ddd; border-radius: 8px;
      font-size: .95rem; outline: none; margin-bottom: 18px;
      transition: border-color .15s;
    }}
    input:focus {{ border-color: #ff6719; }}
    button {{
      width: 100%; padding: 11px; background: #ff6719; color: #fff;
      border: none; border-radius: 8px; font-size: 1rem;
      font-weight: 600; cursor: pointer; transition: background .15s;
    }}
    button:hover {{ background: #e55c12; }}
    .error {{
      color: #c0392b; font-size: .88rem; margin-bottom: 16px;
      padding: 10px 12px; background: #fdf3f3;
      border-radius: 6px; border: 1px solid #f5c6cb;
    }}
  </style>
</head>
<body>
  <div class="card">
    <p class="step">Step 1 of 2</p>
    <h1>Substack Gateway</h1>
    <p class="sub">Sign in with your account credentials</p>
    {error}
    <form method="post">
      <input type="hidden" name="request_id" value="{request_id}">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required autofocus
             placeholder="you@example.com">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required
             placeholder="••••••••">
      <button type="submit">Continue →</button>
    </form>
  </div>
</body>
</html>
"""

_TOKEN_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Substack Gateway — Connect Substack (2/2)</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #f5f5f0; min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
    }}
    .card {{
      background: #fff; border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,.08);
      padding: 40px 36px; width: 100%; max-width: 420px;
    }}
    .step {{ font-size: .78rem; color: #999; font-weight: 600;
             letter-spacing: .05em; text-transform: uppercase; margin-bottom: 6px; }}
    h1 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; color: #111; }}
    .sub {{ font-size: .9rem; color: #666; margin-bottom: 28px; }}
    label {{ display: block; font-size: .85rem; font-weight: 600;
             color: #333; margin-bottom: 6px; }}
    .hint {{ font-size: .78rem; color: #888; margin-top: -12px; margin-bottom: 16px; }}
    input[type=text], input[type=url], input[type=password] {{
      width: 100%; padding: 10px 12px;
      border: 1.5px solid #ddd; border-radius: 8px;
      font-size: .95rem; outline: none; margin-bottom: 6px;
      transition: border-color .15s; font-family: monospace;
    }}
    input[type=url] {{ font-family: inherit; margin-bottom: 6px; }}
    input:focus {{ border-color: #ff6719; }}
    button {{
      width: 100%; padding: 11px; background: #ff6719; color: #fff;
      border: none; border-radius: 8px; font-size: 1rem;
      font-weight: 600; cursor: pointer; transition: background .15s;
      margin-top: 12px;
    }}
    button:hover {{ background: #e55c12; }}
    .error {{
      color: #c0392b; font-size: .88rem; margin-bottom: 16px;
      padding: 10px 12px; background: #fdf3f3;
      border-radius: 6px; border: 1px solid #f5c6cb;
    }}
    details {{ margin-bottom: 20px; }}
    summary {{
      font-size: .82rem; color: #888; cursor: pointer;
      user-select: none; padding: 4px 0;
    }}
    .howto {{
      font-size: .82rem; color: #555; margin-top: 10px; line-height: 1.6;
      background: #f9f9f6; border-radius: 6px; padding: 12px 14px;
    }}
    code {{
      background: rgba(0,0,0,.06); padding: 1px 5px; border-radius: 3px;
      font-size: .9em;
    }}
  </style>
</head>
<body>
  <div class="card">
    <p class="step">Step 2 of 2</p>
    <h1>Connect your Substack</h1>
    <p class="sub">Enter your Substack session cookies so the gateway can act on your behalf</p>
    {error}
    <details>
      <summary>How do I find these values?</summary>
      <div class="howto">
        <ol style="padding-left:18px">
          <li>Open <strong>substack.com</strong> and sign in</li>
          <li>Open DevTools → Application → Cookies → <code>https://substack.com</code></li>
          <li>Copy the values for <code>substack.sid</code> and <code>connect.sid</code></li>
        </ol>
      </div>
    </details>
    <form method="post">
      <input type="hidden" name="session_id" value="{session_id}">

      <label for="substack_sid">substack.sid cookie</label>
      <input type="password" id="substack_sid" name="substack_sid" required
             placeholder="s%3A…">
      <p class="hint">Value of the <code>substack.sid</code> cookie</p>

      <label for="connect_sid">connect.sid cookie</label>
      <input type="password" id="connect_sid" name="connect_sid" required
             placeholder="s%3A…">
      <p class="hint">Value of the <code>connect.sid</code> cookie</p>

      <label for="pub_url">Publication URL</label>
      <input type="url" id="pub_url" name="pub_url" required
             placeholder="https://yourname.substack.com"
             style="font-family:inherit">
      <p class="hint">Your Substack publication URL (no trailing slash)</p>

      <button type="submit">Authorize</button>
    </form>
  </div>
</body>
</html>
"""
