from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import base64
import numpy as np

from analysis import analyze_aoi
from geocoding import detect_state_from_nominatim_result
from plotting import plot_land_cover_trends, visualize_multiple_years, show_overlay_on_map
from utils import buffer_bbox

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        nominatim_result = data.get("nominatim_result")
        
        if not nominatim_result:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Nominatim result is missing."}).encode('utf-8'))
            return

        bbox = [float(nominatim_result["boundingbox"][2]), float(nominatim_result["boundingbox"][0]), float(nominatim_result["boundingbox"][3]), float(nominatim_result["boundingbox"][1])]
        location_name = nominatim_result["display_name"]

        state_name, state_code = detect_state_from_nominatim_result(nominatim_result)

        if state_code == "unknown":
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Location not in a supported state or country."}).encode('utf-8'))
            return

        buffered_bbox = buffer_bbox(bbox)

        try:
            df, images = analyze_aoi(state_code, buffered_bbox)

            if df.empty:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No data found for this region."}).encode('utf-8'))
                return

            trends_plot_bytes = plot_land_cover_trends(df)
            yearly_maps_bytes = visualize_multiple_years(images)

            first_image_array = None
            if images:
                first_image_array = images[list(images.keys())[0]]
            
            overlay_map_bytes = b''
            if first_image_array is not None:
                overlay_map_bytes = show_overlay_on_map(first_image_array, buffered_bbox)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response_data = {
                "location_name": location_name,
                "state_name": state_name,
                "state_code": state_code,
                "trends_data": df.to_dict(orient="records"),
                "trends_plot_png": base64.b64encode(trends_plot_bytes).decode('utf-8'),
                "yearly_maps_png": base64.b64encode(yearly_maps_bytes).decode('utf-8'),
                "overlay_map_png": base64.b64encode(overlay_map_bytes).decode('utf-8'),
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))