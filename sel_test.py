#!/usr/bin/env python
"""
Event Selection 
"""

__author__ = "SHI Xin <shixin@ihep.ac.cn>"
__copyright__ = "Copyright (c) SHI Xin"
__created__ = "[2016-11-01 Tue 09:11]" 

import sys
import os
import math 
import ROOT 
from progressbar import Bar, Percentage, ProgressBar
from time import time 
from tools import duration, check_outfile_path

#TEST=True 
TEST=False

# Global constants 
D0_MASS = 1.86484; 

# Global histograms
h_cutflw = ROOT.TH1F('hcutflw', 'cutflow', 10, 0, 10)
h_cutflw.GetXaxis().SetBinLabel(1, 'vtx_mkpi')
h_cutflw.GetXaxis().SetBinLabel(2, 'vtx_coskpi')
h_cutflw.GetXaxis().SetBinLabel(3, 'vtx_mom_kpi')

h_vtx_mkpi = ROOT.TH1D('h_vtxmkpi', 'mrecpipi', 200, 1.8, 2)
h_vtx_coskpi = ROOT.TH1D('h_vtx_coskpi', 'vtx_coskpi', 200, -1, -0.99) 
h_vtx_mom_kpi = ROOT.TH1D('h_vtx_mom_kpi', 'vtx_mom_kpi', 400, 0.0, 2) 


def usage():
    sys.stdout.write('''
NAME
    sel_events_jpsi2incl.py 

SYNOPSIS

    ./sel_events_jpsi2incl.py infile outfile 

\n''')

    
def main():

    if TEST:
        sys.stdout.write('Run in TEST mode! \n')
    
    args = sys.argv[1:]
    if len(args) < 2:
        return usage()
    
    infile = args[0]
    outfile = args[1]
    check_outfile_path(outfile)

    fin = ROOT.TFile(infile)
    t = fin.Get('D0bar_kpi')
    entries = t.GetEntriesFast()

    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=entries).start()
    time_start = time()

    for jentry in xrange(entries):
        pbar.update(jentry+1)
        # get the next tree in the chain and verify
        ientry = t.LoadTree(jentry)
        if ientry < 0:
            break
        # copy next entry into memory and verify

        if TEST and ientry > 1000:
            break
        
        nb = t.GetEntry(jentry)
        if nb<=0:
            continue

        fill_histograms(t)
        
        #if select_jpsi_to_invisible(t): 
        #   h_vtx_mkpi.Fill(t.vtx_mkpi)
#	select_jpsi_to_invisible(t)
 
    fout = ROOT.TFile(outfile, "RECREATE")
    write_histograms() 
    fout.Close()
    pbar.finish()
    
    dur = duration(time()-time_start)
    sys.stdout.write(' \nDone in %s. \n' % dur) 


def fill_histograms(t):
    cut_vtx_mom_kpi = (abs(t.vtx_mom_kpi-1)<1)
    cut_vtx_mkpi = (abs(t.vtx_mkpi-1.86484) < 0.015)
    cut_vtx_coskpi = (t.vtx_coskpi>-0.998)

    if (cut_vtx_mom_kpi and cut_vtx_mkpi):
        h_vtx_coskpi.Fill(t.vtx_coskpi)

    if (cut_vtx_mkpi and cut_vtx_coskpi):
        h_vtx_mom_kpi.Fill(t.vtx_mom_kpi)

    if (cut_vtx_coskpi and cut_vtx_mom_kpi):
        h_vtx_mkpi.Fill(t.vtx_mkpi)


    
def write_histograms():
    h_vtx_coskpi.Write()
    h_vtx_mom_kpi.Write()
    h_vtx_mkpi.Write()
#    h_cutflw.Write()
    
#def select_jpsi_to_invisible(t):
#    h_cutflw.Fill(0) 

#    if not (abs(t.vtx_mom_kpi-1)<1 and abs(t.vtx_mkpi-1.86484) < 0.015):
#        return False
#    h_cutflw.Fill(1) 
   
#    if not (abs(t.vtx_mkpi-1.86484) < 0.015 and abs(t.vtx_mom_kpi-1)<1):
#        return False
#    h_cutflw.Fill(2) 

#    if not (t.vtx_coskpi>-0.998 and abs(t.vtx_mom_kpi-1)<1 ):
#        return False 
#    h_cutflw.Fill(3)

    
    return True
    
    
if __name__ == '__main__':
    main()
