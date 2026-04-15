"""
Phone comparison with detailed spec analysis
Shows which phones are best in each category
"""

from ecommerce_search import EcommercePhoneSearch

class PhoneAnalyzer:
    """Analyze and compare phones by different criteria"""
    
    def __init__(self, phones):
        self.phones = phones
    
    def find_best_camera(self):
        """Find phone with best camera"""
        return max(self.phones, key=lambda p: p['camera'])
    
    def find_best_battery(self):
        """Find phone with best battery"""
        return max(self.phones, key=lambda p: p['battery'])
    
    def find_best_ram(self):
        """Find phone with best RAM"""
        return max(self.phones, key=lambda p: p['ram'])
    
    def find_best_storage(self):
        """Find phone with best storage"""
        return max(self.phones, key=lambda p: p['storage'])
    
    def find_best_rating(self):
        """Find phone with best rating"""
        return max(self.phones, key=lambda p: p['rating'])
    
    def find_cheapest(self):
        """Find cheapest phone"""
        return min(self.phones, key=lambda p: p['price'])
    
    def get_all_comparisons(self):
        """Get all category winners"""
        return {
            '📷 Best Camera': self.find_best_camera(),
            '🔋 Best Battery': self.find_best_battery(),
            '⚡ Best Performance (RAM)': self.find_best_ram(),
            '💾 Best Storage': self.find_best_storage(),
            '⭐ Highest Rated': self.find_best_rating(),
            '💰 Cheapest': self.find_cheapest(),
        }
    
    def get_spec_comparison(self, phone):
        """Get how phone compares in each spec"""
        max_camera = max(self.phones, key=lambda p: p['camera'])['camera']
        max_battery = max(self.phones, key=lambda p: p['battery'])['battery']
        max_ram = max(self.phones, key=lambda p: p['ram'])['ram']
        max_storage = max(self.phones, key=lambda p: p['storage'])['storage']
        max_price = max(self.phones, key=lambda p: p['price'])['price']
        min_price = min(self.phones, key=lambda p: p['price'])['price']
        
        return {
            'camera_percent': (phone['camera'] / max_camera) * 100,
            'battery_percent': (phone['battery'] / max_battery) * 100,
            'ram_percent': (phone['ram'] / max_ram) * 100,
            'storage_percent': (phone['storage'] / max_storage) * 100,
            'price_percent': ((max_price - phone['price']) / (max_price - min_price)) * 100 if max_price != min_price else 50,
        }
    
    def get_strengths_weaknesses(self, phone):
        """Identify phone's strengths and weaknesses"""
        comparison = self.get_spec_comparison(phone)
        strengths = []
        weaknesses = []
        
        if comparison['camera_percent'] >= 90:
            strengths.append(f"💪 Excellent Camera ({phone['camera']}MP)")
        elif comparison['camera_percent'] < 50:
            weaknesses.append(f"⚠️ Below average camera ({phone['camera']}MP)")
        
        if comparison['battery_percent'] >= 90:
            strengths.append(f"💪 Excellent Battery ({phone['battery']}mAh)")
        elif comparison['battery_percent'] < 50:
            weaknesses.append(f"⚠️ Below average battery ({phone['battery']}mAh)")
        
        if comparison['ram_percent'] >= 90:
            strengths.append(f"💪 Excellent RAM ({phone['ram']}GB)")
        elif comparison['ram_percent'] < 50:
            weaknesses.append(f"⚠️ Limited RAM ({phone['ram']}GB)")
        
        if comparison['storage_percent'] >= 90:
            strengths.append(f"💪 Huge Storage ({phone['storage']}GB)")
        elif comparison['storage_percent'] < 50:
            weaknesses.append(f"⚠️ Limited Storage ({phone['storage']}GB)")
        
        if comparison['price_percent'] >= 70:
            strengths.append(f"💪 Great Value Price (₹{phone['price']:,})")
        elif comparison['price_percent'] < 30:
            weaknesses.append(f"⚠️ Expensive (₹{phone['price']:,})")
        
        return strengths, weaknesses

def display_category_winners(budget):
    """Display which phone is best in each category"""
    search = EcommercePhoneSearch()
    search.fetch_phones(use_sample=True)
    
    phones = search.filter_by_budget(budget)
    
    if not phones:
        print(f"❌ No phones available below ₹{budget:,}")
        return
    
    analyzer = PhoneAnalyzer(phones)
    comparisons = analyzer.get_all_comparisons()
    
    print("\n" + "="*80)
    print(f"  📊 BEST PHONES BY CATEGORY (Budget: ₹{budget:,})")
    print("="*80 + "\n")
    
    for category, phone in comparisons.items():
        if category == '📷 Best Camera':
            spec = f"({phone['camera']}MP)"
        elif category == '🔋 Best Battery':
            spec = f"({phone['battery']}mAh)"
        elif category == '⚡ Best Performance (RAM)':
            spec = f"({phone['ram']}GB)"
        elif category == '💾 Best Storage':
            spec = f"({phone['storage']}GB)"
        elif category == '⭐ Highest Rated':
            spec = f"({phone['rating']}/5.0)"
        elif category == '💰 Cheapest':
            spec = f"(₹{phone['price']:,})"
        else:
            spec = ""
        
        print(f"{category} {spec}")
        print(f"   {phone['name']} by {phone['brand']}")
        print(f"   Platform: {phone['platform']} | Price: ₹{phone['price']:,}\n")

def display_detailed_analysis(phone_name, budget):
    """Show detailed analysis of a specific phone"""
    search = EcommercePhoneSearch()
    search.fetch_phones(use_sample=True)
    
    phones = search.filter_by_budget(budget)
    
    # Find phone by name
    target_phone = None
    for phone in phones:
        if phone_name.lower() in phone['name'].lower():
            target_phone = phone
            break
    
    if not target_phone:
        print(f"\n❌ Phone '{phone_name}' not found in this budget")
        return
    
    analyzer = PhoneAnalyzer(phones)
    comparison = analyzer.get_spec_comparison(target_phone)
    strengths, weaknesses = analyzer.get_strengths_weaknesses(target_phone)
    
    print("\n" + "="*80)
    print(f"  📱 DETAILED ANALYSIS: {target_phone['name']}")
    print("="*80)
    print(f"\nBrand: {target_phone['brand']}")
    print(f"Platform: {target_phone['platform']}")
    print(f"Price: ₹{target_phone['price']:,}")
    print(f"Rating: {target_phone['rating']}/5.0 ⭐\n")
    
    print("📊 SPECIFICATIONS:")
    print(f"   Camera:  {target_phone['camera']}MP {'█' * int(comparison['camera_percent']/10)}{'░' * (10-int(comparison['camera_percent']/10))} {comparison['camera_percent']:.0f}%")
    print(f"   Battery: {target_phone['battery']}mAh {'█' * int(comparison['battery_percent']/10)}{'░' * (10-int(comparison['battery_percent']/10))} {comparison['battery_percent']:.0f}%")
    print(f"   RAM:     {target_phone['ram']}GB {'█' * int(comparison['ram_percent']/10)}{'░' * (10-int(comparison['ram_percent']/10))} {comparison['ram_percent']:.0f}%")
    print(f"   Storage: {target_phone['storage']}GB {'█' * int(comparison['storage_percent']/10)}{'░' * (10-int(comparison['storage_percent']/10))} {comparison['storage_percent']:.0f}%")
    print(f"   Price:   ₹{target_phone['price']:,} {'█' * int(comparison['price_percent']/10)}{'░' * (10-int(comparison['price_percent']/10))} {comparison['price_percent']:.0f}% Value\n")
    
    print("💪 STRENGTHS:")
    if strengths:
        for strength in strengths:
            print(f"   {strength}")
    else:
        print("   (No major strengths)")
    
    print("\n⚠️  WEAKNESSES:")
    if weaknesses:
        for weakness in weaknesses:
            print(f"   {weakness}")
    else:
        print("   (No major weaknesses)")
    
    print("\n" + "="*80)

def main():
    """Display feature demo"""
    print("\n" + "="*80)
    print("  🎯 SMART PHONE COMPARISON ANALYZER")
    print("  Find which phone is BEST for specific needs!")
    print("="*80)
    
    # Get budget from user
    try:
        budget = int(input("\n💰 Enter budget (₹): ₹"))
    except ValueError:
        budget = 14000
        print(f"Using default budget: ₹{budget:,}")
    
    while True:
        print("\n" + "-"*80)
        print("What would you like to see?")
        print("   1. Best phones by category (Camera, Battery, RAM, Storage, etc)")
        print("   2. Detailed analysis of a phone")
        print("   3. Change budget")
        print("   4. Exit")
        print("-"*80)
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            display_category_winners(budget)
        
        elif choice == "2":
            phone_name = input("\nEnter phone name (or part of it): ").strip()
            display_detailed_analysis(phone_name, budget)
        
        elif choice == "3":
            try:
                budget = int(input("\n💰 Enter new budget (₹): ₹"))
                print(f"✅ Budget updated to ₹{budget:,}")
            except ValueError:
                print("⚠️  Invalid input")
        
        elif choice == "4":
            print("\n👋 Thank you!")
            break
        
        else:
            print("⚠️  Invalid option")

if __name__ == "__main__":
    main()
