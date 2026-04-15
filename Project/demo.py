"""
Demo script showing how the interactive recommendation system works
with example user inputs
"""

from phone_comparison_model import PhoneComparisonModel

def demo_scenario_1():
    """Demo: Budget user looking for best value phone under ₹40,000"""
    print("\n" + "=" * 60)
    print("DEMO 1: Budget-Conscious User")
    print("=" * 60)
    print("Input: Budget=₹40,000, No brand preference, Min RAM=6GB, Priority=Best Value")
    print()
    
    model = PhoneComparisonModel()
    result, error = model.get_recommendation(
        budget=40000,
        brands=None,
        min_ram=6,
        min_storage=0,
        min_camera=0,
        min_battery=0,
        weights={"price": 0.5, "camera": 0.15, "battery": 0.15, "ram": 0.1, "storage": 0.1, "rating": 0.0}
    )
    
    if error:
        print(f"❌ {error}")
    elif result:
        phone = result["phone"]
        print(f"✨ BEST RECOMMENDATION: {phone['name']} by {phone['brand']}")
        print(f"   Price: ₹{phone['price']:,}")
        print(f"   RAM: {phone['ram']}GB | Storage: {phone['storage']}GB")
        print(f"   Camera: {phone['camera']}MP | Battery: {phone['battery']}mAh")
        print(f"   Match Score: {result['total_score']:.2%}")

def demo_scenario_2():
    """Demo: Photography enthusiast with higher budget"""
    print("\n" + "=" * 60)
    print("DEMO 2: Camera Enthusiast")
    print("=" * 60)
    print("Input: Budget=₹70,000, Brands=Samsung/Google, Min Camera=50MP, Priority=Camera")
    print()
    
    model = PhoneComparisonModel()
    result, error = model.get_recommendation(
        budget=70000,
        brands=["Samsung", "Google"],
        min_ram=8,
        min_storage=0,
        min_camera=50,
        min_battery=0,
        weights={"price": 0.1, "camera": 0.5, "battery": 0.15, "ram": 0.1, "storage": 0.1, "rating": 0.05}
    )
    
    if error:
        print(f"❌ {error}")
    elif result:
        phone = result["phone"]
        print(f"✨ BEST RECOMMENDATION: {phone['name']} by {phone['brand']}")
        print(f"   Price: ₹{phone['price']:,}")
        print(f"   RAM: {phone['ram']}GB | Storage: {phone['storage']}GB")
        print(f"   Camera: {phone['camera']}MP | Battery: {phone['battery']}mAh")
        print(f"   Match Score: {result['total_score']:.2%}")

def demo_scenario_3():
    """Demo: Battery life seeker"""
    print("\n" + "=" * 60)
    print("DEMO 3: Battery Life Seeker")
    print("=" * 60)
    print("Input: Budget=₹60,000, Min Battery=5000mAh, Priority=Battery Life")
    print()
    
    model = PhoneComparisonModel()
    result, error = model.get_recommendation(
        budget=60000,
        brands=None,
        min_ram=0,
        min_storage=0,
        min_camera=0,
        min_battery=5000,
        weights={"price": 0.1, "camera": 0.15, "battery": 0.5, "ram": 0.1, "storage": 0.1, "rating": 0.05}
    )
    
    if error:
        print(f"❌ {error}")
    elif result:
        phone = result["phone"]
        print(f"✨ BEST RECOMMENDATION: {phone['name']} by {phone['brand']}")
        print(f"   Price: ₹{phone['price']:,}")
        print(f"   RAM: {phone['ram']}GB | Storage: {phone['storage']}GB")
        print(f"   Camera: {phone['camera']}MP | Battery: {phone['battery']}mAh")
        print(f"   Match Score: {result['total_score']:.2%}")

def demo_scenario_4():
    """Demo: Premium user wanting best overall phone"""
    print("\n" + "=" * 60)
    print("DEMO 4: Premium User - Best Overall")
    print("=" * 60)
    print("Input: Budget=₹85,000, Min specs: 8GB RAM, Priority=Balanced")
    print()
    
    model = PhoneComparisonModel()
    result, error = model.get_recommendation(
        budget=85000,
        brands=None,
        min_ram=8,
        min_storage=256,
        min_camera=0,
        min_battery=0,
        weights={"price": 0.2, "camera": 0.25, "battery": 0.25, "ram": 0.15, "storage": 0.1, "rating": 0.05}
    )
    
    if error:
        print(f"❌ {error}")
    elif result:
        phone = result["phone"]
        print(f"✨ BEST RECOMMENDATION: {phone['name']} by {phone['brand']}")
        print(f"   Price: ₹{phone['price']:,}")
        print(f"   RAM: {phone['ram']}GB | Storage: {phone['storage']}GB")
        print(f"   Camera: {phone['camera']}MP | Battery: {phone['battery']}mAh")
        print(f"   Rating: {phone['rating']}/5.0")
        print(f"   Match Score: {result['total_score']:.2%}")

def main():
    print("\n" + "=" * 60)
    print("📱 PHONE RECOMMENDATION AI - DEMO SCENARIOS")
    print("=" * 60)
    
    demo_scenario_1()
    demo_scenario_2()
    demo_scenario_3()
    demo_scenario_4()
    
    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETE")
    print("=" * 60)
    print("\n💡 To use interactive mode, run: python interactive.py")

if __name__ == "__main__":
    main()
