from phone_comparison_model import PhoneComparisonModel
from phones_dataset import phones_data

def get_user_input():
    """Get user preferences interactively"""
    print("\n" + "=" * 60)
    print("🎯 PHONE RECOMMENDATION SYSTEM")
    print("=" * 60)
    print()
    
    # Budget input
    while True:
        try:
            budget = float(input("💰 Enter your budget (max price in INR): ₹"))
            if budget <= 0:
                print("⚠️  Budget must be greater than 0")
                continue
            break
        except ValueError:
            print("⚠️  Please enter a valid number")
    
    # Brand preference
    print("\n📱 Available brands:")
    brands = set(p["brand"] for p in phones_data)
    for i, brand in enumerate(sorted(brands), 1):
        print(f"   {i}. {brand}")
    print("   0. All brands")
    
    brand_choice = input("\nEnter brand numbers (comma-separated) or 0 for all: ").strip()
    
    selected_brands = None
    if brand_choice != "0":
        try:
            indices = [int(x.strip()) - 1 for x in brand_choice.split(",")]
            brand_list = sorted(brands)
            selected_brands = [brand_list[i] for i in indices if 0 <= i < len(brand_list)]
        except (ValueError, IndexError):
            selected_brands = None
    
    # Minimum specifications
    print("\n⚙️  Set minimum specifications (press Enter to skip):")
    
    min_ram = 0
    ram_input = input("   Minimum RAM (GB) [default: any]: ").strip()
    if ram_input:
        try:
            min_ram = int(ram_input)
        except ValueError:
            min_ram = 0
    
    min_storage = 0
    storage_input = input("   Minimum Storage (GB) [default: any]: ").strip()
    if storage_input:
        try:
            min_storage = int(storage_input)
        except ValueError:
            min_storage = 0
    
    min_camera = 0
    camera_input = input("   Minimum Camera (MP) [default: any]: ").strip()
    if camera_input:
        try:
            min_camera = int(camera_input)
        except ValueError:
            min_camera = 0
    
    min_battery = 0
    battery_input = input("   Minimum Battery (mAh) [default: any]: ").strip()
    if battery_input:
        try:
            min_battery = int(battery_input)
        except ValueError:
            min_battery = 0
    
    # Priorities
    print("\n📊 What's most important to you?")
    print("   1. Price (cheapest)")
    print("   2. Camera (best photos)")
    print("   3. Battery (long lasting)")
    print("   4. Performance (more RAM)")
    print("   5. Storage (more space)")
    print("   6. Balanced")
    
    priority = input("Choose priority (1-6, default 6): ").strip()
    
    weights = {
        "price": 0.2,
        "camera": 0.25,
        "battery": 0.25,
        "ram": 0.15,
        "storage": 0.1,
        "rating": 0.05
    }
    
    if priority == "1":
        weights = {"price": 0.5, "camera": 0.15, "battery": 0.15, "ram": 0.1, "storage": 0.1, "rating": 0.0}
    elif priority == "2":
        weights = {"price": 0.1, "camera": 0.5, "battery": 0.15, "ram": 0.1, "storage": 0.1, "rating": 0.05}
    elif priority == "3":
        weights = {"price": 0.1, "camera": 0.15, "battery": 0.5, "ram": 0.1, "storage": 0.1, "rating": 0.05}
    elif priority == "4":
        weights = {"price": 0.1, "camera": 0.15, "battery": 0.15, "ram": 0.5, "storage": 0.1, "rating": 0.0}
    elif priority == "5":
        weights = {"price": 0.1, "camera": 0.15, "battery": 0.15, "ram": 0.1, "storage": 0.5, "rating": 0.0}
    
    return {
        "budget": budget,
        "brands": selected_brands,
        "min_ram": min_ram,
        "min_storage": min_storage,
        "min_camera": min_camera,
        "min_battery": min_battery,
        "weights": weights
    }

def display_recommendation(result, error):
    """Display the recommendation"""
    print("\n" + "=" * 60)
    print("✨ RECOMMENDATION RESULTS")
    print("=" * 60)
    print()
    
    if error:
        print(f"❌ {error}")
        return
    
    if not result:
        print("❌ No suitable phone found")
        return
    
    phone = result["phone"]
    score = result["total_score"]
    
    print(f"🏆 Best Phone: {phone['name']} by {phone['brand']}")
    print(f"   Price: ₹{phone['price']:,}")
    print(f"   Score: {score:.2%}")
    print()
    print("📋 Specifications:")
    print(f"   • RAM: {phone['ram']}GB")
    print(f"   • Storage: {phone['storage']}GB")
    print(f"   • Camera: {phone['camera']}MP")
    print(f"   • Battery: {phone['battery']}mAh")
    print(f"   • Rating: {phone['rating']}/5.0 ⭐")
    print()
    
    # Show pros/cons
    print("✅ Strengths:")
    if result["camera_score"] > 0.6:
        print(f"   • Excellent camera ({phone['camera']}MP)")
    if result["battery_score"] > 0.6:
        print(f"   • Great battery life ({phone['battery']}mAh)")
    if result["price_score"] > 0.6:
        print(f"   • Affordable price (₹{phone['price']:,})")
    if result["ram_score"] > 0.6:
        print(f"   • Good RAM ({phone['ram']}GB)")
    if result["storage_score"] > 0.6:
        print(f"   • Plenty of storage ({phone['storage']}GB)")
    
    print()
    print("⚠️  Areas to consider:")
    if result["camera_score"] < 0.5:
        print(f"   • Average camera ({phone['camera']}MP)")
    if result["battery_score"] < 0.5:
        print(f"   • Moderate battery ({phone['battery']}mAh)")
    if result["price_score"] < 0.5:
        print(f"   • Higher price (₹{phone['price']:,})")
    if result["ram_score"] < 0.5:
        print(f"   • Limited RAM ({phone['ram']}GB)")
    
    print()

def main():
    model = PhoneComparisonModel()
    
    while True:
        user_prefs = get_user_input()
        
        # Get recommendation
        result, error = model.get_recommendation(
            budget=user_prefs["budget"],
            brands=user_prefs["brands"],
            min_ram=user_prefs["min_ram"],
            min_storage=user_prefs["min_storage"],
            min_camera=user_prefs["min_camera"],
            min_battery=user_prefs["min_battery"],
            weights=user_prefs["weights"]
        )
        
        display_recommendation(result, error)
        
        # Ask if user wants to try again
        again = input("🔄 Try another search? (yes/no): ").strip().lower()
        if again not in ["yes", "y"]:
            print("\n👋 Thank you for using Phone Recommendation System!")
            break

if __name__ == "__main__":
    main()
