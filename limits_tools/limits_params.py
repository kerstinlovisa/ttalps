lumi = 150.0 * 1000.0 # pb-1
lumi_syst = 1.1

n_generated_ttj = 12540000.0
n_generated_ttmumu = 9940000.0

# x_sec in pb
cross_section_ttj = 395.296031
cross_section_ttmumu = 0.02091178


def get_ctaus(sample):
    # the empty string includes the default ctau value
    ctaus = {
        "1e4": ("", "0p0000100", "0p0000500", "0p0001000"),
        "1": ("", "0p1000000", "0p5000000", "1p0000000"),
        "1e2": ("", "100p0000000", "50p0000000", "10p0000000"),
    }
    if sample in ctaus:
        return ctaus[sample]
    
    return ("",)


def get_base_background_path(sample):
    if sample == "default_non-prompt-selection":
        return "/nfs/dust/cms/user/lrygaard/ttalps/backgrounds_non-prompt-selection/hists/"
    elif sample == "default_new-dimuon-mass-cuts":
        # return "/nfs/dust/cms/user/lrygaard/ttalps/backgrounds_new-dimuon-mass-cuts/hists/"
        return "/nfs/dust/cms/user/jalimena/ttalps/ttalps_backup_default_July23/backgrounds_new-dimuon-mass-cuts/hists/"    
    
    # return "/nfs/dust/cms/user/lrygaard/ttalps/backgrounds_new-dimuon-mass-cuts/hists/"
    return "/nfs/dust/cms/user/jalimena/ttalps/ttalps_backup_default_July23/backgrounds_new-dimuon-mass-cuts/hists/"


def get_base_path(sample):
    if sample == "default":
        return "/nfs/dust/cms/user/lrygaard/ttalps/hists/"
    elif sample == "default_non-muon-mothers":
        return "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-default_muon-status/hists/"
    elif sample == "default_non-prompt-selection":
        return "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-default_non-prompt-selection/hists/"
    elif sample == "default_new-dimuon-mass-cuts":
        return "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-default_new-dimuon-mass-cuts/hists/"
    elif sample == "default_ptAlp-ge5GeV":
        return "/nfs/dust/cms/user/lrygaard/ttalps/signals_default_ptAlp-ge5GeV/hists/"
    
    # return f"/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-{sample}/hists/"
    return f"/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-{sample}_rerun/hists/"


cuts = "pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05"
# cuts = "pt-min5p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05"

# hist_name = f"final_selection/final_selection_{cuts}_os_maxlxy-muon_lxy_rebinned"
background_hist_name = f"final_selection/final_selection_{cuts}_os_minlxy-muon_lxy_rebinned_extended"
# background_hist_name = f"final_selection/final_selection_{cuts}_os_first_minlxy-muon_lxy_rebinned_extended"

signal_hist_name = f"final_selection/final_selection_{cuts}_os_minlxy-muon_lxy_rebinned_extended"
# signal_hist_name = f"final_selection/final_selection_{cuts}_os_first_minlxy-muon_lxy_rebinned_extended"


output_file_name = f"limits_{cuts}.root"

tmp_combine_file_name = "tmp_combine_workspace.root"
tmp_output_file_name = "tmp_output.txt"

signals = {
    "default": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    990000.0,   1e-3)),
        "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   1000000.0,  1e-3)),
        "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    1000000.0,  1e-3)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    1000000.0,  1e-3)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   990000.0,   1e-3)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-2p5GeV":  (2.5,   ("tta_mAlp-2p5GeV.root",    1000000.0,  1e-3)),
        "tta_mAlp-2p75GeV": (2.75,  ("tta_mAlp-2p75GeV.root",   990000.0,   1e-3)),
        "tta_mAlp-3GeV":    (3.0,   ("tta_mAlp-3GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      1000000.0,  1e0)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-8p25GeV": (8.25,  ("tta_mAlp-8p25GeV.root",   1000000.0,  1e-3)),
        "tta_mAlp-8p5GeV":  (8.5,   ("tta_mAlp-8p5GeV.root",    1000000.0,  1e3)),
        "tta_mAlp-9GeV":    (9.0,   ("tta_mAlp-9GeV.root",      1000000.0,  1e3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     980000.0,   1e3)),
    },
    "1e0": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    1000000.0,  1e-3)),
        "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   1000000.0,  1e-3)),
        "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    1000000.0,  1e-3)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    990000.0,   1e-3)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   990000.0,   1e-3)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      980000.0,   1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     990000.0,   1e-1)),
    },
    "1e1": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        # "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    990000.0,   1e-3)),
        # "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   990000.0,   1e-3)),
        # "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    990000.0,   1e-3)),
        # "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    1000000.0,  1e-3)),
        # "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   1000000.0,  1e-3)),
        # "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      1000000.0,  1e-3)),
        # "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      1000000.0,  1e-3)),
        # "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     990000.0,   1e-3)),
    },
    "5e3": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    990000.0,   1e0)),
        "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    990000.0,   1e0)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   970000.0,   1e0)),
    },
    "1e4": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    970000.0,   1e0)),
        "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   1000000.0,  1e0)),
        # "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    1000000.0,  1e0)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    1000000.0,  1e0)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   990000.0,   1e0)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      990000.0,   1e0)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     1000000.0,  1e-3)),
    },
    "5e4": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      1000000.0,  1e0)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      960000.0,   1e-3)),
    },
    "9e4": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     960000.0,   1e-3)),
    },
    "1e5": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    980000.0,   1e-3)),
        "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   1000000.0,  1e-3)),
        "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    990000.0,   1e-3)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    990000.0,   1e-3)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   990000.0,   1e-3)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      980000.0,   1e-3)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     1000000.0,  1e-3)),
    },
    "1e6": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    990000.0,   1e0)),
        "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   1000000.0,  1e0)),
        "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    990000.0,   1e0)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    1000000.0,  1e0)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   990000.0,   1e-3)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      970000.0,   1e-3)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     1000000.0,  1e-3)),
    },
    "2e6": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    990000.0,   1e0)),
        "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   980000.0,   1e0)),
        "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    990000.0,   1e0)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    990000.0,   1e0)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   1000000.0,  1e-3)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      1000000.0,  1e-3)),
    },
    "3e6": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    980000.0,   1e0)),
        "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   1000000.0,  1e0)),
        "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    1000000.0,  1e0)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    2990000.0,  1e0)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   3000000.0,  1e-3)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      2980000.0,  1e-3)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     980000.0,   1e-3)),
    },
    "5e6": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        # "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    1000000.0,  1e3)),
        "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   970000.0,   1e-1)),
        "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    1000000.0,  1e-1)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    990000.0,   1e-1)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   1000000.0,  1e-1)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      980000.0,   1e-1)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      990000.0,   1e-1)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      990000.0,   1e-1)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     1000000.0,  1e-1)),
    },
    "8e6": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        # "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    990000.0,   1e0)),
        "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   1000000.0,  1e0)),
        "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    1000000.0,  1e0)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    1000000.0,  1e0)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   990000.0,   1e-3)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     1000000.0,  1e-3)),
    },
    "1e7": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        # "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    980000.0,   1e1)),
        "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   990000.0,   1e0)),
        "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    1000000.0,  1e0)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    1000000.0,  1e0)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   980000.0,   1e-3)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      990000.0,   1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     990000.0,   1e-3)),
        "tta_mAlp-50GeV":   (50,    ("tta_mAlp-50GeV.root",     1000000.0,  1e-3)),
    },
    "2e7": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        # "tta_mAlp-0p3GeV":  (0.3,   ("tta_mAlp-0p3GeV.root",    980000.0,   1e1)),
        # "tta_mAlp-0p35GeV": (0.35,  ("tta_mAlp-0p35GeV.root",   1000000.0,  1e1)),
        # "tta_mAlp-0p5GeV":  (0.5,   ("tta_mAlp-0p5GeV.root",    1000000.0,  1e6)),
        "tta_mAlp-0p9GeV":  (0.9,   ("tta_mAlp-0p9GeV.root",    1000000.0,  1e0)),
        "tta_mAlp-1p25GeV": (1.25,  ("tta_mAlp-1p25GeV.root",   1000000.0,  1e0)),
        "tta_mAlp-2GeV":    (2.0,   ("tta_mAlp-2GeV.root",      980000.0,   1e-3)),
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      1000000.0,  1e-3)),
        "tta_mAlp-8GeV":    (8.0,   ("tta_mAlp-8GeV.root",      980000.0,   1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     1000000.0,  1e-3)),
        "tta_mAlp-50GeV":   (50,    ("tta_mAlp-50GeV.root",     1000000.0,  1e-3)),
    },
    "2e8": {
        #                   mass    file                        n_gen       ref. x_sec (pb)
        "tta_mAlp-4GeV":    (4.0,   ("tta_mAlp-4GeV.root",      980000.0,   1e-3)),
        "tta_mAlp-10GeV":   (10,    ("tta_mAlp-10GeV.root",     1000000.0,  1e-3)),
        "tta_mAlp-50GeV":   (50,    ("tta_mAlp-50GeV.root",     1000000.0,  1e-3)),
    },
}

