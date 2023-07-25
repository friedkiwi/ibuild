#!/QopenSys/pkgs/bin/python3

import yaml
import subprocess 

def crtlib(libname):
    subprocess.call(["system", "crtlib", libname])
    

def perform_build(build_dict):
    print("Performing build...")
    
    if build_dict['target_library']:
        crtlib(build_dict['target_library'])

    print("Done!")

def main():
    with open("ibuild.yaml") as f:
        build_dict = yaml.load(f, Loader=yaml.FullLoader)
        perform_build(build_dict)

if __name__ == "__main__":
    main()