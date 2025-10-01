# main.py
from Scraper import run_scrape_and_print       
from Serper import serper_search
from Scenario import scenario_txt2img


def main():
    print("\n" + "="*40)
    print(" ✨ Mythic Python Project ✨")
    while True:
        print("="*40)
        print("1) 🧙  Legendary Creatures Scraped from Wikipedia")
        print("2) 🔍  Search the Web about the Legendary Creature")
        print("3) 🎨  Generate an Image of the Legendary Creature")
        print("0) 🚪  Exit")
        print("="*40)
        
        choice = input("Pick an option: ").strip()

        if choice == "1":
            raw = input("How many creature names to show? [up to 50]: ").strip()
            limit = int(raw) if raw else 50
            print("\n⚡ Summoning legendary creatures...\n")
            run_scrape_and_print(limit=limit)
        elif choice == "2":
            q = input("Enter search query: ").strip() or "coffee"
            print("\n🔎 Searching the web with Serper...\n")
            serper_search(q)
        elif choice == "3":
            p = input("Enter your magical image prompt: ").strip() or "random legendary mythical creature"
            print("\n🎨 Generating an image with Scenario AI...\n")
            scenario_txt2img(p)
        elif choice == "0":
            print("\n👋 Until next time, adventurer!\n")
            break
        else:
            print("❌ Invalid choice, try again.")


if __name__ == "__main__":
    main()
