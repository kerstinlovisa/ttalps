#include <filesystem>

void plot_signal_2dhistograms()
{
  // Options for plotting:
  bool weighted = true;

  string username = getenv("USER");

  string base_path = "/nfs/dust/cms/user/" + username + "/ttalps/signals_ctau-default_non-muon-mothers/hists/";
  // string base_path = "/nfs/dust/cms/user/" + username + "/ttalps/reweighted/hists/";
  // string base_path = "/nfs/dust/cms/user/jalimena/ttalps/hists/backup_lovisa/";
  string output_path;
  if(username == "lrygaard") {output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/plots_signal_2d_no-selection/";}
  // else if(username == "jniedzie") {output_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/";}
  // Only set up for user lrygaard now
  else {cout << "Error: unrecognized user." << endl;}

  filesystem::path p(output_path);
  if(!filesystem::exists(p))
  {
    filesystem::create_directory(p);
    p = output_path + "alp";
    filesystem::create_directory(p);
  }

  int int_lumi = 150e3; // pb-1

  vector<int> lxy_bins = {0, 2, 10, 24, 31, 70, 110};
  
  map<string, tuple<int, string, bool, float, int> > file_names = {
    // file name    
    // {"06_muon_siblings/tta_mAlp-8GeV_ctau-0p000010mm.root",{kGreen+2,     "0.3 GeV non-pair", true,     0.1188,        950000}},
    // {"05_muon_siblings/tta_mAlp-0p315GeV.root",    {kSpring-5,  "0.315 GeV pair",   true,       0.1188,        1000000}},
    // {"07_muon_siblings/tta_mAlp-0p5GeV.root",      {kViolet,    "0.5 GeV pair",     true,       0.1188,        1000000}},
    // {"09_muon_siblings/tta_mAlp-2GeV.root",        {kRed,       "2 GeV pair",       true,       0.1169,        1000000}},
    // {"11_muon_siblings/tta_mAlp-8GeV.root",        {kBlue,      "8 GeV pair",       true,       0.1148,        990000}},
    // {"11_muon_siblings/tta_mAlp-10GeV.root",       {kBlue,      "10 GeV pair",      true,       0.1148,        980000}},

    // {"03_tta_mAlp-0p2GeV.root",                    {kSpring-5,  "m_{a} = 0.2 GeV",        true,       0.117,        970000}},
    {"03_tta_mAlp-0p3GeV.root",                    {kSpring-5,  "m_{a} = 0.3 GeV",        true,       0.1173,       990000}},
    // {"05_tta_mAlp-0p315GeV.root",                  {kSpring-5,  "m_{a} = 0.315 GeV",      true,       0.1169,       1000000}},
    // {"05_tta_mAlp-0p35GeV.root",                   {kYellow,  "m_{a} = 0.35 GeV",       true,       0.1169,       1000000}},
    {"06_tta_mAlp-0p5GeV.root",                    {kOrange,    "m_{a} = 0.5 GeV",        true,       0.1181,       1000000}},
    {"06_tta_mAlp-0p9GeV.root",                    {kRed+2,    "m_{a} = 0.9 GeV",        true,       0.1181,       1000000}},
    {"07_tta_mAlp-1p25GeV.root",                   {kRed,       "m_{a} = 1.25 GeV",       true,       0.1188,       1000000}},
    {"07_tta_mAlp-2GeV.root",                      {kMagenta+2,       "m_{a} = 2 GeV",          true,       0.1188,       1000000}},
    // {"07_tta_mAlp-4GeV.root",                      {kMagenta,       "m_{a} = 4 GeV",          true,       0.1188,       1000000}},
    {"08_tta_mAlp-8GeV.root",                      {kBlue,      "m_{a} = 8 GeV",          true,       0.1163,       990000}},
    {"11_tta_mAlp-10GeV.root",                     {kCyan,      "m_{a} = 10 GeV",         true,       0.1154,       980000}},

    // {"06_muon_non_siblings/tta_mAlp-8GeV_ctau-0p000010mm.root",{kGreen+2,     "0.3 GeV non-pair", true,     0.1188,        950000}},
    // {"06_muon_non_siblings/tta_mAlp-0p9GeV.root",{kGreen+2,     "0.3 GeV non-pair", true,     0.1188,        950000}},
    // {"06_muon_non_siblings/tta_mAlp-0p315GeV.root",{kGreen+2,     "0.3 GeV non-pair", true,     0.1188,        950000}},
    // {"08_muon_non_siblings/tta_mAlp-0p5GeV.root",  {kViolet+2,    "0.5 GeV non-pair", true,     0.1188,        860000}},
    // {"10_muon_non_siblings/tta_mAlp-2GeV.root",    {kRed+3,       "2 GeV non-pair",   true,     0.1169,        980000}},
    // {"12_muon_non_siblings/tta_mAlp-8GeV.root",    {kBlue+2,      "8 GeV non-pair",   true,     0.1148,        890000}},
    // {"12_muon_non_siblings/tta_mAlp-10GeV.root",   {kBlue+2,      "10 GeV non-pair",  true,     3.046,        990000}},
  };

  map<string, tuple<bool, bool, bool, int, double, double, double, double, string, string>> hist_names = {
    // Rebinned option implies histograms with cutomized binning
//                                logy   logx   rebinned  rebin   xMin    xMax    yMin    yMax    xlabel                       ylabel
    // {"first_mother-dimuon_mass_1p5",           {true, false,  false,   1,      0,      1.5,    10,   3e5,         "m_{#mu#bar{#mu}} [GeV]",         "m_{a} [GeV]"}},
    // {"first_mother-dimuon_mass_4p5",           {true, false,  false,   1,      3.75,    4.25,     10,   3e5,      "m_{#mu#bar{#mu}} [GeV]",         "m_{a} [GeV]"}},
    // {"first_mother-dimuon_mass_10p5",          {true, false,  false,   1,      7.75,    8.25,     10,   3e5,      "m_{#mu#bar{#mu}} [GeV]",         "m_{a} [GeV]"}},
    {"first_dimuon_pt_2d",                     {true, false,  false,   1,      0,    100,     0,   100,      "Last p_{T}^{#mu} [GeV]",         "First p_{T}^{#mu} [GeV]"}},
    {"first_mother_dimuon_pt_2d",              {true, false,  false,   1,      0,    100,     0,   100,      "Last p_{T}^{#mu} [GeV]",         "First p_{T}^{#mu} [GeV]"}},
  };
  vector<string> prefixes = {
    "",
    // "alp/alp_", // this is for no selections
    // "alp/alp_final_selection_", // this is for no selections
  };

  vector<string> categories = {
    "os_",
    // "ss_",
    // "single_",
  };

  gStyle->SetStatStyle(0);
  gStyle->SetTitleStyle(0);
  gROOT->ForceStyle();

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

          auto canvas = new TCanvas("canvas", "canvas", 600, 600);
          canvas->cd();
          canvas->SetRightMargin(0.2); 
          canvas->SetLeftMargin(0.2); 
          canvas->SetTopMargin(0.2); 
          canvas->SetBottomMargin(0.2); 

          hist->Draw("COLZ same");

          hist->GetXaxis()->SetTitle(xlabel.c_str());
          hist->GetYaxis()->SetTitle(ylabel.c_str());
          // hist->GetXaxis()->SetTitle("m_{#mu#bar{#mu}} [GeV]");
          // hist->GetYaxis()->SetTitle("m_{a} [GeV]");

          std::cout << xMin << "\t" << xMax << std::endl;
          // hist->GetXaxis()->SetLimits(xMin, xMax);
          hist->GetXaxis()->SetRangeUser(xMin, xMax);
          hist->GetYaxis()->SetRangeUser(xMin, xMax);
          
          // hist->SetMinimum(xMin);
          // hist->SetMaximum(xMax);

          gPad->Modified();
          // gPad->RedrawAxis();
          canvas->SetLogz();
          // hist->Sumw2(false);

          gStyle->SetOptTitle(kFALSE);
          gStyle->SetOptStat(0);
          gPad->Modified();
          gPad->RedrawAxis();
          gPad->Update();
          canvas->Update();
          
          string signal_name = file_name;
          signal_name.erase(signal_name.size()-5, signal_name.size());
          string output_file_name = output_path + full_hist_name + "_" + signal_name + ".pdf";
          canvas->SaveAs(output_file_name.c_str());

          delete canvas;

          // hist->SetLineColor(color);
          // hist->SetLineWidth(2);
          // hist->Rebin(rebin);
          // if(weighted) {hist->Scale(rebin*int_lumi*cross_sec/N_tot);}
          // else{
          //   if(signal) {hist->Scale(rebin/hist->Integral());}
          //   else {
          //     hist->Scale(rebin/hist->Integral());
          //     hist->Scale((hist->GetEntries()*int_lumi*cross_sec/N_tot)/N_tot_background[full_hist_name]);
          //   }
          // }
          // hist->Sumw2(false);
          
          // if(signal) {
          //   hist->SetLineColor(color);
          //   stacks_signal[full_hist_name]->Add(hist);}
        
          // if(find(in_legend.begin(), in_legend.end(), file_name) == in_legend.end()){
          //   if(signal){legend->AddEntry(hist, title.c_str(), "l");}
          //   else {legend->AddEntry(hist, title.c_str(), "f");}
          //   in_legend.push_back(file_name);
          // }
          input_file->cd();
        }
      }
    }
  }
}