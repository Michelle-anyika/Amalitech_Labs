import random
from pathlib import Path

def generate_logs(lines: int):
    Path("data").mkdir(exist_ok=True)
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    urls = ['/index.html', '/api/data', '/home', '/login']
    statuses = [200, 201, 404, 500, 403]
    
    with open('data/server.log', 'w') as f:
        for i in range(lines):
            ip = f"192.168.1.{random.randint(1, 255)}"
            method = random.choice(methods)
            url = random.choice(urls)
            status = random.choice(statuses)
            bytes_sent = random.randint(100, 5000)
            f.write(f'{ip} - - [10/Oct/2023:13:55:36 -0700] "{method} {url} HTTP/1.1" {status} {bytes_sent}\n')
            
    print(f"Generated {lines} lines to data/server.log")

if __name__ == "__main__":
    generate_logs(1500)
