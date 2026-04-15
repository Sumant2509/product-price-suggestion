"""
Test budget phones in ₹14,000 range
"""

from ecommerce_search import EcommercePhoneSearch

search = EcommercePhoneSearch()
search.fetch_phones(use_sample=True)

print("="*70)
print("  PHONES AVAILABLE IN ₹14,000 BUDGET")
print("="*70)

phones = search.filter_by_budget(14000)
print(f"\nTotal phones available: {len(phones)}\n")

for i, phone in enumerate(phones, 1):
    print(f"{i}. {phone['name']}")
    print(f"   Brand: {phone['brand']} | Platform: {phone['platform']}")
    print(f"   Price: ₹{phone['price']:,}")
    print(f"   Specs: {phone['ram']}GB RAM | {phone['storage']}GB Storage | {phone['camera']}MP Camera | {phone['battery']}mAh Battery")
    print(f"   Rating: {phone['rating']}/5.0\n")

print("-"*70)
print("BEST PHONE IN ₹14,000 BUDGET\n")
best, error = search.get_best_in_budget(14000)
if best:
    phone = best['phone']
    print(f"✨ WINNER: {phone['name']}")
    print(f"   Price: ₹{phone['price']:,}")
    print(f"   Brand: {phone['brand']}")
    print(f"   Platform: {phone['platform']}")
    print(f"   Score: {best['total_score']:.2%}")
else:
    print(error)

print("\n" + "="*70)
print("  COMPARISON: DIFERENTES BUDGET RANGES")
print("="*70)

for budget in [10000, 14000, 20000, 30000]:
    count = len(search.filter_by_budget(budget))
    best, _ = search.get_best_in_budget(budget)
    print(f"\n₹{budget:,}: {count} phones available", end="")
    if best:
        print(f" | Best: {best['phone']['name']} (₹{best['phone']['price']:,})")
    else:
        print()
