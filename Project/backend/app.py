"""
Flask Backend API for Phone Recommendation System
Connects all recommendation models and serves data to frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from ecommerce_search import EcommercePhoneSearch
from phone_analyzer import PhoneAnalyzer
from user_profile_recommender import UserProfileAnalyzer

app = Flask('phone_recommendation')
CORS(app)

# Initialize services
search_service = EcommercePhoneSearch()
search_service.fetch_phones(use_sample=True)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': '✅ API is running', 'version': '1.0'})

@app.route('/api/phones/budget', methods=['GET'])
def get_phones_by_budget():
    """Get all phones within budget"""
    budget = request.args.get('budget', 14000, type=int)
    phones = search_service.filter_by_budget(budget)
    return jsonify({
        'budget': budget,
        'count': len(phones),
        'phones': phones
    })

@app.route('/api/phones/best', methods=['GET'])
def get_best_phone_in_budget():
    """Get best phone within budget"""
    budget = request.args.get('budget', 14000, type=int)
    best, error = search_service.get_best_in_budget(budget)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify({
        'budget': budget,
        'phone': best['phone'],
        'score': best['total_score'],
        'match': f"{best['total_score']:.2%}"
    })

@app.route('/api/phones/platform/<platform>', methods=['GET'])
def get_phones_by_platform(platform):
    """Get phones from specific platform"""
    budget = request.args.get('budget', None, type=int)
    phones = search_service.filter_by_platform(platform)
    
    if budget:
        phones = [p for p in phones if p['price'] <= budget]
    
    return jsonify({
        'platform': platform,
        'budget': budget,
        'count': len(phones),
        'phones': phones
    })

@app.route('/api/phones/brand/<brand>', methods=['GET'])
def get_phones_by_brand(brand):
    """Get phones by brand"""
    budget = request.args.get('budget', None, type=int)
    phones = search_service.search_by_brand(brand, budget)
    
    return jsonify({
        'brand': brand,
        'budget': budget,
        'count': len(phones),
        'phones': phones
    })

@app.route('/api/phones/compare', methods=['GET'])
def compare_platforms():
    """Compare best phones from each platform"""
    budget = request.args.get('budget', 14000, type=int)
    results = search_service.compare_platforms(budget)
    
    comparison = {}
    for platform, result in results.items():
        if result:
            comparison[platform] = {
                'phone': result['phone'],
                'score': result['total_score']
            }
    
    return jsonify({
        'budget': budget,
        'comparison': comparison
    })

@app.route('/api/analyzer/categories', methods=['GET'])
def get_category_winners():
    """Get best phones in each category"""
    budget = request.args.get('budget', 14000, type=int)
    phones = search_service.filter_by_budget(budget)
    
    if not phones:
        return jsonify({'error': f'No phones below ₹{budget}'}), 404
    
    analyzer = PhoneAnalyzer(phones)
    comparisons = analyzer.get_all_comparisons()
    
    result = {}
    for category, phone in comparisons.items():
        result[category] = phone
    
    return jsonify({
        'budget': budget,
        'categories': result
    })

@app.route('/api/analyzer/phone/<phone_name>', methods=['GET'])
def analyze_phone(phone_name):
    """Get detailed analysis of a phone"""
    budget = request.args.get('budget', 14000, type=int)
    phones = search_service.filter_by_budget(budget)
    
    # Find phone
    target_phone = None
    for p in phones:
        if phone_name.lower() in p['name'].lower():
            target_phone = p
            break
    
    if not target_phone:
        return jsonify({'error': f'Phone not found: {phone_name}'}), 404
    
    analyzer = PhoneAnalyzer(phones)
    comparison = analyzer.get_spec_comparison(target_phone)
    strengths, weaknesses = analyzer.get_strengths_weaknesses(target_phone)
    
    return jsonify({
        'phone': target_phone,
        'comparison': comparison,
        'strengths': strengths,
        'weaknesses': weaknesses
    })

@app.route('/api/profiles/list', methods=['GET'])
def get_user_profiles():
    """Get list of available user profiles"""
    profiles = []
    for key, profile in UserProfileAnalyzer.USER_PROFILES.items():
        profiles.append({
            'key': key,
            'name': profile['name'],
            'description': profile['description']
        })
    
    return jsonify({'profiles': profiles})

@app.route('/api/profiles/recommend', methods=['GET'])
def recommend_by_profile():
    """Get recommendation for user profile"""
    profile_type = request.args.get('profile', 'gamer')
    budget = request.args.get('budget', 14000, type=int)
    
    phones = search_service.filter_by_budget(budget)
    
    if not phones:
        return jsonify({'error': f'No phones below ₹{budget}'}), 404
    
    analyzer = UserProfileAnalyzer(phones)
    result, error = analyzer.recommend_for_profile(profile_type)
    
    if error:
        return jsonify({'error': error}), 404
    
    phone = result['phone']
    profile = result['profile']
    strengths = analyzer.get_why_this_phone(phone, profile_type)
    
    return jsonify({
        'profile': profile,
        'phone': phone,
        'score': result['score'],
        'strengths': strengths
    })

@app.route('/api/discounts/deals', methods=['GET'])
def get_daily_deals():
    """Get daily deals (budget phones)"""
    deals = search_service.get_deals_of_day()
    
    return jsonify({
        'count': len(deals),
        'deals': deals
    })

@app.route('/api/search', methods=['GET'])
def search_phones():
    """Advanced search"""
    budget = request.args.get('budget', None, type=int)
    brand = request.args.get('brand', None)
    min_ram = request.args.get('min_ram', 0, type=int)
    min_battery = request.args.get('min_battery', 0, type=int)
    min_camera = request.args.get('min_camera', 0, type=int)
    
    phones = search_service.all_phones
    
    if budget:
        phones = [p for p in phones if p['price'] <= budget]
    if brand:
        phones = [p for p in phones if brand.lower() in p['brand'].lower()]
    if min_ram:
        phones = [p for p in phones if p['ram'] >= min_ram]
    if min_battery:
        phones = [p for p in phones if p['battery'] >= min_battery]
    if min_camera:
        phones = [p for p in phones if p['camera'] >= min_camera]
    
    return jsonify({
        'filters': {
            'budget': budget,
            'brand': brand,
            'min_ram': min_ram,
            'min_battery': min_battery,
            'min_camera': min_camera
        },
        'count': len(phones),
        'phones': phones
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    all_phones = search_service.all_phones
    
    stats = {
        'total_phones': len(all_phones),
        'avg_price': sum(p['price'] for p in all_phones) / len(all_phones),
        'price_range': {
            'min': min(p['price'] for p in all_phones),
            'max': max(p['price'] for p in all_phones)
        },
        'avg_camera': sum(p['camera'] for p in all_phones) / len(all_phones),
        'avg_battery': sum(p['battery'] for p in all_phones) / len(all_phones),
        'avg_ram': sum(p['ram'] for p in all_phones) / len(all_phones),
        'brands': len(set(p['brand'] for p in all_phones)),
        'platforms': len(set(p['platform'] for p in all_phones))
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🚀 PHONE RECOMMENDATION API SERVER")
    print("="*70)
    print("\n✅ API running on: http://localhost:5000")
    print("\n📚 Available Endpoints:")
    print("   GET  /api/health")
    print("   GET  /api/phones/budget?budget=14000")
    print("   GET  /api/phones/best?budget=14000")
    print("   GET  /api/phones/platform/<platform>")
    print("   GET  /api/phones/brand/<brand>")
    print("   GET  /api/phones/compare?budget=14000")
    print("   GET  /api/analyzer/categories?budget=14000")
    print("   GET  /api/analyzer/phone/<phone_name>?budget=14000")
    print("   GET  /api/profiles/list")
    print("   GET  /api/profiles/recommend?profile=gamer&budget=14000")
    print("   GET  /api/discounts/deals")
    print("   GET  /api/search?budget=14000&brand=Samsung")
    print("   GET  /api/stats")
    print("\n" + "="*70 + "\n")
    
    app.run(debug=True, port=5000)
