from phone_comparison_model import PhoneComparisonModel

def main():
    print("=" * 60)
    print("PHONE COMPARISON AI MODEL")
    print("=" * 60)
    print()
    
    model = PhoneComparisonModel()
    
    # Default weights (balanced)
    print("📊 RANKED LIST (Default Weights):\n")
    ranked = model.rank_phones()
    for i, result in enumerate(ranked, 1):
        phone = result["phone"]
        score = result["total_score"]
        print(f"{i}. {phone['name']} ({phone['brand']})")
        print(f"   Price: ${phone['price']} | Camera: {phone['camera']}MP | Battery: {phone['battery']}mAh")
        print(f"   Overall Score: {score:.2%}")
        print()
    
    print("-" * 60)
    print()
    
    # Best phone with pros/cons
    print("🏆 BEST PHONE RECOMMENDATION:\n")
    best = ranked[0]
    phone = best["phone"]
    print(f"Winner: {phone['name']} by {phone['brand']}")
    print(f"Price: ${phone['price']}")
    print(f"Score: {best['total_score']:.2%}")
    print()
    
    pros_cons = model.get_pros_cons(ranked)
    print("✅ Pros:")
    for pro in pros_cons["pros"]:
        print(f"   • {pro}")
    print()
    
    print("❌ Cons:")
    for con in pros_cons["cons"]:
        print(f"   • {con}")
    
    print()
    print("-" * 60)
    print()
    
    # Custom weights (budget-focused)
    print("💰 BUDGET-FOCUSED RANKING:\n")
    budget_weights = {
        "price": 0.5,  # Price is most important
        "camera": 0.15,
        "battery": 0.15,
        "specs": 0.1,
        "rating": 0.1
    }
    
    budget_ranked = model.rank_phones(budget_weights)
    for i, result in enumerate(budget_ranked[:3], 1):  # Show top 3
        phone = result["phone"]
        print(f"{i}. {phone['name']} - ${phone['price']}")
    
    print()
    print("-" * 60)
    print()
    
    # Camera-focused
    print("📸 CAMERA-FOCUSED RANKING:\n")
    camera_weights = {
        "price": 0.1,
        "camera": 0.6,  # Camera is most important
        "battery": 0.1,
        "specs": 0.1,
        "rating": 0.1
    }
    
    camera_ranked = model.rank_phones(camera_weights)
    for i, result in enumerate(camera_ranked[:3], 1):  # Show top 3
        phone = result["phone"]
        print(f"{i}. {phone['name']} - {phone['camera']}MP")

if __name__ == "__main__":
    main()
