import asyncio
import os
from playwright.async_api import async_playwright

async def send_gmail(to_email, subject, body):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    user_data_dir = os.path.join(base_dir, "data", "chromium-gmail")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir, headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://mail.google.com/mail/u/0/#inbox?compose=new")
        await page.wait_for_selector("div[role='dialog']", timeout=15000)
        
        print("[Gmail] Compose window open. Executing keystrokes...")
        await asyncio.sleep(3) # Wait for focus to settle on the To field natively
        
        await page.keyboard.type(to_email)
        await asyncio.sleep(1)
        await page.keyboard.press("Enter")
        await asyncio.sleep(1)
        
        await page.keyboard.press("Tab") # Move to subject
        await asyncio.sleep(0.5)
        await page.keyboard.type(subject)
        await asyncio.sleep(1)
        
        await page.keyboard.press("Tab") # Move to body
        await asyncio.sleep(0.5)
        await page.keyboard.type(body)
        await asyncio.sleep(1)
        
        print("[Gmail] Dispatching...")
        await page.keyboard.press("Control+Enter")
        await asyncio.sleep(5)
        await context.close()

async def send_whatsapp(contact, message):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    user_data_dir = os.path.join(base_dir, "data", "chromium-whatsapp")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir, headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://web.whatsapp.com")
        await page.wait_for_selector("div#pane-side", timeout=20000)
        
        print("[WhatsApp] Loaded. Locating textboxes...")
        await asyncio.sleep(2)
        
        # WhatsApp uses contenteditable elements. The first one is the search box.
        textboxes = page.get_by_role("textbox")
        search_box = textboxes.nth(0)
        await search_box.click()
        await asyncio.sleep(1)
        await page.keyboard.type(contact)
        await asyncio.sleep(3) # Wait for search results
        await page.keyboard.press("Enter") # Select the first result
        
        print("[WhatsApp] Chat selected. Typing message...")
        await asyncio.sleep(2)
        
        # The message box is in the footer
        await page.wait_for_selector("footer", timeout=10000)
        message_box = page.locator("footer").get_by_role("textbox")
        await message_box.click()
        await asyncio.sleep(1)
        await page.keyboard.type(message)
        await asyncio.sleep(1)
        
        print("[WhatsApp] Dispatching...")
        await page.keyboard.press("Enter")
        await asyncio.sleep(3)
        await context.close()

async def main():
    email_body = """Hi Jatin,
    
This is J.A.R.V.I.S. reaching out on behalf of my administrator. I'm sending a quick automated update regarding our academic progress.

We are currently tracking our studies for the Bachelor of Science in Cyber Security & Digital Science at MIT ACSC. The immediate focus is the Network Sniffing assignment for the Cyber Security Lab. Additionally, we are actively preparing for the CEH v13 certification, with today's target module being 'Scanning Networks'. 

Please let me know if you would like to collaborate or share study notes on these topics.

Best regards,
J.A.R.V.I.S."""

    whatsapp_msg = "Hello Jatin, this is J.A.R.V.I.S. Just dropping a quick automated update: Currently focusing on the Network Sniffing assignment for the Cyber Security Lab and 'Scanning Networks' for CEH v13 prep. Let me know if you want to collaborate!"

    print("Sending Gmail...")
    try:
        await send_gmail("jatinpardeshi83@gmail.com", "Academic Update & Study Progress", email_body)
        print("Gmail sent successfully.")
    except Exception as e:
        print("Gmail error:", e)
        
    print("\nSending WhatsApp...")
    try:
        await send_whatsapp("jatin", whatsapp_msg)
        print("WhatsApp sent successfully.")
    except Exception as e:
        print("WhatsApp error:", e)

if __name__ == "__main__":
    asyncio.run(main())
