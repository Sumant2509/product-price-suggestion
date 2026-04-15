"""
Demo: Phone Recommendations by User Type
Shows which phone is best for Gamer, Photographer, Student, etc.
"""

from user_profile_recommender import UserProfileAnalyzer
from ecommerce_search import EcommercePhoneSearch

# Initialize
search = EcommercePhoneSearch()
search.fetch_phones(use_sample=True)
phones_14k = search.filter_by_budget(14000)

analyzer = UserProfileAnalyzer(phones_14k)

print("\n" + "="*80)
print("  👥 PHONE RECOMMENDATIONS BY USER TYPE")
print("="*80)

# Show all profiles and their recommendations
profiles_to_show = ['gamer', 'photographer', 'budget', 'battery', 'student', 'professional', 'socialite', 'minimalist']

for profile_key in profiles_to_show:
    result, error = analyzer.recommend_for_profile(profile_key)
    
    profile = analyzer.USER_PROFILES[profile_key]
    
    print(f"\n{profile['name']}")
    print(f"   📌 {profile['description']}\n")
    
    if error:
        print(f"   {error}")
    else:
        phone = result['phone']
        strengths = analyzer.get_why_this_phone(phone, profile_key)
        
        print(f"   ✨ Best Phone: {phone['name']}")
        print(f"   💵 Price: ₹{phone['price']:,}")
        print(f"   ⭐ Rating: {phone['rating']}/5.0")
        print(f"   Specs: {phone['ram']}GB RAM • {phone['storage']}GB Storage • {phone['camera']}MP Cam • {phone['battery']}mAh Battery")
        print(f"   💯 Match Score: {result['score']:.2%}\n")
        
        if strengths:
            print("   Why this phone:")
            for strength in strengths:
                print(f"   • {strength}")

print("\n" + "="*80)
print("✅ DEMO COMPLETE - All User Types Covered!")
print("="*80)
print("\n💡 Run interactive mode: python user_profile_recommender.py")
