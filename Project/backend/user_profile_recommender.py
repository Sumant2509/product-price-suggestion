"""
User Profile Based Phone Recommendation
Recommends phones based on user type: Gamer, Photographer, Budget User, etc.
"""

from ecommerce_search import EcommercePhoneSearch
from phone_analyzer import PhoneAnalyzer

class UserProfileAnalyzer:
    """Analyze user profiles and recommend best phones"""
    
    USER_PROFILES = {
        'gamer': {
            'name': '🎮 GAMER',
            'description': 'Plays intensive games, needs high performance',
            'priorities': {
                'ram': 0.35,
                'battery': 0.25,
                'camera': 0.1,
                'storage': 0.2,
                'price': 0.1,
            },
            'min_specs': {
                'ram': 6,
                'battery': 4500,
                'storage': 128,
            }
        },
        'photographer': {
            'name': '📷 PHOTOGRAPHER',
            'description': 'Professional photography, needs best camera',
            'priorities': {
                'camera': 0.45,
                'storage': 0.25,
                'ram': 0.15,
                'battery': 0.1,
                'price': 0.05,
            },
            'min_specs': {
                'camera': 48,
                'storage': 128,
                'ram': 6,
            }
        },
        'budget': {
            'name': '💰 BUDGET CONSCIOUS',
            'description': 'Looking for best value, max specs for minimum price',
            'priorities': {
                'price': 0.4,
                'battery': 0.2,
                'ram': 0.15,
                'camera': 0.15,
                'storage': 0.1,
            },
            'min_specs': {
                'ram': 4,
                'battery': 4500,
                'storage': 64,
            }
        },
        'battery': {
            'name': '🔋 BATTERY LOVER',
            'description': 'Needs phone that lasts all day, heavy users',
            'priorities': {
                'battery': 0.45,
                'ram': 0.2,
                'camera': 0.15,
                'storage': 0.1,
                'price': 0.1,
            },
            'min_specs': {
                'battery': 5000,
                'ram': 6,
                'storage': 128,
            }
        },
        'student': {
            'name': '🎓 STUDENT',
            'description': 'Balanced needs: studies, social media, gaming',
            'priorities': {
                'price': 0.25,
                'ram': 0.25,
                'battery': 0.2,
                'camera': 0.2,
                'storage': 0.1,
            },
            'min_specs': {
                'ram': 6,
                'battery': 4500,
                'storage': 128,
            }
        },
        'professional': {
            'name': '💼 PROFESSIONAL',
            'description': 'Business work, needs reliability and performance',
            'priorities': {
                'ram': 0.3,
                'storage': 0.25,
                'battery': 0.2,
                'camera': 0.15,
                'price': 0.1,
            },
            'min_specs': {
                'ram': 8,
                'battery': 5000,
                'storage': 256,
            }
        },
        'socialite': {
            'name': '📱 SOCIAL MEDIA LOVER',
            'description': 'TikTok, Instagram, Reels - needs camera & storage',
            'priorities': {
                'camera': 0.4,
                'storage': 0.3,
                'battery': 0.15,
                'ram': 0.1,
                'price': 0.05,
            },
            'min_specs': {
                'camera': 50,
                'storage': 128,
                'battery': 5000,
            }
        },
        'minimalist': {
            'name': '🎯 MINIMALIST',
            'description': 'Just needs calls, messages, basic apps',
            'priorities': {
                'price': 0.5,
                'battery': 0.2,
                'ram': 0.15,
                'camera': 0.1,
                'storage': 0.05,
            },
            'min_specs': {
                'ram': 4,
                'battery': 4000,
                'storage': 64,
            }
        }
    }
    
    def __init__(self, phones):
        self.phones = phones
        self.analyzer = PhoneAnalyzer(phones)
    
    def get_user_profiles(self):
        """Return list of available user profiles"""
        return list(self.USER_PROFILES.keys())
    
    def recommend_for_profile(self, profile_type):
        """Get recommendation for specific user profile"""
        if profile_type.lower() not in self.USER_PROFILES:
            return None, f"❌ Unknown profile: {profile_type}"
        
        profile = self.USER_PROFILES[profile_type.lower()]
        
        # Filter by minimum specs
        min_specs = profile['min_specs']
        filtered_phones = self.phones.copy()
        
        if min_specs.get('ram'):
            filtered_phones = [p for p in filtered_phones if p.get('ram', 0) >= min_specs['ram']]
        if min_specs.get('battery'):
            filtered_phones = [p for p in filtered_phones if p.get('battery', 0) >= min_specs['battery']]
        if min_specs.get('storage'):
            filtered_phones = [p for p in filtered_phones if p.get('storage', 0) >= min_specs['storage']]
        if min_specs.get('camera'):
            filtered_phones = [p for p in filtered_phones if p.get('camera', 0) >= min_specs['camera']]
        
        if not filtered_phones:
            return None, f"⚠️  No phones meet minimum specs for {profile['name']}"
        
        # Calculate weighted score for each phone
        best_phone = None
        best_score = -1
        
        for phone in filtered_phones:
            # Normalize specs
            max_ram = max([p['ram'] for p in filtered_phones])
            max_battery = max([p['battery'] for p in filtered_phones])
            max_camera = max([p['camera'] for p in filtered_phones])
            max_storage = max([p['storage'] for p in filtered_phones])
            min_price = min([p['price'] for p in filtered_phones])
            max_price = max([p['price'] for p in filtered_phones])
            
            ram_score = phone['ram'] / max_ram if max_ram > 0 else 0
            battery_score = phone['battery'] / max_battery if max_battery > 0 else 0
            camera_score = phone['camera'] / max_camera if max_camera > 0 else 0
            storage_score = phone['storage'] / max_storage if max_storage > 0 else 0
            price_score = (max_price - phone['price']) / (max_price - min_price) if max_price != min_price else 0.5
            
            # Apply weights
            weighted_score = (
                ram_score * profile['priorities'].get('ram', 0) +
                battery_score * profile['priorities'].get('battery', 0) +
                camera_score * profile['priorities'].get('camera', 0) +
                storage_score * profile['priorities'].get('storage', 0) +
                price_score * profile['priorities'].get('price', 0)
            )
            
            if weighted_score > best_score:
                best_score = weighted_score
                best_phone = phone
        
        return {
            'profile': profile,
            'phone': best_phone,
            'score': best_score
        }, None
    
    def get_why_this_phone(self, phone, profile_type):
        """Explain why this phone is good for user profile"""
        profile = self.USER_PROFILES[profile_type.lower()]
        strengths = []
        
        # Check against profile priorities
        if profile['priorities'].get('camera', 0) > 0.3 and phone['camera'] >= 50:
            strengths.append(f"📷 Great camera ({phone['camera']}MP) - Perfect for content creation")
        
        if profile['priorities'].get('ram', 0) > 0.3 and phone['ram'] >= 8:
            strengths.append(f"⚡ High RAM ({phone['ram']}GB) - Smooth multitasking & gaming")
        
        if profile['priorities'].get('battery', 0) > 0.3 and phone['battery'] >= 5000:
            strengths.append(f"🔋 Long battery ({phone['battery']}mAh) - All-day usage")
        
        if profile['priorities'].get('storage', 0) > 0.25 and phone['storage'] >= 256:
            strengths.append(f"💾 Ample storage ({phone['storage']}GB) - Store everything")
        
        if profile['priorities'].get('price', 0) > 0.3:
            strengths.append(f"💰 Great value (₹{phone['price']:,}) - Best for budget")
        
        return strengths

def display_all_profiles():
    """Display all available user profiles"""
    profiles = UserProfileAnalyzer.USER_PROFILES
    
    print("\n" + "="*80)
    print("  👥 AVAILABLE USER PROFILES")
    print("="*80 + "\n")
    
    for i, (key, profile) in enumerate(profiles.items(), 1):
        print(f"{i}. {profile['name']}")
        print(f"   {profile['description']}\n")

def recommend_by_profile(budget):
    """Show recommendations for all profiles"""
    search = EcommercePhoneSearch()
    search.fetch_phones(use_sample=True)
    phones = search.filter_by_budget(budget)
    
    if not phones:
        print(f"❌ No phones available below ₹{budget:,}")
        return
    
    analyzer = UserProfileAnalyzer(phones)
    
    print("\n" + "="*80)
    print(f"  🎯 PHONE RECOMMENDATIONS BY USER TYPE (Budget: ₹{budget:,})")
    print("="*80 + "\n")
    
    for profile_key in analyzer.get_user_profiles():
        result, error = analyzer.recommend_for_profile(profile_key)
        
        if error:
            print(f"{analyzer.USER_PROFILES[profile_key]['name']}: {error}")
        else:
            phone = result['phone']
            profile = result['profile']
            strengths = analyzer.get_why_this_phone(phone, profile_key)
            
            print(f"{profile['name']}")
            print(f"   ✨ Best Phone: {phone['name']}")
            print(f"   💵 Price: ₹{phone['price']:,}")
            print(f"   ⭐ Rating: {phone['rating']}/5.0")
            print(f"   Match Score: {result['score']:.2%}")
            
            if strengths:
                print(f"   Why: {strengths[0]}")
            print()

def interactive_profile_recommendation():
    """Interactive mode for user profile recommendations"""
    search = EcommercePhoneSearch()
    search.fetch_phones(use_sample=True)
    
    print("\n" + "="*80)
    print("  🎯 FIND YOUR PERFECT PHONE BY USER TYPE")
    print("="*80)
    
    # Get budget
    try:
        budget = int(input("\n💰 Enter budget (₹): ₹"))
    except ValueError:
        budget = 14000
        print(f"Using default budget: ₹{budget:,}")
    
    phones = search.filter_by_budget(budget)
    
    if not phones:
        print(f"❌ No phones available below ₹{budget:,}")
        return
    
    analyzer = UserProfileAnalyzer(phones)
    
    while True:
        display_all_profiles()
        
        print("-"*80)
        choice = input("\nSelect your profile (1-8) or 0 to exit: ").strip()
        
        if choice == "0":
            print("\n👋 Thank you!")
            break
        
        try:
            index = int(choice) - 1
            profiles = list(analyzer.get_user_profiles())
            if 0 <= index < len(profiles):
                profile_key = profiles[index]
                
                result, error = analyzer.recommend_for_profile(profile_key)
                
                if error:
                    print(f"\n{error}")
                else:
                    phone = result['phone']
                    profile = result['profile']
                    strengths = analyzer.get_why_this_phone(phone, profile_key)
                    
                    print("\n" + "="*80)
                    print(f"  {profile['name']} - BEST RECOMMENDATION")
                    print("="*80 + "\n")
                    
                    print(f"📱 {phone['name']}")
                    print(f"   Brand: {phone['brand']}")
                    print(f"   Platform: {phone['platform']}")
                    print(f"   Price: ₹{phone['price']:,}")
                    print(f"   Rating: {phone['rating']}/5.0 ⭐\n")
                    
                    print("📋 SPECIFICATIONS:")
                    print(f"   • RAM: {phone['ram']}GB")
                    print(f"   • Storage: {phone['storage']}GB")
                    print(f"   • Camera: {phone['camera']}MP")
                    print(f"   • Battery: {phone['battery']}mAh\n")
                    
                    print("✅ WHY THIS PHONE:")
                    for strength in strengths:
                        print(f"   {strength}")
                    
                    print(f"\n   Match Score: {result['score']:.2%}")
                    print("="*80)
            else:
                print("⚠️  Invalid option. Please try again.")
        except ValueError:
            print("⚠️  Please enter a valid number.")

if __name__ == "__main__":
    interactive_profile_recommendation()
