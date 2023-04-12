#include <filesystem>

void plot_histograms()
{
  // Options for plotting:
  bool weighted = true;

  // string base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/";
  // string base_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/hists/";
  // string base_path = "/nfs/dust/cms/user/lrygaard/ttalps/alps/hists/";
  string base_path = "/nfs/dust/cms/user/lrygaard/ttalps/hists/";
  string output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/plots/";

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

  vector<int> lxy_bins = {0, 2, 10, 24, 31, 70, 110};
  
  map<string, tuple<int, string, bool, float, int> > file_names = {
    // file name                                // color        // legend           // signal   // cross-sec  // Ntot
    {"01_muon_siblings/ttj.root",                  {kAzure+6,   "ttj resonances",         false,      395.3,        12540000}},
    {"03_muon_siblings/ttmumu.root",               {kOrange-4,  "tt#mu#mu resonances",    false,      0.02091,      9940000}},
    // {"05_muon_siblings/tta_mAlp-0p315GeV.root",    {kSpring-5,  "0.315 GeV pair",   true,       3.122,        950000}},
    // {"07_muon_siblings/tta_mAlp-0p5GeV.root",      {kViolet,    "0.5 GeV pair",     true,       3.098,        860000}},
    // {"09_muon_siblings/tta_mAlp-2GeV.root",        {kRed,       "2 GeV pair",       true,       3.087,        980000}},
    // {"11_muon_siblings/tta_mAlp-8GeV.root",        {kBlue,      "8 GeV pair",       true,       3.023,        890000}},
    // {"11_muon_siblings/tta_mAlp-10GeV.root",       {kBlue,      "10 GeV pair",      true,       3.046,        990000}},

    {"05_tta_mAlp-0p315GeV.root",                  {kSpring-5,  "m_{a} = 0.315 GeV",      true,       3.122,        950000}},
    {"07_tta_mAlp-0p5GeV.root",                    {kViolet,    "m_{a} = 0.5 GeV",        true,       3.098,        860000}},
    {"09_tta_mAlp-2GeV.root",                      {kRed,       "m_{a} = 2 GeV",          true,       3.087,        980000}},
    {"11_tta_mAlp-8GeV.root",                      {kBlue,      "m_{a} = 8 GeV",          true,       3.023,        890000}},
    // {"11_tta_mAlp-10GeV.root",                     {kBlue,      "m_{a} = 10 GeV",         true,       3.046,        990000}},

    {"02_muon_non_siblings/ttj.root",              {kBlue-6,    "ttj non-resonances",     false,      395.3,        12540000}},
    {"04_muon_non_siblings/ttmumu.root",           {kOrange+1,  "tt#mu#mu non-resonances",false,      0.02091,      9940000}},
    // {"06_muon_non_siblings/tta_mAlp-0p315GeV.root",{kGreen+2,     "0.3 GeV non-pair", true,     3.075,        950000}},
    // {"08_muon_non_siblings/tta_mAlp-0p5GeV.root",  {kViolet+2,    "0.5 GeV non-pair", true,     3.098,        860000}},
    // {"10_muon_non_siblings/tta_mAlp-2GeV.root",    {kRed+3,       "2 GeV non-pair",   true,     3.087,        980000}},
    // {"12_muon_non_siblings/tta_mAlp-8GeV.root",    {kBlue+2,      "8 GeV non-pair",   true,     3.023,        890000}},
    // {"12_muon_non_siblings/tta_mAlp-10GeV.root",   {kBlue+2,      "10 GeV non-pair",  true,     3.046,        990000}},
  };
  
  map<string, tuple<bool, bool, bool, int, double, double, double, double, string, string>> hist_names = {
    // Rebinned option implies histograms with cutomized binning
//                                logy   logx   rebinned  rebin   xMin    xMax    yMin    yMax    xlabel                       ylabel
    {"muons_pt",                  {true, false,  false,   1,      0,      50,     10,   3e5,      "p_{T}^{#mu} [GeV]",         "Muons / 0.5 GeV"}},
    // {"first_mother_pt",           {true, false,  false,   1,      0,      50,     10,   3e5,      "p_{T}^{a} [GeV]",         "Events / 0.5 GeV"}},
    // {"first_mother_eta",          {false, false,  false,   1,      -3,      3,     0,   2000,      "#eta",         "Events "}},
    {"maxlxy-muon_pt",            {true, false,  false,   1,      0,      50,     10,   2e4,      "p_{T}^{#mu} [GeV]",         "Events / 0.5 GeV"}},
    {"minlxy-muon_pt",            {true, false,  false,   1,      0,      50,     10,   2e4,      "p_{T}^{#mu} [GeV]",         "Events / 0.5 GeV"}},
    // {"maxlxy-muon_pz",            {true, false,  false,   10,     0,      100,    0,      0,      "p_{z}^{#mu} [GeV]",      "Events / GeV"}},
    // {"minlxy-muon_pz",            {true, false,  false,   10,     0,      100,    0,      0,      "p_{z}^{#mu} [GeV]",      "Events / GeV"}},
    {"maxlxy-muon_lxy",           {true, false,  false,   20,     0,      150,      5,    4e6,    "l_{xy}^{#mu} [mm]",         "Events / 2.0 mm"}},
    {"minlxy-muon_lxy",           {true, false,  false,   20,     0,      150,     10,    6e6,    "l_{xy}^{#mu} [mm]",         "Events / 2.0 mm"}},
    {"maxlxy-muon_lxy_rebinned",  {true, false,  true,    1,      0,      110,    0.1,    2e5,    "l_{xy}^{#mu} [mm]",         "Events / mm"}},
    {"minlxy-muon_lxy_rebinned",  {true, false,  true,    1,      0,      110,    0.1,    2e5,    "l_{xy}^{#mu} [mm]",         "Events / mm"}},
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
    {"dimuon_pt",                 {true, false,  false,   10,     0,      100,    0,      0,      "Dimuon p_{T}[GeV]",         "Events / GeV"}},
    // {"dimuon_pz",                 {true, false,  false,   10,     0,      100,    0,      0,      "Dimuon p_{z}[GeV]",      "Events / GeV"}},
    {"dimuon_mass",               {true, false,  false,   1,      0.1,    1,      1,      1e6,    "m_{#mu#bar{#mu}} [GeV]",      "Events / GeV"}},
    {"dimuon_mass_log",           {true, true,   false,   1,      0.25,   10,     1,      1e9,    "m_{#mu#bar{#mu}} [GeV]",          "Events / GeV"}},
    // {"first_mother_mass",         {true, false,  false,   1,      0.1,    1,      1,      1e6,     "m_{a} [GeV]",      "Events / GeV"}},
    // {"first_mother_mass_log",     {true, true,   false,   1,      0.25,   10,     1,      1e9,     "m_{a} [GeV]",          "Events / GeV"}},
    {"dimuon_deltaR",             {true, false,  false,   1,      0,      1,      1,      2e5,    "#Delta R(#mu#bar{#mu})",            "Events"}},
    // {"dimuon_deltaPhi",           {true, false,  false,   1,     -4,      4,      0,      0,      "#Delta #phi(#mu#bar{#mu})",              "Events"}},
    {"dimuon_deltalxy",           {true, false,  false,   1,      0,      0.001,  1,      1e6,    "#Delta l_{xy}(#mu#bar{#mu}) [mm]",          "Events / mm"}},
    {"dimuon_deltalxy_diff_abs",  {true, false,  false,   1,      0,      10,     1,      1e6,    "|l_{xy}^{#mu} - l_{xy}^{#bar{#mu}}| [mm]",  "Events / mm"}},
    {"dimuon_deltalxy_ratio_abs", {true, false,  false,   10,     0,      1.05,     1,    1e9,    "R_{lxy}",         "Events / 0.05"}},
    // {"dimuon_deltapt",            {true, false,  false,   1,      0,      100,    1,      1e5,     "#Delta p_{T}(#mu#bar{#mu}) [mm]",          "Events / GeV"}},
  };

  vector<string> prefixes = {
    "", // this is for no selections

    // "intermediate_selections/sel_pt-min10p0GeV_",
    // "intermediate_selections/sel_mass-cuts_",

    // "intermediate_selections/sel_deltalxy-max0p3mm_",
    // "intermediate_selections/sel_deltalxy_ratio_abs-max0p05_",

    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_",

    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy-max0p3mm_",
    "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_",
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
  };
  
  map<string, THStack*> stacks_signal;
  map<string, THStack*> stacks_background;
  for(auto &[hist_name, tmp] : hist_names){
    for(auto prefix : prefixes){
      for (auto category : categories) {
        string full_hist_name =  prefix + category + hist_name;
        stacks_signal[full_hist_name] = new THStack();
        stacks_background[full_hist_name] = new THStack();
      }
    }
  }
  
  auto legend = new TLegend(0.5, 0.6, 0.89, 0.85);
  legend->SetNColumns(2);
  legend->SetBorderSize(0);
  vector<string> in_legend;
  TLatex text(0.51, 0.86, "L = 150 fb^{-1}, #sqrt{s} = 13 TeV");
  text.SetNDC(kTRUE);
  text.SetTextSize(0.03);
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
          
          hist->SetLineColor(color);
          hist->SetLineWidth(2);
          hist->Rebin(rebin);
          if(weighted) {hist->Scale(rebin*int_lumi*cross_sec/N_tot);}
          else{hist->Scale(rebin/hist->GetEntries());}
          hist->Sumw2(false);

          if(rebinned)
          {
            for(int i=0; i<hist->GetNbinsX(); i++){
              hist->SetBinContent(i+1, hist->GetBinContent(i+1)/(lxy_bins[i+1]-lxy_bins[i]));
            }
          }
          
          if(signal) {stacks_signal[full_hist_name]->Add(hist);}
          else {
            hist->SetFillColor(color);
            stacks_background[full_hist_name]->Add(hist);
          }
        
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
          ghost_hist->Draw();
          ghost_hist->GetXaxis()->SetTitle(xlabel.c_str());
          ghost_hist->GetXaxis()->SetTitleSize(0.04);
          ghost_hist->GetYaxis()->SetTitleSize(0.04);
          ghost_hist->GetYaxis()->SetTitle(ylabel.c_str());
          ghost_hist->SetStats(0);
          ghost_hist->SetMaximum(yMax);
          ghost_hist->SetMinimum(yMin);
          stacks_background[full_hist_name]->Draw("same");
        }
        else{
          stacks_background[full_hist_name]->Draw();
        }
        stacks_signal[full_hist_name]->Draw("nostack same");

        stacks_background[full_hist_name]->GetXaxis()->SetLimits(xMin, xMax);
        if(yMax != 0){
          stacks_signal[full_hist_name]->SetMaximum(yMax);
          stacks_background[full_hist_name]->SetMaximum(yMax);
          stacks_signal[full_hist_name]->SetMinimum(yMin);
          stacks_background[full_hist_name]->SetMinimum(yMin);
        }
        stacks_background[full_hist_name]->GetXaxis()->SetTitle(xlabel.c_str());
        stacks_background[full_hist_name]->GetXaxis()->SetTitleSize(0.04);
        stacks_background[full_hist_name]->GetYaxis()->SetTitleSize(0.04);
        stacks_background[full_hist_name]->GetYaxis()->SetTitle(ylabel.c_str());
        stacks_background[full_hist_name]->GetXaxis()->SetRangeUser(xMin, xMax);

        gPad->Modified();
        gPad->RedrawAxis();
        if(logy) canvas->SetLogy();
        if(logx) canvas->SetLogx();

        legend->Draw();
        text.Draw();

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
