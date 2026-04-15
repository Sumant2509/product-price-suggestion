"""
Integrated search system for phones on Amazon & Flipkart
with AI-powered recommendations
"""

from phone_comparison_model import PhoneComparisonModel
from ecommerce_scraper import get_ecommerce_phones, SAMPLE_ECOMMERCE_DATA
import random

class EcommercePhoneSearch:
    """Search and recommend phones from Indian e-commerce platforms"""
    
    def __init__(self):
        self.model = PhoneComparisonModel()
        self.all_phones = None
    
    def fetch_phones(self, use_sample=True):
        """Fetch phones from platforms"""
        if use_sample:
            all_phones = SAMPLE_ECOMMERCE_DATA['flipkart'] + SAMPLE_ECOMMERCE_DATA['amazon']
        else:
            all_phones = get_ecommerce_phones()
        
        self.all_phones = all_phones
        return all_phones
    
    def search_by_budget(self, budget: int, brand: str = None) -> list:
        """Search phones within budget on specific platform"""
        phones = self.filter_by_budget(budget)
        
        if brand:
            phones = [p for p in phones if p['brand'].lower() == brand.lower()]
        
        return phones
    
    def filter_by_budget(self, budget: int) -> list:
        """Filter phones within budget"""
        if not self.all_phones:
            self.fetch_phones()
        
        return [p for p in self.all_phones if p['price'] <= budget]
    
    def filter_by_platform(self, platform: str) -> list:
        """Filter phones from specific platform"""
        if not self.all_phones:
            self.fetch_phones()
        
        return [p for p in self.all_phones if p['platform'].lower() == platform.lower()]
    
    def get_best_in_budget(self, budget: int, weights=None) -> dict:
        """Get best phone within budget"""
        phones = self.filter_by_budget(budget)
        
        if not phones:
            return None, f"❌ No phones available below ₹{budget:,}"
        
        best = self.model.get_best_phone(phones, weights)
        return best, None
    
    def compare_platforms(self, budget: int) -> dict:
        """Compare best phones from each platform"""
        if not self.all_phones:
            self.fetch_phones()
        
        results = {}
        
        for platform in ['Flipkart', 'Amazon']:
            platform_phones = self.filter_by_platform(platform)
            filtered = [p for p in platform_phones if p['price'] <= budget]
            
            if filtered:
                best = self.model.get_best_phone(filtered)
                results[platform] = best
            else:
                results[platform] = None
        
        return results
    
    def search_by_brand(self, brand: str, budget: int = None) -> list:
        """Search phones by brand"""
        if not self.all_phones:
            self.fetch_phones()
        
        phones = [p for p in self.all_phones if p.get('brand', 'Unknown').lower() == brand.lower()]
        
        if budget:
            phones = [p for p in phones if p['price'] <= budget]
        
        return phones
    
    def get_deals_of_day(self):
        """Get random budget phones (simulating daily deals)"""
        if not self.all_phones:
            self.fetch_phones()
        
        budget_phones = [p for p in self.all_phones if p['price'] < 40000]
        return random.sample(budget_phones, min(3, len(budget_phones)))

def display_search_results(phones, title="Search Results"):
    """Display search results"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")
    
    if not phones:
        print("❌ No phones found")
        return
    
    for i, phone in enumerate(phones, 1):
        print(f"{i}. {phone['name']}")
        print(f"   Brand: {phone.get('brand', 'N/A')} | Platform: {phone['platform']}")
        print(f"   Price: ₹{phone['price']:,}")
        if 'specs' not in phone:
            specs = f"RAM: {phone.get('ram', 'N/A')}GB | Storage: {phone.get('storage', 'N/A')}GB"
            specs += f" | Camera: {phone.get('camera', 'N/A')}MP | Battery: {phone.get('battery', 'N/A')}mAh"
            print(f"   {specs}")
        print(f"   Rating: {phone.get('rating', 'N/A')}/5.0 ⭐")
        print()

def display_comparison(results, budget):
    """Display platform comparison"""
    print(f"\n{'='*70}")
    print(f"  Platform Comparison (Budget: ₹{budget:,})")
    print(f"{'='*70}\n")
    
    for platform, result in results.items():
        print(f"🏪 {platform}:")
        if result:
            phone = result['phone']
            print(f"   ✨ Best: {phone['name']}")
            print(f"   Price: ₹{phone['price']:,}")
            print(f"   Score: {result['total_score']:.2%}")
            print(f"   Link: {phone.get('url', 'N/A')}")
        else:
            print(f"   ❌ No phones available")
        print()

def main():
    """Interactive e-commerce search"""
    search = EcommercePhoneSearch()
    
    print("\n" + "="*70)
    print("  🛒 AMAZON & FLIPKART PHONE FINDER")
    print("  AI-Powered Recommendations from Indian E-Commerce Platforms")
    print("="*70)
    
    # Fetch phones
    print("\n📱 Loading phones from platforms...")
    search.fetch_phones(use_sample=True)
    print("✅ Loaded successfully!\n")
    
    while True:
        print("\n" + "-"*70)
        print("📋 What would you like to do?")
        print("   1. Find best phone in budget")
        print("   2. Compare platforms (Flipkart vs Amazon)")
        print("   3. Search by brand")
        print("   4. View daily deals (Budget phones)")
        print("   5. View all phones from specific platform")
        print("   6. Exit")
        print("-"*70)
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            try:
                budget = float(input("💰 Enter budget (₹): ₹"))
                best, error = search.get_best_in_budget(int(budget))
                
                if error:
                    print(f"\n{error}")
                elif best:
                    phone = best['phone']
                    print(f"\n✨ BEST PHONE FOR ₹{budget:,.0f}")
                    print(f"{'='*70}")
                    print(f"📱 {phone['name']}")
                    print(f"   Brand: {phone.get('brand', 'N/A')}")
                    print(f"   Platform: {phone['platform']}")
                    print(f"   Price: ₹{phone['price']:,}")
                    print(f"   RAM: {phone.get('ram', 'N/A')}GB | Storage: {phone.get('storage', 'N/A')}GB")
                    print(f"   Camera: {phone.get('camera', 'N/A')}MP | Battery: {phone.get('battery', 'N/A')}mAh")
                    print(f"   Rating: {phone.get('rating', 'N/A')}/5.0")
                    print(f"   Match Score: {best['total_score']:.2%}")
                    print(f"{'='*70}")
            except ValueError:
                print("⚠️  Please enter a valid number")
        
        elif choice == "2":
            try:
                budget = float(input("💰 Enter budget (₹): ₹"))
                results = search.compare_platforms(int(budget))
                display_comparison(results, int(budget))
            except ValueError:
                print("⚠️  Please enter a valid number")
        
        elif choice == "3":
            brand = input("🏷️  Enter brand name (e.g., Samsung, OnePlus, Xiaomi): ").strip()
            budget_input = input("💰 Budget in ₹ (press Enter for no limit): ").strip()
            budget = int(budget_input) if budget_input else None
            
            phones = search.search_by_brand(brand, budget)
            display_search_results(phones, f"Phones from {brand}")
        
        elif choice == "4":
            deals = search.get_deals_of_day()
            display_search_results(deals, "🎉 Daily Deals (Budget Phones)")
        
        elif choice == "5":
            print("\n1. Flipkart")
            print("2. Amazon")
            platform_choice = input("\nSelect platform (1-2): ").strip()
            
            platform = "Flipkart" if platform_choice == "1" else "Amazon"
            phones = search.filter_by_platform(platform)
            display_search_results(phones, f"All Phones on {platform}")
        
        elif choice == "6":
            print("\n👋 Thank you for using Phone Finder!")
            break
        
        else:
            print("⚠️  Invalid option. Please try again.")

if __name__ == "__main__":
    main()
