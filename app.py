import os
from image_postprocess.processor import process_image
import tempfile
import argparse
from flask import Flask, render_template, request, send_file

# सिस्टम पाथ सेट करें ताकि processor.py मिल जाए
sys.path.insert(1, os.path.join(os.path.dirname(__file__), 'image_postprocess'))
from processor import process_image

app = Flask(__name__)
import tempfile
import argparse
from flask import Flask, render_template, request, send_file
# इस रिपॉजिटरी का अपना फंक्शन इम्पोर्ट कर रहे हैं
from image_postprocess.processor import process_image

app = Flask(__name__)

# वेबसाइट के लिए डिफ़ॉल्ट सेटिंग्स (args बनाना)
def get_default_args():
    return argparse.Namespace(
        awb=True, ref=None, noise=True, noise_std=0.02,
        clahe=True, clahe_clip=2.0, tile=8,
        cutoff=0.25, fstrength=0.9, randomness=0.05, seed=None,
        fft=False, fft_ref=None, fft_mode='auto', fft_alpha=1.0,
        phase_perturb=0.08, radial_smooth=5,
        glcm=False, glcm_distances=[1], glcm_angles=[0, 0.78, 1.57, 2.35],
        glcm_levels=256, glcm_strength=0.9,
        lbp=False, lbp_radius=3, lbp_n_points=24, lbp_method='uniform', lbp_strength=0.9,
        non_semantic=False, ns_iterations=500, ns_learning_rate=3e-4,
        ns_t_lpips=4e-2, ns_t_l2=3e-5, ns_c_lpips=1e-2, ns_c_l2=0.6, ns_grad_clip=0.05,
        sim_camera=True, no_no_bayer=True, jpeg_cycles=1,
        jpeg_qmin=88, jpeg_qmax=96, vignette_strength=0.35,
        chroma_strength=1.2, iso_scale=1.0, read_noise=2.0,
        hot_pixel_prob=1e-6, banding_strength=0.0, motion_blur_kernel=1,
        lut=None, lut_strength=0.1, perturb=True, perturb_magnitude=0.008,
        blend=False, blend_tolerance=10.0, blend_min_region=50,
        blend_max_samples=100000, blend_n_jobs=None
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    
    try:
        temp_dir = tempfile.gettempdir()
        in_path = os.path.join(temp_dir, "input.jpg")
        out_path = os.path.join(temp_dir, "BAHERUNI.jpg")
        
        file.save(in_path)
        args = get_default_args()
        
        # रिपॉजिटरी का मुख्य फंक्शन कॉल कर रहे हैं
        process_image(in_path, out_path, args)
        
        return send_file(out_path, as_attachment=True, download_name='BAHERUNI.jpg')
    except Exception as e:
        import traceback
        return traceback.format_exc(), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
