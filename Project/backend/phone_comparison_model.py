import numpy as np
from phones_dataset import phones_data

class PhoneComparisonModel:
    """AI model to compare and rank phones based on user preferences"""
    
    def __init__(self):
        self.phones = phones_data
    
    def normalize_score(self, value, min_val, max_val):
        """Normalize a value between 0 and 1"""
        if max_val == min_val:
            return 0.5
        return (value - min_val) / (max_val - min_val)
    
    def filter_by_budget(self, max_budget):
        """Filter phones within budget"""
        return [p for p in self.phones if p["price"] <= max_budget]
    
    def filter_by_brand(self, phones, brands):
        """Filter phones by preferred brands"""
        if not brands or brands == ["all"]:
            return phones
        return [p for p in phones if p["brand"].lower() in [b.lower() for b in brands]]
    
    def filter_by_min_specs(self, phones, min_ram=0, min_storage=0, min_camera=0, min_battery=0):
        """Filter phones by minimum specifications"""
        filtered = []
        for p in phones:
            if (p["ram"] >= min_ram and 
                p["storage"] >= min_storage and 
                p["camera"] >= min_camera and 
                p["battery"] >= min_battery):
                filtered.append(p)
        return filtered
    
    def calculate_scores(self, phones, weights=None):
        """Calculate weighted scores for filtered phones"""
        if not phones:
            return []
        
        if weights is None:
            weights = {
                "price": 0.2,
                "camera": 0.25,
                "battery": 0.25,
                "ram": 0.15,
                "storage": 0.1,
                "rating": 0.05
            }
        
        scores = []
        
        # Get min/max for normalization
        prices = [p["price"] for p in phones]
        cameras = [p["camera"] for p in phones]
        batteries = [p["battery"] for p in phones]
        rams = [p["ram"] for p in phones]
        storages = [p["storage"] for p in phones]
        ratings = [p["rating"] for p in phones]
        
        min_price, max_price = min(prices), max(prices)
        min_camera, max_camera = min(cameras), max(cameras)
        min_battery, max_battery = min(batteries), max(batteries)
        min_ram, max_ram = min(rams), max(rams)
        min_storage, max_storage = min(storages), max(storages)
        min_rating, max_rating = min(ratings), max(ratings)
        
        # Calculate score for each phone
        for phone in phones:
            # Price: lower is better (invert)
            price_score = 1 - self.normalize_score(phone["price"], min_price, max_price)
            
            # Camera: higher is better
            camera_score = self.normalize_score(phone["camera"], min_camera, max_camera)
            
            # Battery: higher is better
            battery_score = self.normalize_score(phone["battery"], min_battery, max_battery)
            
            # RAM: higher is better
            ram_score = self.normalize_score(phone["ram"], min_ram, max_ram)
            
            # Storage: higher is better
            storage_score = self.normalize_score(phone["storage"], min_storage, max_storage)
            
            # Rating: higher is better
            rating_score = self.normalize_score(phone["rating"], min_rating, max_rating)
            
            # Weighted total
            total_score = (
                price_score * weights["price"] +
                camera_score * weights["camera"] +
                battery_score * weights["battery"] +
                ram_score * weights["ram"] +
                storage_score * weights["storage"] +
                rating_score * weights["rating"]
            )
            
            scores.append({
                "phone": phone,
                "total_score": total_score,
                "price_score": price_score,
                "camera_score": camera_score,
                "battery_score": battery_score,
                "ram_score": ram_score,
                "storage_score": storage_score,
                "rating_score": rating_score
            })
        
        return scores
    
    def rank_phones(self, phones, weights=None):
        """Rank phones by score (highest first)"""
        scores = self.calculate_scores(phones, weights)
        ranked = sorted(scores, key=lambda x: x["total_score"], reverse=True)
        return ranked
    
    def get_best_phone(self, phones, weights=None):
        """Get single best phone"""
        ranked = self.rank_phones(phones, weights)
        return ranked[0] if ranked else None
    
    def get_recommendation(self, budget, brands=None, min_ram=0, min_storage=0, 
                          min_camera=0, min_battery=0, weights=None):
        """Get best phone recommendation based on user preferences"""
        
        # Filter by budget
        filtered = self.filter_by_budget(budget)
        if not filtered:
            return None, "No phones available within your budget"
        
        # Filter by brand
        filtered = self.filter_by_brand(filtered, brands)
        if not filtered:
            return None, "No phones found for selected brands within budget"
        
        # Filter by minimum specs
        filtered = self.filter_by_min_specs(filtered, min_ram, min_storage, min_camera, min_battery)
        if not filtered:
            return None, "No phones meet your minimum specifications"
        
        # Get best phone
        best = self.get_best_phone(filtered, weights)
        return best, None
