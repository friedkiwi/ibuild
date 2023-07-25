#!/QopenSys/pkgs/bin/python3

import yaml
import subprocess
import os
import random  

def sanitize_path(filename):
    return os.path.abspath(filename)


def crtlib(libname):
    subprocess.call(["system", "crtlib", libname])

def dltlib(libname):
    subprocess.call(["system", "dltlib", libname])

def crtdspf(srcfile, tgtlib, tgtfile):    
    tmp_id = random.randint(100000,999999)
    crtlib("BLD%d" % (tmp_id))
    subprocess.call(["system", "crtsrcpf", "FILE(BLD%d/BLD%d)" % (tmp_id, tmp_id), "RCDLEN(132)" ])
    subprocess.call(["system", "cpyfrmstmf", "FROMSTMF('%s')" % (sanitize_path(srcfile)), "TOMBR('/QSYS.LIB/BLD%d.LIB/BLD%d.FILE/BUILD.MBR')" % (tmp_id, tmp_id), "MBROPT(*ADD)"])
    subprocess.call(["system", "crtdspf", "FILE(%s/%s)" % (tgtlib, tgtfile), "SRCFILE(BLD%d/BLD%d)" % (tmp_id, tmp_id), "SRCMBR(BUILD)"])
    subprocess.call(["system", "dsplib", "BLD%d" % (tmp_id)])
    dltlib("BLD%d" % (tmp_id))

def crtcmd(cmdname, tgtlib, tgtpgm, cmdspec):    
    tmp_id = random.randint(100000,999999)
    crtlib("BLD%d" % (tmp_id))
    subprocess.call(["system", "crtsrcpf", "FILE(BLD%d/BLD%d)" % (tmp_id, tmp_id), "RCDLEN(132)" ])
    subprocess.call(["system", "cpyfrmstmf", "FROMSTMF('%s')" % (sanitize_path(cmdspec)), "TOMBR('/QSYS.LIB/BLD%d.LIB/BLD%d.FILE/BUILD.MBR')" % (tmp_id, tmp_id), "MBROPT(*ADD)"])
    subprocess.call(["system", "crtcmd", "CMD(%s/%s)" % (tgtlib, cmdname) , "SRCFILE(BLD%d/BLD%d)" % (tmp_id, tmp_id), "PGM(%s/%s)" % (tgtlib, tgtpgm), "SRCMBR(BUILD)"])
    subprocess.call(["system", "dsplib", "BLD%d" % (tmp_id)])
    dltlib("BLD%d" % (tmp_id))



def crtbndrpg(srcfile, tgtlib, tgtfile):
    subprocess.call(['system', 'crtbndrpg', "SRCSTMF('%s')" % (sanitize_path(srcfile)), "PGM(%s/%s)" % (tgtlib, tgtfile)])

    

def perform_build(build_dict):
    print("Performing build...")
    
    if build_dict['target_library']:
        crtlib(build_dict['target_library'])

    if build_dict['dspf']:
        for dspf in build_dict['dspf']:
            crtdspf(dspf, build_dict['target_library'], os.path.splitext(dspf)[0])

    if build_dict['rpgle']:
        for rpgle in build_dict['rpgle']:
            crtbndrpg(rpgle, build_dict['target_library'], os.path.splitext(rpgle)[0])

    if build_dict['cmd']:
        for pgm in list(build_dict['cmd'].keys()):
            crtcmd(pgm, build_dict['target_library'], build_dict['cmd'][pgm]['pgm'], build_dict['cmd'][pgm]['src'])

    print("Done!")

def main():
    with open("ibuild.yaml") as f:
        build_dict = yaml.load(f, Loader=yaml.FullLoader)
        perform_build(build_dict)

if __name__ == "__main__":
    main()