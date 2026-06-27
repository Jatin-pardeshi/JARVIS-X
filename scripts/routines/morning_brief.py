import datetime
import os

def generate_briefing():
    today = datetime.date.today().isoformat()
    briefing_content = f"""# ☀️ J.A.R.V.I.S. Morning Briefing
**Date:** {today} | **Time:** 08:00 AM
**Location:** Pune, India

## ⛅ Weather & Environment
- **Condition:** Clear
- **Temperature:** 24°C

## 🎓 Academic Radar (MIT ACSC)
> [!IMPORTANT]
> **Immediate Deadlines:**
> - Cyber Security Lab: Network Sniffing Assignment (Due: TBD)

> [!NOTE]
> **CEH v13 Prep Progress:**
> - [x] Footprinting and Reconnaissance Lab
> - [ ] Today's Target: Scanning Networks

## 📥 Communication Ledger
- **High-Priority Emails:** 0
- **WhatsApp Mentions/Logistics:** 0
- *See `ledger.md` for full breakdown and generated drafts.*

## 🏋️‍♂️ Lifestyle & Hypertrophy
- **Training Block:** Push
- **Target Time:** 18:00
- **Caloric/Macro Goal:** 2800 kcal, 180g Protein

## 🛡️ System Health & Lab Status
- **Lab Environments:** Offline
"""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    briefings_dir = os.path.join(base_dir, "briefings")
    os.makedirs(briefings_dir, exist_ok=True)
    
    file_path = os.path.join(briefings_dir, f"briefing_{today}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(briefing_content)
    print(f"Morning briefing generated at {file_path}")

if __name__ == "__main__":
    generate_briefing()
