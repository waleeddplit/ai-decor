"""
GeoFinderAgent: Find local décor stores and galleries
Uses Google Maps API for location-based search
"""

import os
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()


class GeoFinderAgent:
    """
    Finds nearby art galleries and décor stores
    - Google Maps API integration
    - Distance calculation
    - Store availability checking
    """

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")

        if self.api_key and self.api_key != "your_google_maps_api_key":
            try:
                import googlemaps

                self.gmaps = googlemaps.Client(key=self.api_key)
                print("GeoFinderAgent initialized with Google Maps API")
            except (ImportError, ValueError) as e:
                print(f"Warning: Could not initialize Google Maps client: {e}. Using mock data.")
                self.gmaps = None
        else:
            print("Warning: GOOGLE_MAPS_API_KEY not set. Using mock data.")
            self.gmaps = None

    async def find_nearby_stores(
        self,
        latitude: float,
        longitude: float,
        radius: int = 10000,  # 10km default
        store_type: str = "art_gallery",
    ) -> List[Dict[str, Any]]:
        """
        Find nearby art stores and galleries

        Args:
            latitude: User's latitude
            longitude: User's longitude
            radius: Search radius in meters
            store_type: Type of store (art_gallery, home_goods_store, furniture_store)

        Returns:
            List of nearby stores with details
        """
        if self.gmaps:
            try:
                return await self._search_real_stores(
                    latitude, longitude, radius, store_type
                )
            except Exception as e:
                print(f"Error searching stores: {e}")
                return self._get_mock_stores(latitude, longitude)
        else:
            return self._get_mock_stores(latitude, longitude)

    async def _search_real_stores(
        self, lat: float, lng: float, radius: int, store_type: str
    ) -> List[Dict[str, Any]]:
        """Search stores using Google Maps API"""
        try:
            location = (lat, lng)

            # Search for places
            places_result = self.gmaps.places_nearby(
                location=location, radius=radius, type=store_type
            )

            stores = []
            for place in places_result.get("results", [])[:10]:  # Limit to 10 results
                # Get place details
                place_details = self.gmaps.place(place["place_id"])["result"]

                stores.append(
                    {
                        "id": place["place_id"],
                        "name": place.get("name", "Unknown"),
                        "address": place.get("vicinity", "Address not available"),
                        "location": {
                            "lat": place["geometry"]["location"]["lat"],
                            "lng": place["geometry"]["location"]["lng"],
                        },
                        "rating": place.get("rating", 0),
                        "distance": self._calculate_distance(
                            lat, lng, place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"]
                        ),
                        "phone": place_details.get("formatted_phone_number", "N/A"),
                        "website": place_details.get("website", "N/A"),
                        "opening_hours": place.get("opening_hours", {}).get(
                            "weekday_text", []
                        ),
                        "is_open": place.get("opening_hours", {}).get("open_now", None),
                    }
                )

            return sorted(stores, key=lambda x: x["distance"])
        except Exception as e:
            print(f"Error in Google Maps API call: {e}")
            return self._get_mock_stores(lat, lng)

    def _get_mock_stores(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        """Return mock store data"""
        stores = [
            {
                "id": "mock_1",
                "name": "Gallery Downtown",
                "address": "123 Art Street, Downtown",
                "location": {"lat": lat + 0.01, "lng": lng + 0.01},
                "rating": 4.5,
                "distance": 1.2,
                "phone": "(555) 123-4567",
                "website": "https://gallerydowntown.com",
                "opening_hours": [
                    "Monday: 10:00 AM – 6:00 PM",
                    "Tuesday: 10:00 AM – 6:00 PM",
                    "Wednesday: 10:00 AM – 6:00 PM",
                    "Thursday: 10:00 AM – 8:00 PM",
                    "Friday: 10:00 AM – 8:00 PM",
                    "Saturday: 11:00 AM – 7:00 PM",
                    "Sunday: 12:00 PM – 5:00 PM",
                ],
                "is_open": True,
            },
            {
                "id": "mock_2",
                "name": "Art House",
                "address": "456 Creative Ave, Arts District",
                "location": {"lat": lat + 0.02, "lng": lng - 0.01},
                "rating": 4.7,
                "distance": 2.5,
                "phone": "(555) 234-5678",
                "website": "https://arthouse.com",
                "opening_hours": [
                    "Monday: Closed",
                    "Tuesday: 11:00 AM – 7:00 PM",
                    "Wednesday: 11:00 AM – 7:00 PM",
                    "Thursday: 11:00 AM – 7:00 PM",
                    "Friday: 11:00 AM – 9:00 PM",
                    "Saturday: 10:00 AM – 9:00 PM",
                    "Sunday: 12:00 PM – 6:00 PM",
                ],
                "is_open": True,
            },
            {
                "id": "mock_3",
                "name": "Modern Décor Co.",
                "address": "789 Design Blvd, Uptown",
                "location": {"lat": lat - 0.015, "lng": lng + 0.02},
                "rating": 4.3,
                "distance": 3.8,
                "phone": "(555) 345-6789",
                "website": "https://moderndecorco.com",
                "opening_hours": [
                    "Monday: 9:00 AM – 7:00 PM",
                    "Tuesday: 9:00 AM – 7:00 PM",
                    "Wednesday: 9:00 AM – 7:00 PM",
                    "Thursday: 9:00 AM – 7:00 PM",
                    "Friday: 9:00 AM – 8:00 PM",
                    "Saturday: 10:00 AM – 8:00 PM",
                    "Sunday: 11:00 AM – 6:00 PM",
                ],
                "is_open": False,
            },
        ]

        return stores

    def _calculate_distance(
        self, lat1: float, lng1: float, lat2: float, lng2: float
    ) -> float:
        """
        Calculate distance between two points in kilometers
        Using Haversine formula
        """
        from math import radians, cos, sin, asin, sqrt

        # Convert to radians
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])

        # Haversine formula
        dlng = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers
        r = 6371

        return round(c * r, 1)

    async def get_store_inventory(
        self, store_id: str, artwork_id: str
    ) -> Dict[str, Any]:
        """
        Check if a specific artwork is available at a store

        Args:
            store_id: Store identifier
            artwork_id: Artwork identifier

        Returns:
            Availability info
        """
        # Placeholder: In production, integrate with store inventory APIs
        return {
            "store_id": store_id,
            "artwork_id": artwork_id,
            "in_stock": True,
            "quantity": 1,
            "price": None,  # Store-specific pricing
            "estimated_delivery": "Available for pickup",
        }

    async def get_directions(
        self, origin: Tuple[float, float], destination: Tuple[float, float]
    ) -> Dict[str, Any]:
        """
        Get directions from origin to destination

        Args:
            origin: (latitude, longitude)
            destination: (latitude, longitude)

        Returns:
            Directions with distance and duration
        """
        if self.gmaps:
            try:
                directions = self.gmaps.directions(origin, destination, mode="driving")

                if directions:
                    leg = directions[0]["legs"][0]
                    return {
                        "distance": leg["distance"]["text"],
                        "duration": leg["duration"]["text"],
                        "steps": [
                            step["html_instructions"] for step in leg["steps"]
                        ][:5],  # First 5 steps
                    }
            except Exception as e:
                print(f"Error getting directions: {e}")

        # Mock directions
        return {
            "distance": "2.5 km",
            "duration": "8 mins",
            "steps": ["Head north on Main St", "Turn right onto Art Ave"],
        }

