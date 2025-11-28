# National-Bank-Vulnerable-Training-Lab
🏦 National Bank – Vulnerable Training Lab  A purposely vulnerable FastAPI-based web application designed for cybersecurity learning, penetration testing practice, and CTF challenges. This project simulates a small internal banking system containing multiple real‑world security flaws that attackers can exploit to retrieve hidden flags.

This lab is perfect for:

🔥 Beginners learning hacking

🔥 Students practicing web exploitation

🔥 Red‑team training & demonstrations

🔥 CTF competitions

⚠️ Disclaimer

This project is intentionally insecure and should ONLY be run in a safe, isolated environment such as TryHackMe, local VMs, or private labs.
Do NOT deploy it on public servers.

🧩 Included Vulnerabilities

The application contains 4 core vulnerabilities, each hiding a secret flag:

1️⃣ SQL Injection – Login Bypass
1️⃣ SQL Injection – Login Bypass

The authentication page directly inserts user input into an SQL query, allowing attackers to bypass login using traditional SQLi payloads.

2️⃣ Path Traversal – Arbitrary File Read

3️⃣ OS Command Injection – Ping Tool

4️⃣ Hardcoded Logic Flaw – Hidden Admin Backdoor

🚀 Features

Easy to run (uvicorn main:app --reload)

Clear challenges + hints

Flags stored inside secret/

Beginner‑friendly but realistic vulnerabilities

Perfect for self‑study, teaching, or labs
