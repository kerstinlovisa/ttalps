#include <filesystem>

TH1D* get_hist_with_same_width_bins(TH1D* input_hist, string input_hist_name, vector<int> lxy_bins, vector<string> bin_labels)
{
  int n_bins = lxy_bins.size();
  TH1D* hist = new TH1D((input_hist_name+"_1widthbins").c_str(), (input_hist_name+"_1widthbins").c_str(), n_bins-1, 0, n_bins-1);
  for(int i=0; i<n_bins-1; i++)
  {
    hist->SetBinContent(i+1, input_hist->GetBinContent(i+1));
    TAxis* a = hist->GetXaxis();
    a->ChangeLabel(1,-1,-1,-1,-1,-1,"-#pi");
  }
  hist->GetXaxis()->SetLabelSize(0.04);
  return hist;
}

void add_overflow_bin(TH1D* hist, double xMax)
{
  int maxbin = hist->FindBin(xMax);
  double content = 0;
  for(int i=maxbin-1; i<hist->GetNbinsX()+1; i++){
    content+=hist->GetBinContent(i);
  }
  // hist->GetXaxis()->SetLimits(xMin, xMax);
  hist->SetBinContent(hist->FindBin(xMax)-1, content);
}

vector<int> rebin_histogram(TH1D* hist, string hist_name)
{
  vector<int> lxy_bins;
  if (hist_name == "minlxy-muon_lxy_rebinned") {lxy_bins = {0, 2, 10, 24, 31, 70, 110};} 
  if (hist_name == "maxlxy-muon_lxy_rebinned") {lxy_bins = {0, 2, 10, 24, 31, 70, 110};} 
  if (hist_name == "minlxy-muon_lxy_rebinned_extended") {lxy_bins = {0, 2, 10, 24, 31, 70, 110, 1310, 2950, 7285};} 
  if (hist_name == "minlxy-muon_lxy_rebinned_extended_gen") {lxy_bins = {0, 110, 1310, 2950, 7285};}
  if (hist_name == "minlxy-muon_lxy_rebinned_extended_general") {lxy_bins = {0, 110, 1310, 2950, 7285};}
  for(int i=0; i<hist->GetNbinsX(); i++){
    hist->SetBinContent(i+1, hist->GetBinContent(i+1)/(lxy_bins[i+1]-lxy_bins[i]));
  }
  return lxy_bins;
}

void set_hist_layout(THStack* stack, tuple<bool, bool, bool, int, double, double, double, double, string, string> params)
{
  auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel, ylabel] = params;
  stack->GetXaxis()->SetLimits(xMin, xMax);
  if(yMax != 0){
    stack->SetMaximum(yMax);
    stack->SetMinimum(yMin);
  }
  stack->GetXaxis()->SetTitle(xlabel.c_str());
  stack->GetXaxis()->SetTitleSize(0.04);
  stack->GetYaxis()->SetTitleSize(0.04);
  stack->GetYaxis()->SetTitle(ylabel.c_str());
  stack->GetXaxis()->SetRangeUser(xMin, xMax);
}

void plot_signal_histograms()
{
  // Options for plotting:
  bool weighted = true;
  bool overflow = true;
  bool selection_description = true;

  string username = getenv("USER");

  // string base_path = "/nfs/dust/cms/user/" + username + "/ttalps/signals_ctau-default_non-muon-mothers/hists/";
  // string base_path = "/nfs/dust/cms/user/" + username + "/ttalps/signals_ctau-default_muon-status/hists/";
  string base_path = "/nfs/dust/cms/user/" + username + "/ttalps/signals_ctau-default_non-prompt-selection/hists/";
  // string base_path = "/nfs/dust/cms/user/" + username + "/ttalps/reweighted/hists/";
  // string base_path = "/nfs/dust/cms/user/jalimena/ttalps/hists/backup_lovisa/";
  string output_path;
  // if(username == "lrygaard") {output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/plots_signal_fs/";}
  if(username == "lrygaard") {output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/plots_signal_non-prompt-selection/";}
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

  int int_lumi = 150e3; // pb-1

  vector<int> lxy_bins;
  
  map<string, tuple<int, string, bool, float, int> > file_names = {
    // file name    
    // {"06_muon_siblings/tta_mAlp-8GeV_ctau-0p000010mm.root",{kGreen+2,     "0.3 GeV non-pair", true,     0.1188,        950000}},
    {"05_muon_siblings/tta_mAlp-0p3GeV.root",      {kSpring-5,  "0.3 GeV pair",     true,       0.1173,        9900000}},
    {"07_muon_siblings/tta_mAlp-0p5GeV.root",      {kViolet,    "0.5 GeV pair",     true,       0.1188,        1000000}},
    // {"09_muon_siblings/tta_mAlp-2GeV.root",        {kRed,       "2 GeV pair",       true,       0.1188,        1000000}},
    // {"11_muon_siblings/tta_mAlp-8GeV.root",        {kBlue,      "8 GeV pair",       true,       0.1148,        990000}},
    // {"11_muon_siblings/tta_mAlp-10GeV.root",       {kBlue,      "10 GeV pair",      true,       0.1148,        980000}},

    // {"03_tta_mAlp-0p2GeV.root",                    {kSpring-5,  "m_{a} = 0.2 GeV",        true,       0.117,        970000}},
    // {"03_tta_mAlp-0p3GeV.root",                    {kSpring-5,  "m_{a} = 0.3 GeV",        true,       0.1173,       990000}},
    // {"05_tta_mAlp-0p315GeV.root",                  {kSpring-5,  "m_{a} = 0.315 GeV",      true,       0.1169,       1000000}},
    // {"05_tta_mAlp-0p35GeV.root",                   {kSpring-5,    "m_{a} = 0.35 GeV",       true,       0.1169,       1000000}},
    // {"06_tta_mAlp-0p5GeV.root",                    {kOrange,    "m_{a} = 0.5 GeV",        true,       0.1181,       1000000}},
    // {"06_tta_mAlp-0p9GeV.root",                    {kRed+2,     "m_{a} = 0.9 GeV",        true,       0.1181,       1000000}},
    // {"07_tta_mAlp-1p25GeV.root",                   {kOrange,       "m_{a} = 1.25 GeV",       true,       0.1188,       1000000}},
    // {"07_tta_mAlp-2GeV.root",                      {kMagenta, "m_{a} = 2 GeV",          true,       0.1188,       1000000}},
    // {"07_tta_mAlp-4GeV.root",                      {kMagenta,   "m_{a} = 4 GeV",          true,       0.1188,       1000000}},
    // {"08_tta_mAlp-8GeV.root",                      {kBlue,      "m_{a} = 8 GeV",          true,       0.1163,       990000}},
    // {"11_tta_mAlp-10GeV.root",                     {kCyan,      "m_{a} = 10 GeV",         true,       0.1154,       980000}},

    // {"06_muon_non_siblings/tta_mAlp-8GeV_ctau-0p000010mm.root",{kGreen+2,     "0.3 GeV non-pair", true,     0.1188,        950000}},
    // {"06_muon_non_siblings/tta_mAlp-0p9GeV.root",{kGreen+2,     "0.3 GeV non-pair", true,     0.1188,        950000}},
    {"06_muon_non_siblings/tta_mAlp-0p3GeV.root",  {kGreen+2,     "0.3 GeV non-pair",     true,     0.1173,        990000}},
    {"08_muon_non_siblings/tta_mAlp-0p5GeV.root",  {kViolet+2,    "0.5 GeV non-pair",     true,     0.1188,        1000000}},
    // {"10_muon_non_siblings/tta_mAlp-2GeV.root",    {kRed+3,       "2 GeV non-pair",       true,     0.1188,        1000000}},
    // {"12_muon_non_siblings/tta_mAlp-8GeV.root",    {kBlue+7,      "8 GeV non-pair",   true,     0.1148,        890000}},
    // {"12_muon_non_siblings/tta_mAlp-10GeV.root",   {kBlue+2,      "10 GeV non-pair",  true,     3.046,        990000}},
  };
  
  map<string, tuple<bool, bool, bool, int, double, double, double, double, string, string>> hist_names = {
    // Rebinned option implies histograms with cutomized binning
//                                logy   logx   rebinned  rebin   xMin    xMax    yMin    yMax    xlabel                       ylabel
    // {"muons_pt",                  {true, false,  false,   1,      0,      50,     10,   3e5,      "p_{T}^{#mu} [GeV]",         "Muons / 0.5 GeV"}},
    // {"first_mother_pt",           {true, false,  false,   1,      0,      50,     10,   3e5,      "p_{T}^{a} [GeV]",         "Events / 0.5 GeV"}},
    // {"first_mother_eta",          {false, false,  false,   1,      -3,      3,     0,   2000,      "#eta",         "Events "}},
    // {"maxlxy-muon_pt",            {true, false,  false,   5,      0,      50,     10,   3e5,      "p_{T}^{#mu} [GeV]",         "Events / 1.0 GeV"}},
    // {"minlxy-muon_pt",            {true, false,  false,   5,      0,      50,     10,   3e5,      "p_{T}^{#mu} [GeV]",         "Events / 1.0 GeV"}},
    // {"minpt-muon_pt",             {true, false,  false,   5,      0,      200,    1000,   2e5,      "p_{T}^{#mu} [GeV]",         "Events / 1.0 GeV"}},
    // // {"maxlxy-muon_pz",            {true, false,  false,   10,     0,      100,    0,      0,      "p_{z}^{#mu} [GeV]",      "Events / GeV"}},
    // // {"minlxy-muon_pz",            {true, false,  false,   10,     0,      100,    0,      0,      "p_{z}^{#mu} [GeV]",      "Events / GeV"}},
    // {"maxlxy-muon_lxy",           {true, false,  false,   20,     0,      150,      5,    4e6,    "l_{xy}^{#mu} [mm]",         "Events / 2.0 mm"}},
    // {"minlxy-muon_lxy",           {true, false,  false,   20,     0,      150,     10,    6e6,    "l_{xy}^{#mu} [mm]",         "Events / 2.0 mm"}},
    // {"minlxy-muon_lxy_logx",      {true, true,   false,    1,      0.0001, 100,     10,    6e6,    "l_{xy}^{#mu} [mm]",         "Events / 2.0 mm"}},
    // {"maxlxy-muon_lxy_rebinned",  {true, false,  true,    1,      0,      110,    0.00005,    5,    "l_{xy}^{#mu} [mm]",         "Events"}},
    // {"minlxy-muon_lxy_rebinned",  {true, false,  true,    1,      0,      110,    0.00005,    5,    "l_{xy}^{#mu} [mm]",         "Events"}},
    // {"minlxy-muon_lxy_rebinned_extended",  {true, false,  true,    1,      0,      7285,    0.1,    1e5,    "l_{xy}^{#mu} [mm]",         "Events"}},
    // {"maxlxy-muon_lxy_rebinned_extended",  {true, false,  true,    1,      0,      7285,    0.1,    1e5,    "l_{xy}^{#mu} [mm]",         "Events"}},
    // {"minlxy-muon_lxy_rebinned_extended_general",  {true, false,  true,    1,      0,      7285,    0.1,    1e4,    "l_{xy}^{#mu} [mm]",         "Events"}},
    // {"maxlxy-muon_lxy_2bins",     {true, false,  true,    1,      0,      110,    0.1,    2e5,    "l_{xy}^{#mu} [mm]",         "Events / mm"}},
    // {"minlxy-muon_lxy_2bins",     {true, false,  true,    1,      0,      110,    0.1,    2e5,    "l_{xy}^{#mu} [mm]",         "Events / mm"}},
    // {"maxlxy-muon_lz",            {true, false,  false,   1,      0,      50,     0,      0,      "l_{z}^{#mu} [mm]",       "Events / mm"}},
    // {"minlxy-muon_lz",            {true, false,  false,   1,      0,      50,     0,      0,      "l_{z}^{#mu} [mm]",       "Events / mm"}},
    // {"maxlxy-muon_lxyz",          {true, false,  false,   1,      0,      100,    0,      0,      "l_{xyz}^{#mu} [mm]",        "Events / mm"}},
    // {"minlxy-muon_lxyz",          {true, false,  false,   1,      0,      100,    0,      0,      "l_{xyz}^{#mu} [mm]",        "Events / mm"}},
    // {"maxlxy-muon_ctau",          {true, false,  false,   1,      0,      100,    0,      0,      "Muon c#tau [mm]",           "Events / mm"}},
    // {"minlxy-muon_ctau",          {true, false,  false,   1,      0,      100,    0,      0,      "Muon c#tau [mm]",           "Events / mm"}},
    // {"maxlxy-muon_boost",         {true, false,  false,   20,     0,      120,    0,      0,      "Muon #gamma#beta",          "Events / GeV"}},
    // {"minlxy-muon_boost",         {true, false,  false,   20,     0,      120,    0,      0,      "Muon #gamma#beta",          "Events / GeV"}},
    // {"dimuon_pt",                 {true, false,  false,   10,     0,      100,    0,      0,      "Dimuon p_{T}[GeV]",         "Events / GeV"}},
    // {"dimuon_pz",                 {true, false,  false,   10,     0,      100,    0,      0,      "Dimuon p_{z}[GeV]",      "Events / GeV"}},
    {"dimuon_mass",               {true, false,  false,   1,      0.1,    1,      0.01,      1e6,    "m_{#mu#bar{#mu}} [GeV]",      "Events / GeV"}},
    {"minlxy-muon_mass",               {true, false,  false,   1,      0.1,    1,      0.01,      1e6,    "m_{#mu#bar{#mu}} [GeV]",      "Events / GeV"}},
    // {"maxlxy-muon_mass",               {true, false,  false,   1,      0.1,    1,      0.01,      1e6,    "m_{#mu#bar{#mu}} [GeV]",      "Events / GeV"}},
    // {"dimuon_mass_log",           {true, true,   false,   1,      0.25,   10,     10,      1e5,    "m_{#mu#bar{#mu}} [GeV]",          "Events"}},
    // {"first_mother_mass",         {true, false,  false,   1,      0.1,    1,      1,      1e6,     "m_{a} [GeV]",      "Events / GeV"}},
    // {"first_mother_mass_log",     {true, true,   false,   1,      0.25,   10,     1,      1e9,     "m_{a} [GeV]",          "Events / GeV"}},
    // {"dimuon_deltaR",             {true, false,  false,   1,      0,      1,      1,      2e5,    "#Delta R(#mu#bar{#mu})",            "Events"}},
    // {"dimuon_deltaPhi",           {true, false,  false,   1,     -4,      4,      0,      0,      "#Delta #phi(#mu#bar{#mu})",              "Events"}},
    // {"dimuon_deltalxy",           {true, false,  false,   1,      0,      0.001,  1,      1e6,    "#Delta l_{xy}(#mu#bar{#mu}) [mm]",          "Events / mm"}},
    // {"dimuon_deltalxy_diff_abs",  {true, false,  false,   1,      0,      10,     1,      1e6,    "|l_{xy}^{#mu} - l_{xy}^{#bar{#mu}}| [mm]",  "Events / mm"}},
    // {"dimuon_deltalxy_ratio_abs", {true, false,  false,   5,     0,      1.05,     1,    1e9,    "R_{lxy}",         "Events / 0.05"}},
    // {"dimuon_deltapt",            {true, false,  false,   1,      0,      100,    1,      1e5,     "#Delta p_{T}(#mu#bar{#mu}) [mm]",          "Events / GeV"}},
  };

  map<string, tuple<bool, bool, bool, int, double, double, double, double, string, string>> hist_names_1widthbins;

  vector<string> prefixes = {
    "", // this is for no selections
    // "alp/alp_", 
    // "alp/alp_eta-max1p0_", 
    // "alp/alp_eta-max0p5_", 
    // "alp/alp_eta-max0p1_", 

    // "intermediate_selections/sel_pt-min10p0GeV_",
    // "intermediate_selections/sel_mass-cuts_",

    // "intermediate_selections/sel_deltalxy-max0p3mm_",
    // "intermediate_selections/sel_deltalxy_ratio_abs-max0p05_",

    // "intermediate_selections/sel_eta-max0p1_",

    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_",

    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy-max0p3mm_",
    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_",
    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p1_",
    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p5_",

    // // "final_selection/final_selection_pt-min10p0GeV_deltalxy-max0p3mm_",
    // "final_selection/final_selection_pt-min10p0GeV_deltalxy_ratio_abs-max0p05_",

    // "final_selection/final_selection_mass-cuts_deltalxy-max0p3mm_",
    // "final_selection/final_selection_mass-cuts_deltalxy_ratio_abs-max0p05_",

  };
  
  vector<string> categories = {
    "os_",
    // "ss_",
    // "single_",
    "os_first_",
    "os_first_mother_",
    "os_last_mother_",
  };
  
  map<string, THStack*> stacks_signal;
  map<string, int> N_tot_background;
  for(auto &[hist_name, tmp] : hist_names){
    for(auto prefix : prefixes){
      for (auto category : categories) {
        string full_hist_name =  prefix + category + hist_name;
        stacks_signal[full_hist_name] = new THStack();
        if(hist_name == "minlxy-muon_lxy_rebinned_extended_gen") stacks_signal[full_hist_name+"_1widthbins"] = new THStack();
        if(hist_name == "minlxy-muon_lxy_rebinned_extended_general") stacks_signal[full_hist_name+"_1widthbins"] = new THStack();
      }
    }
  }
  
  auto legend = new TLegend(0.11, 0.83, 0.89, 0.88);
  legend->SetNColumns(4);
  legend->SetBorderSize(0);
  legend-> SetTextSize(0.036);
  vector<string> in_legend;
  TLatex text(0.6, 0.91, "L = 150 fb^{-1}, #sqrt{s} = 13 TeV");
  text.SetNDC(kTRUE);
  text.SetTextSize(0.036);
  TLatex selection_text(0.13, 0.78, "#bf{Selection: p_{T}^{#mu} < 10 GeV, di-muon mass, R_{lxy} < 0.05}");
  selection_text.SetNDC(kTRUE);
  selection_text.SetTextSize(0.036);
  
  gStyle->SetStatStyle(0);
  gStyle->SetTitleStyle(0);
  gROOT->ForceStyle();

  if(!weighted){
    for(auto &[file_name_, params] : file_names){
      auto [color, title, signal, cross_sec, N_tot] = params;
        if(!signal){
        string file_name = file_name_;
        file_name.erase(0,3);

        auto input_file = TFile::Open((base_path+file_name).c_str());
        
        for(auto &[hist_name, params] : hist_names){
          for (auto prefix : prefixes){
            for (auto category : categories) {
              string full_hist_name = prefix + category + hist_name;
              auto hist = (TH1D*)input_file->Get(full_hist_name.c_str());
              
              auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel, ylabel] = params;
              
              N_tot_background[full_hist_name] += hist->GetEntries()*int_lumi*cross_sec/N_tot;
            }
          }
        }
      }
    }
  }

  for(auto &[file_name_, params] : file_names){
    auto [color, title, signal, cross_sec, N_tot] = params;

    string file_name = file_name_;
    file_name.erase(0,3);

    auto input_file = TFile::Open((base_path+file_name).c_str());
    
    for(auto &[hist_name, params] : hist_names){
      for (auto prefix : prefixes){
        for (auto category : categories) {
          string full_hist_name = prefix + category + hist_name;
          auto hist = (TH1D*)input_file->Get(full_hist_name.c_str());
          auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel, ylabel] = params;
          
          cout << file_name << ":  " << full_hist_name << endl;
          if(hist->GetEntries() == 0) continue;
          
          if(rebinned)
          {
            rebin_histogram(hist, hist_name);
            if (hist_name == "minlxy-muon_lxy_rebinned_extended_general")
            {
              vector<string> bin_labels = {"Inner tracker 0-110", "Outer tracker 110-1300", "Calorimiter 1300-3000", "Muon system 3000-7300"};
              TH1D* hist_new = get_hist_with_same_width_bins(hist, full_hist_name, lxy_bins, bin_labels);
              hist_new->SetLineColor(color);
              hist_new->SetLineWidth(2);
              hist_new->Rebin(rebin);
              if(weighted) {hist_new->Scale(rebin*int_lumi*cross_sec/N_tot);}
              else{
                hist_new->Scale(rebin/hist_new->Integral());
              }
              hist_new->Sumw2(false);
              stacks_signal[full_hist_name+"_1widthbins"]->Add(hist_new);
              get<5>(params) = lxy_bins.size();
              hist_names_1widthbins[hist_name+"_1widthbins"] = params;
            }
          }

          // hist->SetLineColor(color);
          hist->SetLineWidth(2);
          hist->Rebin(rebin);
          if(weighted) {hist->Scale(rebin*int_lumi*cross_sec/N_tot);}
          else{
            if(signal) {hist->Scale(rebin/hist->Integral());}
            else {
              hist->Scale(rebin/hist->Integral());
              hist->Scale((hist->GetEntries()*int_lumi*cross_sec/N_tot)/N_tot_background[full_hist_name]);
            }
          }
          hist->Sumw2(false);

          if(overflow) add_overflow_bin(hist, xMax);
          
          hist->SetLineColor(color);
          stacks_signal[full_hist_name]->Add(hist);
        
          if(find(in_legend.begin(), in_legend.end(), file_name) == in_legend.end()){
            if(signal){legend->AddEntry(hist, title.c_str(), "l");}
            else {legend->AddEntry(hist, title.c_str(), "f");}
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
    
        auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel, ylabel] = params;

        auto canvas = new TCanvas("canvas", "canvas");
        canvas->cd();

        if(hist_name == "dimuon_mass" || hist_name == "dimuon_mass_log")
        {
          // This is to update the x-axis region which couldn't be done for the mass.
          int n_bins = 100;
          float* binList = new float[n_bins+1];
          for (int i=0; i<n_bins+1; i++) {
            binList[i] = (pow(10,log10(xMin)+((log10(xMax)-log10(xMin))/n_bins)*i));
          }
          ghost_hist = new TH1F("hist","",n_bins, binList);
          THStack* ghost_stack = new THStack();
          ghost_stack->Add(ghost_hist);
          ghost_stack->Draw();
          set_hist_layout(ghost_stack, params);

          stacks_signal[full_hist_name]->Draw("nostack same");
        }
        else if(hist_name == "minlxy-muon_lxy_rebinned_extended_general_1widthbins")
        {
          // This is to update the x-axis region which couldn't be done for the mass.
          int n_bins = 4;
          float binList[] = {0, 1, 2, 3, 4};
          ghost_hist = new TH1F("hist","",n_bins, binList);
          THStack* ghost_stack = new THStack();
          ghost_stack->Add(ghost_hist);
          ghost_stack->Draw();
          set_hist_layout(ghost_stack, params);
          ghost_stack->GetXaxis()->ChangeLabel(2,-1,-1,-1,-1,-1,"110");
          ghost_stack->GetXaxis()->ChangeLabel(3,-1,-1,-1,-1,-1,"1300");
          ghost_stack->GetXaxis()->ChangeLabel(4,-1,-1,-1,-1,-1,"3000");
          ghost_stack->GetXaxis()->ChangeLabel(5,-1,-1,-1,-1,-1,"7300");
          ghost_stack->GetXaxis()->SetNdivisions(4);
          stacks_signal[full_hist_name]->Draw("same");

          vector<string> bin_labels = {"#bf{Inner tracker}", "#bf{Outer tracker}", "#bf{Calorimeter}", "#bf{Muon system}"};
          TLatex* l = new TLatex();
          vector<double> y = {0.6, 0.3, 0.11, 0.11};
          for (int i=0; i<n_bins; i++){
            double x = i*0.2+0.13;
            l->SetNDC(kTRUE);
            l->SetTextSize(0.036);
            l->DrawLatex(x, y[i], bin_labels[i].c_str());
          }
        }
        else{
          stacks_signal[full_hist_name]->Draw("nostack");
        }

        stacks_signal[full_hist_name]->GetXaxis()->SetLimits(xMin, xMax);
        if(yMax != 0){
          stacks_signal[full_hist_name]->SetMaximum(yMax);
          stacks_signal[full_hist_name]->SetMinimum(yMin);
        }

        set_hist_layout(stacks_signal[full_hist_name], params);

        gPad->Modified();
        gPad->RedrawAxis();
        if(logy) canvas->SetLogy();
        if(logx) canvas->SetLogx();

        legend->Draw();
        if(weighted) {text.Draw();}
        if(prefix.substr(0,15) == "final_selection") {selection_text.Draw();}

        canvas->Update();
        
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
