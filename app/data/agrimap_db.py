"""Database layer for AgriMap - NPK soil data and polygon storage."""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid


class AgriMapDatabase:
    """Simple JSON-based database for AgriMap data."""
    
    def __init__(self, data_dir='instance'):
        """Initialize database with data directory."""
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.polygons_file = os.path.join(data_dir, 'agrimap_polygons.json')
        self.npk_data_file = os.path.join(data_dir, 'agrimap_npk_data.json')
        self.markers_file = os.path.join(data_dir, 'agrimap_markers.json')
        
        # Initialize files if they don't exist
        self._init_file(self.polygons_file, [])
        self._init_file(self.npk_data_file, [])
        self._init_file(self.markers_file, [])
    
    def _init_file(self, filepath, default_data):
        """Initialize JSON file if it doesn't exist."""
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
    
    def _read_json(self, filepath):
        """Read JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return []
    
    def _write_json(self, filepath, data):
        """Write JSON file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    
    # ========== POLYGON OPERATIONS ==========
    
    def save_polygon(self, name: str, coordinates: List, area_sqm: float, 
                     soil_type: Optional[str] = None, ph: Optional[float] = None,
                     notes: Optional[str] = None) -> Dict:
        """Save a field polygon."""
        polygons = self._read_json(self.polygons_file)
        
        polygon = {
            'id': str(uuid.uuid4()),
            'name': name,
            'coordinates': coordinates,
            'area_sqm': area_sqm,
            'area_hectares': round(area_sqm / 10000, 4),
            'soil_type': soil_type,
            'ph': ph,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        polygons.append(polygon)
        self._write_json(self.polygons_file, polygons)
        return polygon
    
    def get_polygons(self) -> List[Dict]:
        """Get all saved polygons."""
        return self._read_json(self.polygons_file)
    
    def get_polygon_by_id(self, polygon_id: str) -> Optional[Dict]:
        """Get polygon by ID."""
        polygons = self._read_json(self.polygons_file)
        for polygon in polygons:
            if polygon['id'] == polygon_id:
                return polygon
        return None
    
    def update_polygon(self, polygon_id: str, updates: Dict) -> bool:
        """Update polygon data."""
        polygons = self._read_json(self.polygons_file)
        for i, polygon in enumerate(polygons):
            if polygon['id'] == polygon_id:
                polygon.update(updates)
                polygon['updated_at'] = datetime.now().isoformat()
                polygons[i] = polygon
                return self._write_json(self.polygons_file, polygons)
        return False
    
    def delete_polygon(self, polygon_id: str) -> bool:
        """Delete polygon."""
        polygons = self._read_json(self.polygons_file)
        polygons = [p for p in polygons if p['id'] != polygon_id]
        return self._write_json(self.polygons_file, polygons)
    
    # ========== NPK DATA OPERATIONS ==========
    
    def save_npk_data(self, latitude: float, longitude: float,
                      n_value: float, p_value: float, k_value: float,
                      polygon_id: Optional[str] = None,
                      crop_type: Optional[str] = None,
                      soil_texture: Optional[str] = None,
                      ph: Optional[float] = None,
                      soil_temperature: Optional[float] = None,
                      soil_moisture: Optional[float] = None,
                      notes: Optional[str] = None) -> Dict:
        """Save NPK soil data for a location with comprehensive professional data."""
        npk_data_list = self._read_json(self.npk_data_file)
        
        npk_data = {
            'id': str(uuid.uuid4()),
            'latitude': latitude,
            'longitude': longitude,
            'crop_type': crop_type,
            'soil_texture': soil_texture,
            'n_value': n_value,
            'p_value': p_value,
            'k_value': k_value,
            'ph': ph,
            'soil_temperature': soil_temperature,
            'soil_moisture': soil_moisture,
            'polygon_id': polygon_id,
            'notes': notes,
            'created_at': datetime.now().isoformat()
        }
        
        npk_data_list.append(npk_data)
        self._write_json(self.npk_data_file, npk_data_list)
        return npk_data
    
    def get_npk_data(self, polygon_id: Optional[str] = None) -> List[Dict]:
        """Get NPK data, optionally filtered by polygon_id."""
        npk_data_list = self._read_json(self.npk_data_file)
        if polygon_id:
            return [data for data in npk_data_list if data.get('polygon_id') == polygon_id]
        return npk_data_list
    
    def get_npk_by_location(self, latitude: float, longitude: float, 
                           radius_km: float = 1.0) -> List[Dict]:
        """Get NPK data near a location (simple distance check)."""
        npk_data_list = self._read_json(self.npk_data_file)
        nearby = []
        
        for data in npk_data_list:
            # Simple distance calculation (rough approximation)
            lat_diff = abs(data['latitude'] - latitude)
            lon_diff = abs(data['longitude'] - longitude)
            distance = ((lat_diff ** 2 + lon_diff ** 2) ** 0.5) * 111  # km
            
            if distance <= radius_km:
                data['distance_km'] = round(distance, 2)
                nearby.append(data)
        
        return sorted(nearby, key=lambda x: x['distance_km'])
    
    def delete_npk_data(self, npk_id: str) -> bool:
        """Delete NPK data."""
        npk_data_list = self._read_json(self.npk_data_file)
        npk_data_list = [data for data in npk_data_list if data['id'] != npk_id]
        return self._write_json(self.npk_data_file, npk_data_list)
    
    # ========== MARKER OPERATIONS ==========
    
    def add_marker(self, marker_type: str, latitude: float, longitude: float,
                   title: str, description: Optional[str] = None,
                   polygon_id: Optional[str] = None) -> Dict:
        """Add a marker to the map."""
        markers = self._read_json(self.markers_file)
        
        marker = {
            'id': str(uuid.uuid4()),
            'type': marker_type,  # crop, pest, irrigation, note, npk_sample
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'description': description,
            'polygon_id': polygon_id,
            'created_at': datetime.now().isoformat()
        }
        
        markers.append(marker)
        self._write_json(self.markers_file, markers)
        return marker
    
    def get_markers(self, polygon_id: Optional[str] = None, 
                   marker_type: Optional[str] = None) -> List[Dict]:
        """Get markers, optionally filtered."""
        markers = self._read_json(self.markers_file)
        
        if polygon_id:
            markers = [m for m in markers if m.get('polygon_id') == polygon_id]
        if marker_type:
            markers = [m for m in markers if m.get('type') == marker_type]
        
        return markers
    
    def delete_marker(self, marker_id: str) -> bool:
        """Delete marker."""
        markers = self._read_json(self.markers_file)
        markers = [m for m in markers if m['id'] != marker_id]
        return self._write_json(self.markers_file, markers)
    
    # ========== STATISTICS ==========
    
    def get_statistics(self) -> Dict:
        """Get overall statistics."""
        polygons = self._read_json(self.polygons_file)
        npk_data = self._read_json(self.npk_data_file)
        markers = self._read_json(self.markers_file)
        
        total_area = sum(p.get('area_sqm', 0) for p in polygons)
        
        return {
            'total_polygons': len(polygons),
            'total_area_sqm': total_area,
            'total_area_hectares': round(total_area / 10000, 4),
            'total_npk_samples': len(npk_data),
            'total_markers': len(markers),
            'marker_types': self._count_marker_types(markers)
        }
    
    def _count_marker_types(self, markers: List[Dict]) -> Dict:
        """Count markers by type."""
        counts = {}
        for marker in markers:
            marker_type = marker.get('type', 'unknown')
            counts[marker_type] = counts.get(marker_type, 0) + 1
        return counts
