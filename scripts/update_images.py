
import json
import os

# Define the mapping from local filename/keyword to external URL
# Based on user input:
IMAGE_MAP = {
    "2dbeamformingsimulator": "https://i.postimg.cc/0bFTx0zL/2dbeamformingsimulator.jpg",
    "audiophileeq": "https://i.postimg.cc/ZWN1qv3C/audiophileeq.jpg",
    "automateddefibrillatorsystem": "https://i.postimg.cc/yDRwN3Rw/automateddefibrillatorsystem.avif",
    "biorhythmanalyzer": "https://i.postimg.cc/hXmHGQmN/biorhythmanalyzer.jpg",
    "breastcancerxaievaluation": "https://i.postimg.cc/svqky4BV/breastcancerxaievaluation.avif",
    "checkmatechessgame": "https://i.postimg.cc/K1TdY3Lb/checkmatechessgame.jpg",
    "cybermazer2077": "https://i.postimg.cc/WdZQ4qr2/cybermazer2077.jpg",
    "digitalfilterapplication": "https://i.postimg.cc/21WP5Lvr/digitalfilterapplication.jpg",
    "drivesafesigndetection": "https://i.postimg.cc/hXmHGQxG/drivesafesigndetection.avif",
    "dynamicmultichannelsignalviewer": "https://i.postimg.cc/5XzZtQv0/dynamicmultichannelsignalviewer.jpg",
    "edgeenhance": "https://i.postimg.cc/LJPrsgfJ/edgeenhance.jpg",
    "facevector": "https://i.postimg.cc/dhCz0ZdZ/facevector.jpg",
    "hospitalsystemwebsite": "https://i.postimg.cc/68ZDQ4Rv/hospitalsystemwebsite.jpg",
    "imageftmixerpro": "https://i.postimg.cc/JyWSH7cv/imageftmixerpro.jpg",
    "lifestream": "https://i.postimg.cc/hJqNQ4bL/lifestream.jpg",
    "medicluster": "https://i.postimg.cc/gwP1Lcqw/medicluster.avif",
    "moviematch100k": "https://i.postimg.cc/SXpHYQ72/moviematch100k.avif",
    "mrfrequencysculptor": "https://i.postimg.cc/wtcZXK0Z/mrfrequencysculptor.jpg",
    "musicspectronet": "https://i.postimg.cc/DWKR4fdP/musicspectronet.avif",
    "neuropathx": "https://i.postimg.cc/yJXtmqvP/neuropathx.jpg",
    "oralcancerprediction": "https://i.postimg.cc/kVFzQrfw/oralcancerprediction.avif",
    "pixelizing": "https://i.postimg.cc/sB9qYFw0/pixelizing.jpg",
    "predictiloan": "https://i.postimg.cc/cKM2RqXP/predictiloan.avif",
    "pulsespy": "https://i.postimg.cc/5HqTBcsJ/pulsespy.jpg",
    "sequencealignx": "https://i.postimg.cc/06dFYgVP/sequencealignx.jpg",
    "siftsee": "https://i.postimg.cc/LqBwtdxm/siftsee.jpg",
    "sigmavision": "https://i.postimg.cc/jWQmHVMd/sigmavision.jpg",
    "signalreconstructionapplication": "https://i.postimg.cc/xJf7gsZV/signalreconstructionapplication.jpg",
    "smartretailregressor": "https://i.postimg.cc/wyqPFWrd/smartretailregressor.avif",
    "soundprints": "https://i.postimg.cc/1nmTMWdy/soundprints.jpg",
    "stm32labsuite": "https://i.postimg.cc/hzDwMCYS/stm32labsuite.jpg"
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CONTENT_FILE = os.path.join(PROJECT_ROOT, 'content', 'projects.json')

def update_images():
    with open(CONTENT_FILE, 'r') as f:
        data = json.load(f)
    
    projects = data.get('Projects', [])
    updated_count = 0
    
    for p in projects:
        current_img = p.get('overview_image', '')
        # Extract basename without extension to find key
        # e.g. "/images/projects/neuropathx.avif" -> "neuropathx"
        basename = os.path.splitext(os.path.basename(current_img))[0]
        
        if basename in IMAGE_MAP:
            p['overview_image'] = IMAGE_MAP[basename]
            updated_count += 1
            print(f"Updated {p['title']} -> {IMAGE_MAP[basename]}")
        else:
            print(f"⚠️ No match found for {p['title']} (file: {basename})")

    with open(CONTENT_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"\nSuccessfully updated {updated_count} projects in projects.json")

if __name__ == "__main__":
    update_images()
