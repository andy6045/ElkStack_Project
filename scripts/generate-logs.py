#!/usr/bin/env python3
"""
Generate sample Apache/Nginx access logs for the ELK dashboard demo.
Produces realistic-looking web server logs with varied IPs, paths, status codes,
user agents, and timestamps.
"""

import random
import datetime

# Sample data pools
IPS = [
    "192.168.1.100", "10.0.0.15", "172.16.0.42", "203.0.113.50",
    "198.51.100.23", "45.33.32.156", "104.26.10.78", "151.101.1.69",
    "185.199.108.153", "140.82.114.3", "52.64.108.95", "13.107.42.14",
    "216.58.214.206", "17.253.144.10", "23.215.0.136", "93.184.216.34",
    "8.8.8.8", "1.1.1.1", "208.67.222.222", "9.9.9.9",
    "54.239.28.85", "76.76.21.21", "199.232.69.194", "151.101.65.140",
]

PATHS = [
    "/", "/index.html", "/about", "/contact", "/products",
    "/api/v1/users", "/api/v1/products", "/api/v1/orders",
    "/api/v1/auth/login", "/api/v1/auth/logout",
    "/static/css/main.css", "/static/js/app.js", "/static/img/logo.png",
    "/blog", "/blog/post-1", "/blog/post-2", "/blog/post-3",
    "/dashboard", "/settings", "/profile", "/admin",
    "/search?q=elastic", "/search?q=kibana", "/search?q=logstash",
    "/api/v1/health", "/api/v1/metrics", "/favicon.ico",
    "/robots.txt", "/sitemap.xml", "/login", "/register",
]

METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
METHOD_WEIGHTS = [60, 20, 10, 5, 5]

STATUS_CODES = [200, 201, 204, 301, 302, 304, 400, 401, 403, 404, 500, 502, 503]
STATUS_WEIGHTS = [50, 5, 3, 5, 5, 10, 5, 3, 2, 8, 2, 1, 1]

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36',
    'curl/8.4.0',
    'python-requests/2.31.0',
    'Googlebot/2.1 (+http://www.google.com/bot.html)',
]

REFERRERS = [
    "-",
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://github.com/",
    "https://stackoverflow.com/",
    "https://example.com/",
    "https://twitter.com/",
    "https://www.reddit.com/",
]


def generate_log_line(timestamp):
    ip = random.choice(IPS)
    method = random.choices(METHODS, weights=METHOD_WEIGHTS, k=1)[0]
    path = random.choice(PATHS)
    status = random.choices(STATUS_CODES, weights=STATUS_WEIGHTS, k=1)[0]
    size = random.randint(128, 65536) if status == 200 else random.randint(0, 1024)
    user_agent = random.choice(USER_AGENTS)
    referrer = random.choice(REFERRERS)

    # Format: Combined Apache Log Format
    ts = timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")
    return f'{ip} - - [{ts}] "{method} {path} HTTP/1.1" {status} {size} "{referrer}" "{user_agent}"'


def main():
    random.seed(42)
    
    # Generate logs spanning the last 7 days
    end_time = datetime.datetime(2024, 1, 15, 23, 59, 59)
    start_time = end_time - datetime.timedelta(days=7)

    lines = []
    current = start_time

    # Generate ~5000 log entries
    num_entries = 5000
    time_span = (end_time - start_time).total_seconds()

    for i in range(num_entries):
        # Add some randomness to timing (simulate traffic patterns)
        progress = i / num_entries
        offset = progress * time_span
        
        # Add burstiness - more traffic during "business hours"
        hour = (start_time + datetime.timedelta(seconds=offset)).hour
        if 9 <= hour <= 17:
            jitter = random.uniform(0, 30)
        else:
            jitter = random.uniform(0, 120)
        
        timestamp = start_time + datetime.timedelta(seconds=offset + jitter)
        lines.append(generate_log_line(timestamp))

    # Sort by timestamp embedded in the line
    with open("/home/ubuntu/elk-dashboard-project/data/sample-access.log", "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Generated {len(lines)} log entries")


if __name__ == "__main__":
    main()
