#!/usr/bin/env python
"""
Plot summary histograms 
"""

__author__ = "SHI Xin <shixin@ihep.ac.cn>"
__copyright__ = "Copyright (c) SHI Xin"
__created__ = "[2016-07-25 Mon 09:22]" 

import os
import sys 
import ROOT 
#from ROOT import TH1F, gROOT
from tools import check_outfile_path, set_root_style


def main():
    set_root_style(stat=0, grid=0) 
    ROOT.gStyle.SetPadLeftMargin(0.15)

    sample = sys.argv[1:]
    fs = get_files_from_sample(sample)
    c = ROOT.TCanvas('c', 'c', 800, 800)

    draw_vtx_mkpi(sample, c, fs)
    draw_vtx_coskpi(sample, c, fs)
    draw_vtx_mom_kpi(sample, c, fs) 
    

def get_files_from_sample(sample):
    fs = [] 
    if 'data' in sample:
        fs.append(ROOT.TFile('/besfs/groups/jpsi/jpsigroup/user/gushan/ddstar/v0.3/4260/plot/python/cut.root'))

    if 'con3650' in sample:
        fs.append(ROOT.TFile('run/hist/con3650/jpsi2invi_con3650_merged_1.root'))

    if 'data09' in sample:
        fs.append(ROOT.TFile('run/hist/data09/jpsi2invi_data09_merged_1.root'))

    if 'mc_psip09' in sample:
        fs.append(ROOT.TFile('run/hist/mc_psip09/jpsi2invi_mc_psip_09mc_merged_1.root'))
        
    if 'mc_psip12' in sample:
        fs.append(ROOT.TFile('run/hist/mc_psip12/jpsi2invi_mc_psip_12mc_merged_1.root'))
        
    return fs 

def get_common_objects_to_draw(fs, hname, leg):
    hs = []

    leg.SetTextSize(0.03)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(0)
    
    for f in fs:
	print hname
	#h = gROOT.FindObject(hname)
        h = f.Get(hname)
        if fs.index(f) == 0:
            h.Sumw2()
            h.GetXaxis().SetLabelSize(0.03) 
            h.GetYaxis().SetLabelSize(0.03) 
            h.GetYaxis().SetTitleOffset(1.8) 
            h.SetMarkerStyle(ROOT.kFullDotLarge)
            
        elif fs.index(f) == 1:
            h.SetLineColor(29)
            h.SetFillColor(29)

        elif fs.index(f) == 2:
            h.SetLineColor(ROOT.kOrange)
            h.SetFillColor(ROOT.kOrange)
            
        leg = leg_add_entry_hist(leg, f, h)    
        hs.append(h) 
            
    return  hs, leg 


def leg_add_entry_hist(leg, f, h):
    sample = f.GetName()
    sample = sample.split('/')[2] 

    print sample
    if sample in ['data', 'data09', 'groups']:
        leg.AddEntry(h, "Data", "lp")

    elif sample in ['con3650']:
        leg.AddEntry(h, "Cont.")

    elif sample in ['mc_psip12', 'mc_psip09']:
        leg.AddEntry(h, "#psi(2S) inclusive MC")
    else:
        raise NameError(sample)

    return leg


def draw_vtx_mkpi(sample, c, fs):
    hname = 'h_vtxmkpi'
    figfile = 'figure/mkp_%s.pdf' %'_'.join(sample)
    check_outfile_path(figfile)
        
    leg = ROOT.TLegend(0.2, 0.71, 0.32, 0.91)
    hs, leg = get_common_objects_to_draw(fs, hname, leg) 

    for h in hs:
        if hs.index(h) == 0:
            h.SetXTitle('P_{ K^{+}#pi^{-}} (GeV/c^{2})') 
            h.SetYTitle('Events/(5 MeV/c^{2})')
            h.SetMarkerStyle(ROOT.kFullDotLarge)
            h.Draw()
        else:
            h.Draw('same')

    leg.Draw()
    c.SaveAs(figfile)

    
def draw_vtx_coskpi(sample, c, fs):
    hname = 'h_vtx_coskpi'
    figfile = 'figure/coskpi_%s.pdf' %'_'.join(sample) 
        
    leg = ROOT.TLegend(0.2, 0.71, 0.32, 0.91)
    hs, leg = get_common_objects_to_draw(fs, hname, leg) 
    
    for h in hs:
        if hs.index(h) == 0:
            h.SetXTitle('cos K^{+}#pi^{-}') 
            h.SetYTitle('Events /0.00005')
            h.SetMarkerStyle(ROOT.kFullDotLarge)
            h.Draw()
        else:
            h.Draw('same')

    leg.Draw()
    c.SaveAs(figfile)


def draw_vtx_mom_kpi(sample, c, fs):
    hname = 'h_vtx_mom_kpi'
    figfile = 'figure/mom_kpi_%s.pdf'  %'_'.join(sample) 
    leg = ROOT.TLegend(0.2, 0.71, 0.32, 0.91)
    hs, leg = get_common_objects_to_draw(fs, hname, leg) 

    for h in hs:
        if hs.index(h) == 0:
            h.SetXTitle('P_{ K^{+}#pi^{-}}')
            h.SetYTitle('Events /5MeV/c^{2}') 
            h.SetMarkerStyle(ROOT.kFullDotLarge)
            h.Draw()
        else:
            h.Draw('same') 

    leg.Draw()
    c.SaveAs(figfile)



    
if __name__ == '__main__':
    main()
