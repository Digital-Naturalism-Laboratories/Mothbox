import piexif
from PIL import Image

def deg_to_dms_rational(deg_float):
    """Convert decimal degrees to degrees, minutes, seconds in rational format"""
    deg = int(deg_float)
    min_float = abs(deg_float - deg) * 60
    minute = int(min_float)
    sec_float = (min_float - minute) * 60
    sec = int(sec_float * 10000)

    return ((abs(deg), 1), (minute, 1), (sec, 10000))

def add_gps_exif(input_path, output_path, lat, lng, altitude=None):
    # Load image
    img = Image.open(input_path)

    # Try to load existing EXIF data, or start fresh
    exif_bytes = img.info.get("exif")
    if exif_bytes:
        exif_dict = piexif.load(exif_bytes)
    else:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    # Create GPS IFD
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
        piexif.GPSIFD.GPSLatitude: deg_to_dms_rational(lat),
        piexif.GPSIFD.GPSLongitudeRef: 'E' if lng >= 0 else 'W',
        piexif.GPSIFD.GPSLongitude: deg_to_dms_rational(lng),
    }

    if altitude is not None:
        gps_ifd[piexif.GPSIFD.GPSAltitudeRef] = 0 if altitude >= 0 else 1
        gps_ifd[piexif.GPSIFD.GPSAltitude] = (int(abs(altitude * 100)), 100)

    # Inject GPS into EXIF
    exif_dict['GPS'] = gps_ifd
    exif_bytes = piexif.dump(exif_dict)

    # Save the image with new EXIF
    img.save(output_path, exif=exif_bytes)
    print(f"Saved image with GPS data: {output_path}")

# === Example usage ===
input_file = r"c:\Users\andre\Desktop\Dinacon Stuff\test\cuervoCinife_2025_06_30__04_53_06_HDR0_0_Mothbot_yolo11m_4500_imgsz1600_b1_2024-01-18.pt.jpg"  # Replace with your photo path
output_file = r"c:\Users\andre\Desktop\Dinacon Stuff\test\cuervoCinife_2025_06_30__04_53_06_HDR0_0_Mothbot_yolo11m_4500_imgsz1600_b1_2024-01-18.ptGPS.jpg"  # Path to save the modified photo
latitude = 37.7749
longitude = -122.4194
altitude = 15.2  # Optional

add_gps_exif(input_file, output_file, latitude, longitude, altitude)



