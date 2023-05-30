#include <filesystem>
#include "PlotHelpers.h"

void plot_pt()
{
  // Options for plotting:
  bool weighted = true;
  bool overflow = true;
  int int_lumi = 150e3; // pb-1

  string username = getenv("USER");

  string base_path; 
  string base_path_signal =  "/nfs/dust/cms/user/" + username + "/ttalps/signals_ctau-default_new-dimuon-mass-cuts/hists/";
  string base_path_background =  "/nfs/dust/cms/user/" + username + "/ttalps/backgrounds_new-dimuon-mass-cuts/hists/";
  string output_path;
  if(username == "lrygaard") {output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/plots_pt/";}
  // else if(username == "jniedzie") {output_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/";}
  // Only set up for user lrygaard now
  else {cout << "Error: unrecognized user." << endl;}

  filesystem::path p(output_path);
  if(!filesystem::exists(p))
  {
    filesystem::create_directory(p);
    p = output_path + "final_selection";
    filesystem::create_directory(p);
    p = output_path + "intermediate_selections";
    filesystem::create_directory(p);
    p = output_path + "alp";
    filesystem::create_directory(p);
  }

  // N-1 selection
  vector<const char*> selections = {
    "l_{xy} > 200 #mum",
    "|#eta^{#mu}| < 2.5",
    "m_{#mu#mu} #neq m_{J/#Psi},m_{#Psi}",
    "R_{lxy} < 0.05",
  };

  vector<int> color_palette = {
    TColor::GetColor(230, 159, 0),
    TColor::GetColor(86, 180, 233),
    TColor::GetColor(0, 158, 115),
    TColor::GetColor(0, 114, 178),
    TColor::GetColor(213, 94, 0),
  };
  
  map<string, tuple<int, string, int, bool, float, int, float> > file_names = {
    // file name                                  // color  // legend            // linestyle    // signal   // cross-sec  // Ntot
    {"01_muon_siblings/ttj.root",                  {33,    "t#bar{t}j resonant",            kSolid,    false,      395.3,        12540000,    1 }},
    // {"03_muon_siblings/ttmumu.root",               {45,    "tt#mu#mu resonant",       kSolid,    false,      0.02091,      9940000}},

    // {"05_tta_mAlp-0p3GeV.root",                    {kCyan,      "m_{a} = 0.3 GeV",    kSolid,    true,       0.1485,       990000,          0.9999516480656298}},
    {"06_tta_mAlp-0p35GeV.root",                   {color_palette[0],  "m_{a} = 0.35 GeV",   kSolid,     true,       0.1480,       980000,          0.999954381388671}},
    // {"07_tta_mAlp-0p5GeV.root",                    {kSpring-5,  "m_{a} = 0.5 GeV",    kDashed,    true,       0.1483,       1000000,          0.9998929187578673}},
    {"08_tta_mAlp-0p9GeV.root",                    {color_palette[2],  "m_{a} = 0.9 GeV",    kSolid,     true,       0.1486,       1000000,          0.9994465135087311}},
    // {"09_tta_mAlp-1p25GeV.root",                   {kOrange,    "m_{a} = 1.25 GeV",   kDashed,    true,       0.1482,       990000,        0.24705198671664572}},
    {"10_tta_mAlp-2GeV.root",                      {color_palette[3],  "m_{a} = 2 GeV",      kSolid,     true,       0.1483,       1000000,        0.17681064813740055}},
    // {"11_tta_mAlp-4GeV.root",                      {kMagenta,   "m_{a} = 4 GeV",      kDashed,    true,       0.1479,       1000000,        0.0018272180991503392}},
    {"12_tta_mAlp-8GeV.root",                      {color_palette[4],  "m_{a} = 8 GeV",      kSolid,     true,       0.1459,       990000,       0.0010447039648636659}},
    // {"13_tta_mAlp-10GeV.root",                     {kBlue,      "m_{a} = 10 GeV",     kDashed,    true,       0.1449,       980000,        1.35213783949236e-05}},

    {"02_muon_non_siblings/ttj.root",              {36,     "t#bar{t}j non-resonant",       kSolid,     false,      395.3,        12540000,       1 }},
    // {"04_muon_non_siblings/ttmumu.root",           {49,     "tt#mu#mu non-resonant",  kSolid,     false,      0.02091,      9940000}},
  };
  
  map<string, tuple<bool, bool, bool, int, double, double, double, double, string, string>> hist_names = {
    // Rebinned option implies histograms with cutomized binning
//                                logy   logx   rebinned  rebin   xMin    xMax    yMin    yMax    xlabel                       ylabel
    {"minpt-muon_pt",             {true, false,  false,   5,      5,      50,     3.5,   5e5,      "p_{T}^{#mu} [GeV]",         "Events / 1.0 GeV"}},
// {"minpt-muon_pt",             {true, false,  false,   5,      0,      50,     10,   3e5,      "p_{T}^{#mu} [GeV]",         "Events / 1.0 GeV"}},

    };

  vector<string> prefixes = {
    "", // this is for no selections

    "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_",
    "final_selection/final_selection_pt-min0p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_",

  };
  
  vector<string> categories = {
    "os_",
    "os_first_",
  };
  
  map<string, THStack*> stacks_signal;
  map<string, THStack*> stacks_background;
  map<string, int> N_tot_background;
  for(auto &[hist_name, tmp] : hist_names){
    for(auto prefix : prefixes){
      for (auto category : categories) {
        string full_hist_name =  prefix + category + hist_name;
        stacks_signal[full_hist_name] = new THStack();
        stacks_background[full_hist_name] = new THStack();
        N_tot_background[full_hist_name] = 0;
      }
    }
  }
  
  // Calculating total number of scaled background events to properly divide the fraction of events in stack
  if(!weighted){
    for(auto &[file_name_, params] : file_names){
      auto [color, title, line, signal, cross_sec, N_tot, BR] = params;
      if(!signal){
        string file_name = file_name_;
        file_name.erase(0,3);

        base_path = base_path_background;
        auto input_file = TFile::Open((base_path+file_name).c_str());
        
        for(auto &[hist_name, params] : hist_names){
          for (auto prefix : prefixes){
            for (auto category : categories) {
              string full_hist_name = prefix + category + hist_name;
              auto hist = (TH1D*)input_file->Get(full_hist_name.c_str());
              
              auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel, ylabel] = params;
              
              N_tot_background[full_hist_name] += hist->GetEntries()*int_lumi*cross_sec*BR/N_tot;
            }
          }
        }
      }
    }
  }
  
  auto legend_sig = new TLegend(0.40, 0.64, 0.65, 0.88);
  set_legend_layout(legend_sig);
  legend_sig->SetMargin(0.2);
  auto legend_bkg = new TLegend(0.14, 0.76, 0.30, 0.88);
  set_legend_layout(legend_bkg);
  vector<string> in_legend;

  gStyle->SetStatStyle(0);

  for(auto &[file_name_, params] : file_names){
    auto [color, title, line, signal, cross_sec, N_tot, BR] = params;

    string file_name = file_name_;
    file_name.erase(0,3);

    if(signal) base_path = base_path_signal;
    else base_path = base_path_background;
    auto input_file = TFile::Open((base_path+file_name).c_str());
    
    for(auto &[hist_name, params] : hist_names){
      for (auto prefix : prefixes){
        for (auto category : categories) {
          if(category == "os_first_" && !signal) continue;
          string full_hist_name = prefix + category + hist_name;
          
          auto hist = (TH1D*)input_file->Get(full_hist_name.c_str());
          auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel, ylabel] = params;
          
          cout << file_name << ":  " << full_hist_name << endl;
          if(hist->GetEntries() == 0) continue;

          hist->SetLineWidth(2);
          hist->Rebin(rebin);
          if(weighted) {hist->Scale(rebin*int_lumi*cross_sec*BR/N_tot);}
          else{
            if(signal) {hist->Scale(rebin/hist->Integral());}
            else {
              hist->Scale(rebin/hist->Integral());
              hist->Scale((hist->GetEntries()*int_lumi*cross_sec*BR/N_tot)/N_tot_background[full_hist_name]);
            }
          }
          hist->Sumw2(false);

          if(overflow) add_overflow_bin(hist, xMax);
          
          if(signal) {
            hist->SetLineColor(color);
            hist->SetLineStyle(line);
            vector<TH1D*> hists = break_into_smaller_histograms(hist, 0.1, false);
            for(int i=0; i<hists.size(); i++) {
              hists[i]->SetLineColor(color);
              hists[i]->SetLineStyle(line);
              hists[i]->SetLineWidth(2);
              stacks_signal[full_hist_name]->Add(hists[i]);
            }
          } else {
            hist->SetLineColorAlpha(color, 0);
            hist->SetFillColorAlpha(color, 0.7);
            stacks_background[full_hist_name]->Add(hist);
          }
        
          if(find(in_legend.begin(), in_legend.end(), file_name) == in_legend.end()){
            if(signal){legend_sig->AddEntry(hist, title.c_str(), "l");}
            else {legend_bkg->AddEntry(hist, title.c_str(), "f");}
            in_legend.push_back(file_name);
          }
          input_file->cd();
        }
      }
    }
  }

  // TODO: make this possible to run with only signal or only background
  cout << "Saving all plots in: " << output_path << endl;
  gROOT->SetBatch(kTRUE);
  for(auto &[hist_name, params] : hist_names){
    for(auto prefix : prefixes){
      for (auto category : categories) {
        string full_hist_name = prefix + category + hist_name;
        string bkg_hist_name = prefix + category + hist_name;
        if(category == "os_first_") bkg_hist_name = prefix + "os_" + hist_name;
    
        auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel, ylabel] = params;

        auto canvas = new TCanvas("canvas", "canvas");
        canvas->cd();
        canvas->SetBottomMargin(0.15); 
        canvas->SetLeftMargin(0.12); 

        
        stacks_background[bkg_hist_name]->Draw();
        stacks_signal[full_hist_name]->Draw("nostack same");

        set_hist_layout(stacks_background[bkg_hist_name], params, weighted);

        gPad->Modified();
        gPad->RedrawAxis();

        if(logy) canvas->SetLogy();
        if(logx) canvas->SetLogx();

        double x_selection = 0.68;
        draw_legends_and_text(nullptr, legend_bkg, selections, prefix, x_selection, weighted, false);

        canvas->Update();
        
        string file_name = output_path + full_hist_name + ".pdf";
        canvas->SaveAs(file_name.c_str());

        delete canvas;
      }
    }
  }

}
