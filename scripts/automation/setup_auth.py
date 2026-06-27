import asyncio
import os
from playwright.async_api import async_playwright

async def setup_session(service_name, url):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, "data", f"chromium-{service_name}")
    
    print(f"\n[J.A.R.V.I.S.] Starting interactive session for {service_name}.")
    print("Please log in. The browser will remain open until you close it.")
    
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=data_dir,
            headless=False,
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(url)
        print(f"[J.A.R.V.I.S.] Browser ready. Close the browser window when you are fully authenticated.")
        
        # Keep process alive until user closes the persistent context browser
        while True:
            try:
                # If pages are closed, this will eventually error or we can check contexts
                if len(context.pages) == 0:
                    break
                await asyncio.sleep(1)
            except:
                break
            
        print(f"[J.A.R.V.I.S.] Session data for {service_name} saved locally to {data_dir}\n")

async def main():
    print("=== J.A.R.V.I.S. Web Authentication Setup ===")
    print("1. WhatsApp Web (Requires QR Scan)")
    print("2. Gmail (Requires Google Login)")
    choice = input("Select service to authenticate (1/2): ")
    
    if choice == "1":
        await setup_session("whatsapp", "https://web.whatsapp.com/")
    elif choice == "2":
        await setup_session("gmail", "https://mail.google.com/")
    else:
        print("Invalid selection. Exiting.")

if __name__ == "__main__":
    asyncio.run(main())
