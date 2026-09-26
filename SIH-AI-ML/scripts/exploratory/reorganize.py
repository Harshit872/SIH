import os
import shutil

root_dir = 'C:/Users/umang/SIH'

# Target directories
aiml_data_prep = os.path.join(root_dir, 'SIH-AI-ML', 'src', 'data_prep')
aiml_model = os.path.join(root_dir, 'SIH-AI-ML', 'src', 'model')
aiml_scripts = os.path.join(root_dir, 'SIH-AI-ML', 'scripts', 'exploratory')
backend_scripts = os.path.join(root_dir, 'SIH-BACKEND', 'scripts')
frontend_scripts = os.path.join(root_dir, 'SIH-FRONTEND', 'scripts')

for d in [aiml_data_prep, aiml_model, aiml_scripts, backend_scripts, frontend_scripts]:
    os.makedirs(d, exist_ok=True)

# List all .py files in root
py_files = [f for f in os.listdir(root_dir) if f.endswith('.py') and os.path.isfile(os.path.join(root_dir, f))]

for f in py_files:
    src = os.path.join(root_dir, f)
    
    # Logic to route files
    if f in ['clean_data.py', 'extract_pdfs.py', 'gen_synthetic.py', 'prepare_dataset.py', 'run_etl.py']:
        dest = aiml_data_prep
    elif f in ['train.py', 'guardrails.py']:
        dest = aiml_model
    elif f.startswith('patch_') and not 'routes' in f:
        dest = frontend_scripts
    elif f.startswith('patch_routes') or f.startswith('test_'):
        dest = backend_scripts
    else:
        # Default for exploratory / temp scripts (check_, inspect_, generalize_, etc)
        dest = aiml_scripts
        
    shutil.move(src, os.path.join(dest, f))
    print(f"Moved {f} -> {dest}")
