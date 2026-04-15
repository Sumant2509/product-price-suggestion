"""
Demo for e-commerce phone search system
Shows phones from Amazon & Flipkart with AI recommendations
"""

from ecommerce_search import EcommercePhoneSearch, display_search_results

def main():
    search = EcommercePhoneSearch()
    search.fetch_phones(use_sample=True)

    print("\n" + "="*70)
    print("  🛒 AMAZON & FLIPKART PHONE FINDER - DEMO")
    print("="*70)

    # Demo 1: Best phone in budget
    print("\n📍 DEMO 1: Best phone under ₹40,000\n")
    best, error = search.get_best_in_budget(40000)
    if best:
        phone = best['phone']
        print(f"✨ Winner: {phone['name']}")
        print(f"   Brand: {phone.get('brand', 'N/A')}")
        print(f"   Platform: {phone['platform']}")
        print(f"   Price: ₹{phone['price']:,}")
        print(f"   Specs: RAM {phone.get('ram')}GB | Camera {phone.get('camera')}MP | Battery {phone.get('battery')}mAh")
        print(f"   Score: {best['total_score']:.2%}")

    # Demo 2: Platform comparison
    print("\n" + "-"*70)
    print("\n📍 DEMO 2: Platform Comparison (Budget: ₹50,000)\n")
    results = search.compare_platforms(50000)
    for platform, result in results.items():
        if result:
            phone = result['phone']
            print(f"🏪 {platform}:")
            print(f"   ✨ {phone['name']} - ₹{phone['price']:,}")
            print(f"   Score: {result['total_score']:.2%}\n")

    # Demo 3: Search by brand
    print("-"*70)
    print("\n📍 DEMO 3: Samsung phones under ₹45,000\n")
    phones = search.search_by_brand('Samsung', 45000)
    if phones:
        for i, phone in enumerate(phones, 1):
            print(f"{i}. {phone['name']}")
            print(f"   Platform: {phone['platform']} | Price: ₹{phone['price']:,}")
            print(f"   Rating: {phone.get('rating')}/5.0\n")
    else:
        print("❌ No Samsung phones found in this budget\n")

    # Demo 4: Daily deals
    print("-"*70)
    print("\n📍 DEMO 4: 🎉 Daily Deals (Budget Phones)\n")
    deals = search.get_deals_of_day()
    display_search_results(deals)

    # Demo 5: All phones from Flipkart
    print("-"*70)
    print("\n📍 DEMO 5: All Phones on Flipkart\n")
    flipkart_phones = search.filter_by_platform('Flipkart')
    for i, phone in enumerate(flipkart_phones, 1):
        print(f"{i}. {phone['name']} - ₹{phone['price']:,} ({phone.get('rating')}/5.0)")

    print("\n" + "="*70)
    print("✅ DEMO COMPLETE")
    print("="*70)
    print("\n💡 To use interactive mode, run: python ecommerce_search.py")

if __name__ == "__main__":
    main()
