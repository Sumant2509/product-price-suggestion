"""
Demo of phone analyzer feature
Shows best phones by category and detailed analysis
"""

from phone_analyzer import PhoneAnalyzer, display_category_winners, display_detailed_analysis
from ecommerce_search import EcommercePhoneSearch
from flask import Flask

print("\n" + "="*80)
print("  📊 PHONE ANALYZER - DEMO")
print("="*80)

# Initialize
search = EcommercePhoneSearch()
search.fetch_phones(use_sample=True)

app = Flask('phone_recommendation')

# Demo 1: Show best phones by category in ₹14,000 budget
print("\n" + "="*80)
print("  DEMO 1: Best Phones in Each Category (₹14,000 Budget)")
print("="*80)

phones_14k = search.filter_by_budget(14000)
analyzer_14k = PhoneAnalyzer(phones_14k)
comparisons_14k = analyzer_14k.get_all_comparisons()

for category, phone in comparisons_14k.items():
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
    
    print(f"\n{category} {spec}")
    print(f"   {phone['name']} by {phone['brand']}")
    print(f"   Price: ₹{phone['price']:,} | Platform: {phone['platform']}")

# Demo 2: Detailed analysis of Infinix Note 30
print("\n" + "="*80)
print("  DEMO 2: Detailed Analysis - Infinix Note 30")
print("="*80)

infinix = None
for phone in phones_14k:
    if 'infinix' in phone['name'].lower():
        infinix = phone
        break

if infinix:
    comparison = analyzer_14k.get_spec_comparison(infinix)
    strengths, weaknesses = analyzer_14k.get_strengths_weaknesses(infinix)
    
    print(f"\n📱 {infinix['name']}")
    print(f"   Brand: {infinix['brand']}")
    print(f"   Platform: {infinix['platform']}")
    print(f"   Price: ₹{infinix['price']:,}")
    print(f"   Rating: {infinix['rating']}/5.0 ⭐\n")
    
    print("📊 PERFORMANCE COMPARISON:")
    print(f"   Camera:  {infinix['camera']:3d}MP  {'█' * int(comparison['camera_percent']/10)}{'░' * (10-int(comparison['camera_percent']/10))} {comparison['camera_percent']:5.0f}%")
    print(f"   Battery: {infinix['battery']:4d}mAh {'█' * int(comparison['battery_percent']/10)}{'░' * (10-int(comparison['battery_percent']/10))} {comparison['battery_percent']:5.0f}%")
    print(f"   RAM:     {infinix['ram']:2d}GB   {'█' * int(comparison['ram_percent']/10)}{'░' * (10-int(comparison['ram_percent']/10))} {comparison['ram_percent']:5.0f}%")
    print(f"   Storage: {infinix['storage']:3d}GB  {'█' * int(comparison['storage_percent']/10)}{'░' * (10-int(comparison['storage_percent']/10))} {comparison['storage_percent']:5.0f}%")
    print(f"   Value:   {'█' * int(comparison['price_percent']/10)}{'░' * (10-int(comparison['price_percent']/10))} {comparison['price_percent']:5.0f}%\n")
    
    print("💪 STRENGTHS:")
    for strength in strengths:
        print(f"   {strength}")
    
    print("\n⚠️  WEAKNESSES:")
    if weaknesses:
        for weakness in weaknesses:
            print(f"   {weakness}")
    else:
        print("   None - This is a solid phone!")

# Demo 3: Compare top 3 phones
print("\n" + "="*80)
print("  DEMO 3: Top 3 Phones Comparison in ₹20,000 Budget")
print("="*80)

phones_20k = search.filter_by_budget(20000)
analyzer_20k = PhoneAnalyzer(phones_20k)

# Sort by price and show top 3 after recommended
top_phones = sorted(phones_20k, key=lambda p: analyzer_20k.get_spec_comparison(p)['camera_percent'] + 
                                                 analyzer_20k.get_spec_comparison(p)['battery_percent'] + 
                                                 analyzer_20k.get_spec_comparison(p)['ram_percent'], reverse=True)[:3]

for i, phone in enumerate(top_phones, 1):
    comp = analyzer_20k.get_spec_comparison(phone)
    strengths, weaknesses = analyzer_20k.get_strengths_weaknesses(phone)
    
    print(f"\n{i}. {phone['name']}")
    print(f"   {phone['brand']} | {phone['platform']} | ₹{phone['price']:,}")
    print(f"   Specs: {phone['ram']}GB RAM | {phone['storage']}GB Storage | {phone['camera']}MP Cam | {phone['battery']}mAh Battery")
    print(f"   Rating: {phone['rating']}/5.0")
    if strengths:
        strength_list = ", ".join([s.replace('💪 ', '').replace('💰 ', '') for s in strengths])
        print(f"   Strengths: {strength_list}")

print("\n" + "="*80)
print("✅ DEMO COMPLETE")
print("="*80)
print("\n💡 To use interactive mode, run: python phone_analyzer.py")
