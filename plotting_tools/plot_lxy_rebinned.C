#include <filesystem>
#include "PlotHelpers.h"

void plot_lxy_rebinned()
{
  // Options for plotting:
  bool weighted = false;
  bool overflow = true;
  int int_lumi = 150e3; // pb-1
  bool include_legend = true;
  bool include_ctau = true;

  string username = getenv("USER");

  string base_path; 
  string base_path_signal =  "/nfs/dust/cms/user/" + username + "/ttalps/signals_lxy_plot/";
  // string base_path_signal =  "/nfs/dust/cms/user/" + username + "/ttalps/signals_ctau-1e5mm/hists/";
  string base_path_background =  "/nfs/dust/cms/user/" + username + "/ttalps/backgrounds_new-dimuon-mass-cuts/hists/";
  string output_path;
  if(username == "lrygaard") {
    if (include_ctau) output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/plots_lxy_legend_ctau/";
    else if (include_legend) output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/plots_lxy_legend/";
    else output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/plots_lxy/";
  }
  // else if(username == "jniedzie") {output_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/";}
  // Only set up for user lrygaard now
  else {cout << "Error: unrecognized user." << endl;}

  vector<const char*> selections = {
    "l_{xy}^{#mu} > 200 #mum",
    "|#eta^{#mu}| < 2.5",
    "p_{T}^{#mu} > 10 GeV",
    "m_{#mu#mu} #neq m_{J/#Psi},m_{#Psi}",
    "R_{lxy} < 0.05",
  };
  // vector<const char*> preselections = {
  //   "l_{xy}^{#mu} > 200 #mum",
  //   "|#eta^{#mu}| < 2.5",
  //   "p_{T}^{#mu} > 5 GeV",
  // };

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

  vector<int> color_palette = {
    TColor::GetColor(230, 159, 0),
    TColor::GetColor(86, 180, 233),
    TColor::GetColor(0, 158, 115),
    TColor::GetColor(0, 114, 178),
    TColor::GetColor(213, 94, 0),

    TColor::GetColor(204,121,167),
    TColor::GetColor(240,228,66),
    TColor::GetColor(0, 0, 0),
  };
  
  map<string, tuple<int, string, int, bool, float, int, float> > file_names = {
    // file name                                  // color  // legend            // linestyle    // signal   // cross-sec  // Ntot
    {"01_muon_siblings/ttj.root",                  {33,    "t#bar{t}j resonant",            kSolid,    false,      395.3,        12540000,    1}},
    // {"03_muon_siblings/ttmumu.root",               {45,    "t#bar{t}#mu#mu resonant",       kSolid,    false,      0.02091,      9940000}},
    // {"07_muon_siblings/tta_mAlp-0p35GeV.root",      {kViolet,    "0.35 GeV pair",     true,       0.1188,        1000000}},
    // {"09_muon_siblings/tta_mAlp-2GeV.root",        {kRed,       "2 GeV pair",       true,       0.1169,        1000000}},
    // {"11_muon_siblings/tta_mAlp-8GeV.root",        {kBlue,      "8 GeV pair",       true,       0.1148,        990000}},
    // {"11_muon_siblings/tta_mAlp-10GeV.root",       {kBlue,      "10 GeV pair",      true,       0.1148,        980000}},

    // // {"05_tta_mAlp-0p3GeV.root",                    {kCyan,               "m_{a} = 0.3 GeV",    kSolid,     true,       0.1185,       990000,      0.9999516480656298}},
    // {"06_tta_mAlp-0p35GeV.root",                   {color_palette[0],    "m_{a} = 0.35 GeV",   kSolid,     true,       0.1180,       980000,       0.999954381388671}},
    // // {"07_tta_mAlp-0p5GeV.root",                 {kSpring-5,           "m_{a} = 0.5 GeV",    kDashed,    true,       0.1183,       1000000,       0.9998929187578673}},
    // {"08_tta_mAlp-0p9GeV.root",                    {color_palette[2],    "m_{a} = 0.9 GeV",    kSolid,     true,       0.1186,       1000000,       0.9994465135087311}},
    // // {"09_tta_mAlp-1p25GeV.root",                {kOrange,             "m_{a} = 1.25 GeV",   kDashed,    true,       0.1182,       990000,     0.24705198671664572}},
    // {"10_tta_mAlp-2GeV.root",                      {color_palette[3],    "m_{a} = 2 GeV",      kSolid,     true,       0.1183,       1000000,      0.17681064813740055}},
    // // {"11_tta_mAlp-4GeV.root",                   {kMagenta,            "m_{a} = 4 GeV",      kDashed,    true,       0.1179,       1000000,    0.0018272180991503392}},
    // {"12_tta_mAlp-8GeV.root",                      {color_palette[4],    "m_{a} = 8 GeV",      kSolid,     true,       0.1159,       990000,   0.0010447039648636659}},
    // // {"13_tta_mAlp-10GeV.root",                     {kBlue,               "m_{a} = 10 GeV",     kDashed,    true,       0.1149,       980000,    1.35213783949236e-05}},

    // {"13_tta_mAlp-0p35GeV_ctau-1e5mm.root",        {color_palette[1],      "m_{a} = 0.35 GeV, c#tau = 1e5 mm",      kSolid,     true,       5,       634373}},
    // {"13_tta_mAlp-0p35GeV_ctau-1e4mm.root",        {color_palette[1],      "m_{a} = 0.35 GeV, c#tau = 1e4 mm",      kSolid,     true,       5,       634373}},
    // {"13_tta_mAlp-0p35GeV_ctau-1e1mm.root",        {color_palette[1],      "m_{a} = 0.35 GeV,",      kSolid,     true,       0.1183,       990000}},

    // {"01_ttj.root",              {kBlue-6,    "ttj",     false,      395.3,        12540000}},
    // {"02_ttmumu.root",           {kOrange+1,  "tt#mu#mu",false,      0.02091,      9940000}},

    {"02_muon_non_siblings/ttj.root",              {36,     "t#bar{t}j non-resonant",       kSolid,     false,      395.3,        12540000,    1}},
    // {"04_muon_non_siblings/ttmumu.root",           {49,     "t#bar{t}#mu#mu non-resonant",  kSolid,     false,      0.02091,      9940000}},
    // {"08_muon_non_siblings/tta_mAlp-0p35GeV.root",  {kViolet+2,    "0.35 GeV non-pair", true,     0.1169,        1000000}},
    // {"10_muon_non_siblings/tta_mAlp-2GeV.root",    {kRed+3,       "2 GeV non-pair",   true,     0.1169,        980000}},
    // {"12_muon_non_siblings/tta_mAlp-8GeV.root",    {kBlue+3,      "8 GeV non-pair",   true,     0.1148,        890000}},
    // {"12_muon_non_siblings/tta_mAlp-10GeV.root",   {kBlue+2,      "10 GeV non-pair",  true,     3.046,        990000}},
  };

  if(include_ctau){
    // file_names["13_tta_mAlp-10GeV.root"]              = {color_palette[0],      "c#tau = 10^{-5} m",      kSolid,     true,       0.1183,       980000};
    file_names["14_tta_mAlp-0p35GeV.root"]            = {color_palette[0],      "c#tau = 10^{-4} m",      kSolid,     true,       0.1183,       980000,   0.999954381388671};
    file_names["15_tta_mAlp-0p35GeV_ctau-1e0mm.root"] = {color_palette[1],      "c#tau = 10^{-3} m",      kSolid,     true,       0.1183,       1000000,  0.999954381388671};
    file_names["16_tta_mAlp-0p35GeV_ctau-1e1mm.root"] = {color_palette[5],      "c#tau = 10^{-2} m",      kSolid,     true,       0.1183,       990000,   0.999954381388671};
    file_names["17_tta_mAlp-0p35GeV_ctau-1e4mm.root"] = {color_palette[6],      "c#tau = 10^{0} m",       kSolid,     true,       0.1183,       1000000,  0.999954381388671};
    // file_names["18_tta_mAlp-0p35GeV_ctau-1e5mm.root"] = {color_palette[4],      "c#tau = 10^{1} m",       kSolid,     true,       0.1183,       1000000};
  }
  
  map<string, tuple<bool, bool, bool, int, double, double, double, double, string, string>> hist_names = {
    // Rebinned option implies histograms with cutomized binning
//
    // {"maxlxy-muon_lxy_rebinned",  {true, false,  true,    1,      0,      110,    0.00005,    5,    "l_{xy}^{#mu} [mm]",         "Events"}},
    {"minlxy-muon_lxy_rebinned",  {true, false,  true,    1,      0,      110,    0.4,     1e5,    "l_{xy}^{#mu} [m]",         "Events"}},
    {"minlxy-muon_lxy_rebinned_extended",  {true, false,  true,    1,      0,      1500,    0.35,    5e4,    "l_{xy}^{#mu} [m]",         "Events"}},
    // {"minlxy-muon_lxy_rebinned_extended_general",  {true, false,  true,    1,      0,      7285,    0.3,    1e3,    "l_{xy}^{#mu} [mm]",         "Events"}},
    {"minlxy-muon_lxy_rebinned_extended_general",  {true, false,  true,    1,      0,      7300,    0.015,    60,    "l_{xy}^{#mu} [m]",         "Events"}},
    // {"minlxy-muon_lxy_rebinned_extended_general",  {true, false,  true,    1,      0,      7285,    0.26,    6.1e2,    "l_{xy}^{#mu} [m]",         "Events"}},
    // {"minlxy-muon_lxy_rebinned_extended_general",  {true, false,  true,    1,      0,      7285,    0.26,    6.1e3,    "l_{xy}^{#mu} [m]",         "Events"}},
  };

  map<string, tuple<bool, bool, bool, int, double, double, double, double, string, string>> hist_names_1widthbins;

  vector<string> prefixes = {
    "", // this is for no selections

    "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_",
  };
  
  vector<string> categories = {
    "os_",
    // "os_first_",
    // "ss_",
    // "single_",
  };

  if(!include_ctau) categories.push_back("os_first_");
  
  map<string, THStack*> stacks_signal;
  map<string, THStack*> stacks_background;
  map<string, int> N_tot_background;
  for(auto &[hist_name, tmp] : hist_names){
    for(auto prefix : prefixes){
      for (auto category : categories) {
        string full_hist_name =  prefix + category + hist_name;
        stacks_signal[full_hist_name] = new THStack();
        stacks_background[full_hist_name] = new THStack();
        if(category == "os_first_") stacks_background[prefix + "os_" + hist_name] = new THStack();
        N_tot_background[full_hist_name] = 0;
        if(hist_name == "minlxy-muon_lxy_rebinned_extended_general") {
          stacks_signal[full_hist_name+"_1widthbins"] = new THStack();
          stacks_background[full_hist_name+"_1widthbins"] = new THStack();
          if(category == "os_first_") stacks_background[prefix + "os_" + hist_name+"_1widthbins"] = new THStack();
        }
        if(hist_name == "minlxy-muon_lxy_rebinned_extended") {
          stacks_signal[full_hist_name+"_outer-tracker"] = new THStack();
          stacks_background[full_hist_name+"_outer-tracker"] = new THStack();
          if(category == "os_first_") stacks_background[prefix + "os_" + hist_name+"_outer-tracker"] = new THStack();
        }
      }
    }
  }
  
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
  
  // auto legend = new TLegend(0.14, 0.73, 0.70, 0.83);
  TLegend *legend;
  if(include_ctau) legend = new TLegend(0.46, 0.58, 0.65, 0.82);
  else legend = new TLegend(0.44, 0.64, 0.65, 0.88);
  // auto legend = new TLegend(0.44, 0.64, 0.65, 0.88);
  // auto legend = new TLegend(0.44, 0.58, 0.65, 0.88);
  // auto legend = new TLegend(0.44, 0.58, 0.65, 0.88);
  legend->SetNColumns(1);
  legend->SetBorderSize(0);
  legend->SetTextSize(0.050);
  legend->SetTextFont(42);
  legend->SetMargin(0.2);
  double x_max = 0.35;
  // auto legend_bkg = new TLegend(0.14, 0.83, x_max, 0.88);
  auto legend_bkg = new TLegend(0.15, 0.76, 0.30, 0.88);
  legend_bkg->SetNColumns(1);
  legend_bkg->SetBorderSize(0);
  legend_bkg->SetTextSize(0.050);
  legend_bkg->SetTextFont(42);
  vector<string> in_legend;
  TLatex text_header(0.53, 0.91, "L = 150 fb^{-1}, #sqrt{s} = 13 TeV");
  text_header.SetNDC(kTRUE);
  text_header.SetTextSize(0.050);
  text_header.SetTextFont(42);

  // TLatex selection_text(0.14, 0.63, "Selections: l_{xy}^{#mu} > 200 #mum, |#eta^{#mu}| < 2.5, p_{T}^{#mu} > 10 GeV, m_{#mu#bar{#mu}}, R_{lxy} < 0.05");
  // TLatex preselection_text(0.14, 0.63, "Selections: l_{xy}^{#mu} > 200 #mum, |#eta^{#mu}| < 2.5, p_{T}^{#mu} > 5 GeV");
  TLatex selection_text(0.14, 0.68, "l_{xy}^{#mu} > 200 #mum, |#eta^{#mu}| < 2.5, p_{T}^{#mu} > 10 GeV, m_{#mu#mu} #neq m_{J/#Psi},m_{#Psi}, R_{lxy} < 0.05");
  TLatex preselection_text(0.14, 0.68, "l_{xy}^{#mu} > 200 #mum, |#eta^{#mu}| < 2.5, p_{T}^{#mu} > 5 GeV");
  selection_text.SetNDC(kTRUE);
  selection_text.SetTextSize(0.050);
  selection_text.SetTextFont(42);
  preselection_text.SetNDC(kTRUE);
  preselection_text.SetTextSize(0.050);
  preselection_text.SetTextFont(42);

  auto legend_lines = new TLegend(0.14, 0.79, 0.89, 0.83);
  legend_lines->SetNColumns(2);
  legend_lines->SetBorderSize(0);
  legend_lines->SetTextSize(0.050);
  legend_lines->SetTextFont(42);
  legend_lines->AddEntry((TObject*)0, "Resonsonant", "l");
  legend_lines->AddEntry((TObject*)0, "Non-resonsonant", "l");

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
          string full_hist_name = prefix + category + hist_name;
          if(category == "os_first_" && !signal) full_hist_name = prefix + "os_" + hist_name;
          
          auto hist = (TH1D*)input_file->Get(full_hist_name.c_str());
          auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel, ylabel] = params;
          
          cout << file_name << ":  " << full_hist_name << endl;
          if(hist->GetEntries() == 0) continue;
          
          if(rebinned)
          {
            vector<int> lxy_bins = rebin_histogram(hist, hist_name);
            if (hist_name == "minlxy-muon_lxy_rebinned_extended_general")
            {
              TH1D* hist_new = get_hist_with_same_width_bins(hist, full_hist_name, lxy_bins);
              hist_new->Rebin(rebin);
              if(weighted) {hist_new->Scale(rebin*int_lumi*cross_sec*BR/N_tot);}
              else{
                if(signal) {hist_new->Scale(rebin/hist_new->Integral());}
                else {
                  hist_new->Scale(rebin/hist_new->Integral());
                  hist_new->Scale((hist_new->GetEntries()*int_lumi*cross_sec*BR/N_tot)/N_tot_background[full_hist_name]);
                }
              }
              hist_new->Sumw2(false);
              hist_new->SetLineWidth(2);
              if(signal) {
                hist_new->SetLineColor(color);
                hist_new->SetLineStyle(line);
                stacks_signal[full_hist_name+"_1widthbins"]->Add(hist_new);
              }
              else {
                hist_new->SetLineColorAlpha(color, 0);
                hist_new->SetFillColorAlpha(color, 0.7);
                stacks_background[full_hist_name+"_1widthbins"]->Add(hist_new);
              }
              get<5>(params) = lxy_bins.size();
              hist_names_1widthbins[hist_name+"_1widthbins"] = params;
            }
            if (hist_name == "minlxy-muon_lxy_rebinned_extended"){
              TH1D* hist_new = get_lxy_with_outer_tracker(hist, full_hist_name, lxy_bins, 150);
              hist_new->Rebin(rebin);
              if(weighted) {hist_new->Scale(rebin*int_lumi*cross_sec*BR/N_tot);}
              else{
                if(signal) {hist_new->Scale(rebin/hist_new->Integral());}
                else {
                  hist_new->Scale(rebin/hist_new->Integral());
                  hist_new->Scale((hist_new->GetEntries()*int_lumi*cross_sec*BR/N_tot)/N_tot_background[full_hist_name]);
                }
              }
              hist_new->Sumw2(false);
              hist_new->SetLineWidth(2);
              if(signal) {
                hist_new->SetLineColor(color);
                hist_new->SetLineStyle(line);
                stacks_signal[full_hist_name+"_outer-tracker"]->Add(hist_new);
              }
              else {
                hist_new->SetLineColorAlpha(color, 0);
                hist_new->SetFillColorAlpha(color, 0.7);
                stacks_background[full_hist_name+"_outer-tracker"]->Add(hist_new);
              }
              get<5>(params) = lxy_bins.size();
              hist_names_1widthbins[hist_name+"_outer-tracker"] = params;
            }

          }

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
            stacks_signal[full_hist_name]->Add(hist);}
          else {
            hist->SetLineColorAlpha(color, 0);
            hist->SetFillColorAlpha(color, 0.7);
            std::cout << full_hist_name << std::endl;
            stacks_background[full_hist_name]->Add(hist);
          }
        
          if(find(in_legend.begin(), in_legend.end(), file_name) == in_legend.end()){
            if(signal){legend->AddEntry(hist, title.c_str(), "l");}
            else {legend_bkg->AddEntry(hist, title.c_str(), "f");}
            in_legend.push_back(file_name);
          }
          input_file->cd();
        }
      }
    }
  }

  for(auto &[hist_name, params] : hist_names_1widthbins){
    hist_names[hist_name] = params;
  }

  // TODO: make this possible to run with only signal or only background
  cout << "Saving all plots in: " << output_path << endl;
  // gROOT->SetBatch(kTRUE);
  TH1F *ghost_hist;
  for(auto &[hist_name, params] : hist_names){
    for(auto prefix : prefixes){
      for (auto category : categories) {
        string full_hist_name = prefix + category + hist_name;
        string bkg_hist_name = prefix + category + hist_name;
        if(category == "os_first_") bkg_hist_name = prefix + "os_" + hist_name;
    
        auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel, ylabel] = params;

        auto canvas = new TCanvas("canvas", "canvas", 650, 500);
        canvas->cd();
        canvas->SetBottomMargin(0.15); 
        canvas->SetLeftMargin(0.13); 
        canvas->SetRightMargin(0.03); 

        if(hist_name == "minlxy-muon_lxy_rebinned_extended_general_1widthbins")
        {
          // This is to update the x-axis region which couldn't be done for the mass.
          int n_bins = 4;
          float binList[] = {0, 1, 2, 3, 4};
          ghost_hist = new TH1F("hist","",n_bins, binList);
          THStack* ghost_stack = new THStack();
          ghost_stack->Add(ghost_hist);
          ghost_stack->Draw();
          set_hist_layout(ghost_stack, params);
          ghost_stack->GetXaxis()->ChangeLabel(2,-1,-1,-1,-1,-1,"0.11");
          ghost_stack->GetXaxis()->ChangeLabel(3,-1,-1,-1,-1,-1,"1.3");
          ghost_stack->GetXaxis()->ChangeLabel(4,-1,-1,-1,-1,-1,"3.0");
          ghost_stack->GetXaxis()->ChangeLabel(5,-1,-1,-1,-1,-1,"7.3");
          ghost_stack->GetXaxis()->SetNdivisions(4);
          stacks_background[bkg_hist_name]->Draw("same");

          vector<string> bin_labels = {"Inner tracker", "Outer tracker", "Calorimeter", "Muon system"};
          TLatex* l = new TLatex();
          vector<double> y;
          if (weighted) y = {0.71, 0.45, 0.40, 0.33};
          else y = {0.57, 0.49, 0.47, 0.47};
          // vector<double> y = {0.76, 0.41, 0.19, 0.19};
          // vector<double> x = {0.14, 0.32, 0.52, 0.705};
          // vector<double> x = {0.15, 0.35, 0.56, 0.75};
          vector<double> x = {0.15, 0.35, 0.56, 0.76};
          for (int i=0; i<n_bins; i++){
            // double x = i*0.2+0.12;
            l->SetNDC(kTRUE);
            l->SetTextSize(0.050);
            l->SetTextFont(42);
            l->DrawLatex(x[i], y[i], bin_labels[i].c_str());
          }
        }
        else if(hist_name == "minlxy-muon_lxy_rebinned_extended_outer-tracker"){
          int n_bins = 7;
          float binList[8] = {0, 2, 10, 24, 31, 70, 110, 150}; // mm
          // float binList[] = {0, 1, 2, 3, 4};
          ghost_hist = new TH1F("hist","",n_bins, binList);
          THStack* ghost_stack = new THStack();
          ghost_stack->Add(ghost_hist);
          ghost_stack->Draw();
          auto hbox = new TBox(115, -0.3, 145, 0.3);
          // hbox->Draw("same");
          hbox->SetFillColor(kRed);
          set_hist_layout(ghost_stack, params);
          ghost_stack->GetXaxis()->ChangeLabel(2,-1,0);
          ghost_stack->GetXaxis()->ChangeLabel(3,-1,-1,-1,-1,-1,"0.02");
          ghost_stack->GetXaxis()->ChangeLabel(4,-1,0);
          ghost_stack->GetXaxis()->ChangeLabel(5,-1,-1,-1,-1,-1,"0.04");
          ghost_stack->GetXaxis()->ChangeLabel(6,-1,0);
          ghost_stack->GetXaxis()->ChangeLabel(7,-1,-1,-1,-1,-1,"0.06");
          ghost_stack->GetXaxis()->ChangeLabel(8,-1,0);
          ghost_stack->GetXaxis()->ChangeLabel(9,-1,-1,-1,-1,-1,"0.08");
          ghost_stack->GetXaxis()->ChangeLabel(10,-1,0);
          ghost_stack->GetXaxis()->ChangeLabel(11,-1,0);
          // ghost_stack->GetXaxis()->ChangeLabel(11,-1,-1,-1,-1,-1,"0.10");
          ghost_stack->GetXaxis()->ChangeLabel(12,-1,-1,-1,-1,-1,"0.11");
          ghost_stack->GetXaxis()->ChangeLabel(13,-1,0);
          ghost_stack->GetXaxis()->ChangeLabel(14,-1,0);
          // ghost_stack->GetXaxis()->ChangeLabel(14,-1,-1,-1,-1,-1,"Outer tracker");
          ghost_stack->GetXaxis()->ChangeLabel(15,-1,0);
          // ghost_stack->GetXaxis()->ChangeLabel(16,-1,0);
          ghost_stack->GetXaxis()->ChangeLabel(16,-1,-1,-1,-1,-1,"1.3");
          ghost_stack->GetXaxis()->SetTickLength(0);

          ghost_stack->GetXaxis()->SetNdivisions(20);
          stacks_background[bkg_hist_name]->Draw("same");

          auto axis1 = new TGaxis(0, 0, 110, 0, 0, 110, 11);
          axis1->Draw();
          axis1->SetLabelSize(0);

          TLatex* l = new TLatex();
          l->SetNDC(kTRUE);
          l->SetTextSize(0.050);
          l->SetTextFont(42);
          l->DrawLatex(0.76, 0.33, "Outer tracker");
          // l->DrawLatex(0.79, 0.10, "Outer tracker");
        }
        else{
          std::cout << bkg_hist_name << std::endl;
          stacks_background[bkg_hist_name]->Draw();
        }
        stacks_signal[full_hist_name]->Draw("nostack same");
        if(hist_name == "minlxy-muon_lxy_rebinned"){
          stacks_background[bkg_hist_name]->GetXaxis()->ChangeLabel(2,-1,-1,-1,-1,-1,"0.02");
          stacks_background[bkg_hist_name]->GetXaxis()->ChangeLabel(3,-1,-1,-1,-1,-1,"0.04");
          stacks_background[bkg_hist_name]->GetXaxis()->ChangeLabel(4,-1,-1,-1,-1,-1,"0.06");
          stacks_background[bkg_hist_name]->GetXaxis()->ChangeLabel(5,-1,-1,-1,-1,-1,"0.08");
          stacks_background[bkg_hist_name]->GetXaxis()->ChangeLabel(6,-1,-1,-1,-1,-1,"0.10");
        }

        set_hist_layout(stacks_background[bkg_hist_name], params);

        gPad->Modified();
        gPad->RedrawAxis();

        if(logy) canvas->SetLogy();
        if(logx) canvas->SetLogx();
        TLatex latex;
        latex.SetTextSize(0.050);
        latex.SetTextFont(42);
        latex.SetNDC(kTRUE);
        if(weighted) latex.DrawLatex(0.53, 0.91, "L = 150 fb^{-1}, #sqrt{s} = 13 TeV");
        else latex.DrawLatex(0.73, 0.91, "#sqrt{s} = 13 TeV");
        if(include_legend){
          legend->Draw();
          legend_bkg->Draw();
          // TLatex latex;
          // latex.SetTextSize(0.050);
          // latex.SetTextFont(42);
          // latex.SetNDC(kTRUE);
          double y = 0.84;
          double x = 0.74;
          if(prefix.substr(0,15) == "final_selection") {
            // selection_text.Draw();
            for(auto sel : selections){
              latex.DrawLatex(x, y, sel);
              y -= 0.06;
            }
          }
          else {
            preselection_text.Draw();
            // for(auto sel : preselections){
            //   latex.DrawLatex(0.7, y, sel);
            //   y -= 0.05;
            // }
          }
          if(include_ctau){
            latex.DrawLatex(0.46, 0.84, "m_{a} = 0.35 GeV");
          }
        }

        canvas->Update();

        if(hist_name == "minlxy-muon_lxy_rebinned_extended_outer-tracker"){
          auto hbox = new TBox(129.5, -0.5, 131, 0.3);
          hbox->Draw("same");
          hbox->SetFillColor(kWhite);
          TLine *line = new TLine(0.85,0.125,0.86,0.175);
          line->SetNDC(kTRUE);
          line->SetLineWidth(2);
          line->Draw();
          line = new TLine(0.86,0.125,0.87,0.175);
          line->SetNDC(kTRUE);
          line->SetLineWidth(2);
          line->Draw();
        }
        
        string file_name = output_path + full_hist_name + ".pdf";
        canvas->SaveAs(file_name.c_str());

        delete canvas;
        if(hist_name == "dimuon_mass" || hist_name == "dimuon_mass_log")
        {
          delete ghost_hist;
        }
      }
    }
  }

}
