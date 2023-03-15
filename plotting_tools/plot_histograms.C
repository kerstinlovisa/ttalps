#include <filesystem>

void plot_histograms()
{
  // Options for plotting:
  bool weighted = true;

  // string base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/";
  string base_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/hists/";
  // string base_path = "/nfs/dust/cms/user/lrygaard/ttalps/hists/";
  string output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/plots/";

  filesystem::path p(output_path);
  if(!filesystem::exists(p))
  {
    filesystem::create_directory(p);
    p = output_path + "final_selection";
    filesystem::create_directory(p);
    p = output_path + "intermediate_selections";
    filesystem::create_directory(p);
  }

  int int_lumi = 101e3; // pb-1

  vector<int> lxy_bins = {0, 2, 10, 24, 31, 70, 110};
  
  map<string, tuple<int, string, bool, float, int> > file_names = {
    // file name                                // color        // legend           // signal   // cross-sec  // Ntot
    {"01_muon_siblings/ttj.root",                  {kAzure+6,   "ttj pair",         false,      395.3,        12540000}},
    {"03_muon_siblings/ttmumu.root",               {kOrange-4,  "tt#mu#mu pair",    false,      0.02091,      9940000}},
    {"05_muon_siblings/tta_mAlp-0p315GeV.root",    {kSpring-5,  "0.3 GeV pair",     true,       3.075,        1950000}},
    {"07_muon_siblings/tta_mAlp-0p5GeV.root",      {kViolet,    "0.5 GeV pair",     true,       3.098,        1659356}},
    {"09_muon_siblings/tta_mAlp-1GeV.root",        {kRed,       "1 GeV pair",       true,       3.104,        1158318}},
    // {"11_muon_siblings/tta_mAlp-10GeV.root",       {kCyan+2,  "10 GeV pair",         true,       3.046,    1127443}},

    // {"single_muon/ttj.root",                    {kViolet,   "ttj single",         false}},
    // {"single_muon/ttmumu.root",                 {kBlue,     "tt#mu#mu single",    false}},
    // {"single_muon/tta_mAlp-0p315GeV.root",      {kBlue+1,   "0.3 GeV single",     true}},
    // {"single_muon/tta_mAlp-0p5GeV.root",        {kBlue+1,   "0.5 GeV single",     true}},
    // {"single_muon/tta_mAlp-1GeV.root",          {kBlue+1,   "1 GeV single",       true}},
    // {"single_muon/tta_mAlp-10GeV.root",         {kBlue+1,   "10 GeV single",      true}},

    {"02_muon_non_siblings/ttj.root",              {kBlue-6,      "ttj non-pair",     false,    395.3,        12540000}},
    {"04_muon_non_siblings/ttmumu.root",           {kOrange+1,    "tt#mu#mu non-pair",false,    0.02091,      9940000}},
    // {"06_muon_non_siblings/tta_mAlp-0p315GeV.root",  {kGreen+3,   "0.3 GeV non-pair",    true,    3.075,     1950000}},
    // {"08_muon_non_siblings/tta_mAlp-0p5GeV.root",  {kBlue+3,    "0.5 GeV non-pair",    true,    3.098,     1659356}},
    // {"10_muon_non_siblings/tta_mAlp-1GeV.root",    {kRed+4,  "1 GeV non-pair",         true,    3.104,     1158318}},
    // {"12_muon_non_siblings/tta_mAlp-10GeV.root",   {kBlack,    "10 GeV non-pair",      true,    3.046,     1127443}},
  };
  
  map<string, tuple<bool, bool, bool, int, double, double, double, double, string>> hist_names = {
    // Add desciption of rebin & rebinned...
//                                logy   logx   rebinned  rebin   xMin    xMax    yMin    yMax    xlabel
    {"muon_pt",                   {true, false,  false,   1,      0,      50,     10,   1e5,      "p_{T}^{#mu} [GeV]"}},
    // {"muon_pz",                   {true, false,  false,   10,     0,      100,    0,      0,      "p_{z}^{#mu} [GeV]"}},
    // {"muon_mass",                 {true, false,   false,  1,      0.1,    1,      10,     5e6,    "m_{#mu} [GeV]"}},
    {"muon_mass_log",             {true, true,   false,   1,      0.1,    1,      10,     5e6,    "m_{#mu} [GeV]"}},
    {"muon_lxy",                  {true, false,  false,   10,     0,      110,    100,    4e6,    "l_{xy}^{#mu} [mm]"}},
    // {"muon_lxy_logx",             {true, true,   false,   1,      0,      200,    0,      0,      "l_{xy}^{#mu} [mm]"}},
    {"muon_lxy_rebinned",         {true, false,  true,    1,      0,      110,    0.1,    2e5,    "l_{xy}^{#mu} [mm]"}},
    // {"muon_lz",                   {true, false,  false,   1,      0,      50,     0,      0,      "l_{z}^{#mu} [mm]"}},
    {"muon_lxyz",                 {true, false,  false,   1,      0,      100,    0,      0,      "l_{xyz}^{#mu} [mm]"}},
    {"muon_ctau",                 {true, false,  false,   1,      0,      100,    0,      0,      "Muon c#tau [mm]"}},
    {"muon_boost",                {true, false,  false,   20,     0,      120,    0,      0,      "Muon #gamma#beta"}},
    {"dimuon_pt",                 {true, false,  false,   10,     0,      100,    0,      0,      "Dimuon p_{T}[GeV]"}},
    // {"dimuon_pz",                 {true, false,  false,   10,     0,      100,    0,      0,      "Dimuon p_{z}[GeV]"}},
    // {"dimuon_mass",               {true, false,  false,   1,      0.1,    10,      1,      2e5,      "m_{#mu#bar{#mu}} [GeV]"}},
    {"dimuon_mass_log",           {true, true,   false,   1,      0.1,    200,    1,      2e5,      "m_{#mu#bar{#mu}} [GeV]"}},
    {"dimuon_deltaR",             {true, false,  false,   1,      0,      1,      1,      2e5,    "#Delta R(#mu#bar{#mu})"}},
    // {"dimuon_deltaPhi",           {true, false,  false,   1,     -4,      4,      0,      0,      "#Delta #phi(#mu#bar{#mu})"}},
    {"dimuon_deltalxy",           {true, false,  false,   1,      0,      10,     1,      2e5,    "#Delta l_{xy}(#mu#bar{#mu}) [mm]"}},
    {"dimuon_deltalxyz",          {true, false,  false,   1,      0,      10,     1,      2e5,    "#Delta l_{xyz}(#mu#bar{#mu}) [mm]"}},
    {"dimuon_deltapt",            {true, false,  false,   1,      0,      100,     1,      1e5,      "#Delta p_{T}(#mu#bar{#mu}) [mm]"}},
    // {"first_mother_pt",           {true, false,  false,   1,      0,      100,    0,      0,      "Muon first mother p_{T} [GeV]"}},
    // {"first_mother_pz",           {true, false,  false,   10,     0,      100,    0,      0,      "Muon first mother p_{z} [GeV]"}},
    // {"first_mother_mass",         {true, true,   false,   1,      0.1,    10,    10,    5e6,      "Muon first mother m [GeV]"}},
    // {"first_mother_lxy",          {true, false,  false,   1,      0,      100,    0,      0,      "Muon first mother l_{xy} [mm]"}},
    // {"first_mother_lxy_rebinned", {true, false,  true,    1,      0,      110,    0,      0,      "Muon first mother l_{xy} [mm]"}},
    // {"first_mother_lz",           {true, false,  false,   1,      0,      100,    0,      0,      "Muon first mother l_{z} [mm]"}},
    // {"first_mother_lxyz",         {true, false,  false,   1,      0,      100,    0,      0,      "Muon first mother l_{xyz} [mm]"}},
    // {"first_mother_ctau",         {true, false,  false,   1,      0,      100,    0,      0,      "Muon first mother c#tau [mm]"}},
    // {"first_mother_boost",        {true, false,  false,   20,     0,      120,    0,      0,      "Muon first mother #gamma#beta"}},
  };

  vector<string> prefixes = {
    "", // this is for no selections

    "intermediate_selections/sel_pt-min10GeV_",
    "intermediate_selections/sel_pt-min8GeV_",
    "intermediate_selections/sel_pt-min5GeV_",

    "intermediate_selections/sel_mass-Jpsi_",
    "intermediate_selections/sel_mass-rho_omega_",
    "intermediate_selections/sel_mass-max20GeV_",

    "intermediate_selections/sel_dlxy-max0p1mm_",
    "intermediate_selections/sel_dlxyz-max0p1mm_",
    "intermediate_selections/sel_dlxy_ratio-max0p1_",
    // "intermediate_selections/sel_dlxyz_ratio-max0p1_",
    // "intermediate_selections/sel_dlxy_ratio_v2-max0p1_",
    // "intermediate_selections/sel_dlxyz_ratio_v2-max0p1_",

    "final_selection/final_selection_pt-min10GeV_mass-cuts_",
    "final_selection/final_selection_pt-min10GeV_mass-cuts_dR-max0p1_",
    "final_selection/final_selection_pt-min10GeV_mass-cuts_dR-max0p2_",
    "final_selection/final_selection_pt-min10GeV_mass-cuts_dR-max0p05_",
    "final_selection/final_selection_pt-min10GeV_mass-cuts_dlxy-max0p1mm_",
    "final_selection/final_selection_pt-min10GeV_mass-cuts_dlxyz-max0p1mm_",
    "final_selection/final_selection_pt-min10GeV_mass-cuts_dlxy_ratio-max0p1_",
    "final_selection/final_selection_pt-min10GeV_mass-cuts_dlxyz_ratio-max0p1_",
    "final_selection/final_selection_pt-min10GeV_mass-cuts_dlxy_ratio_v2-max0p1_",
    "final_selection/final_selection_pt-min10GeV_mass-cuts_dlxyz_ratio_v2-max0p1_",

    // "final_selection/final_selection_pt-min10GeV_dR-max0p1_",
    // "final_selection/final_selection_pt-min10GeV_dR-max0p2_",
    // "final_selection/final_selection_pt-min10GeV_dR-max0p05_",
    // "final_selection/final_selection_pt-min10GeV_dlxy-max0p1mm_",
    // "final_selection/final_selection_pt-min10GeV_dlxyz-max0p1mm_",
    // "final_selection/final_selection_pt-min10GeV_dlxy_ratio-max0p1_",
    // "final_selection/final_selection_pt-min10GeV_dlxyz_ratio-max0p1_",
    // "final_selection/final_selection_pt-min10GeV_dlxy_ratio_v2-max0p1_",
    // "final_selection/final_selection_pt-min10GeV_dlxyz_ratio_v2-max0p1_",
    // "final_selection/final_selection_pt-min10GeV_dlxy_ratio_v2-max0p1_",
    // "final_selection/final_selection_pt-min10GeV_dlxyz_ratio_v2-max0p1_",

    // "final_selection/final_selection_pt-min8GeV_mass-cuts_",
    // "final_selection/final_selection_pt-min8GeV_mass-cuts_dR-max0p1_",
    // "final_selection/final_selection_pt-min8GeV_mass-cuts_dR-max0p2_",
    // "final_selection/final_selection_pt-min8GeV_mass-cuts_dR-max0p05_",
    // "final_selection/final_selection_pt-min8GeV_mass-cuts_dlxy-max0p1mm_",
    // "final_selection/final_selection_pt-min8GeV_mass-cuts_dlxyz-max0p1mm_",
    // "final_selection/final_selection_pt-min8GeV_mass-cuts_dlxy_ratio-max0p1_",
    // "final_selection/final_selection_pt-min8GeV_mass-cuts_dlxyz_ratio-max0p1_",
    // "final_selection/final_selection_pt-min8GeV_mass-cuts_dlxy_ratio_v2-max0p1_",
    // "final_selection/final_selection_pt-min8GeV_mass-cuts_dlxyz_ratio_v2-max0p1_",

    // "final_selection/final_selection_pt-min8GeV_dR-max0p1_",
    // "final_selection/final_selection_pt-min8GeV_dR-max0p2_",
    // "final_selection/final_selection_pt-min8GeV_dR-max0p05_",
    // "final_selection/final_selection_pt-min8GeV_dlxy-max0p1mm_",
    // "final_selection/final_selection_pt-min8GeV_dlxyz-max0p1mm_",
    // "final_selection/final_selection_pt-min8GeV_dlxy_ratio-max0p1_",
    // "final_selection/final_selection_pt-min8GeV_dlxyz_ratio-max0p1_",
    // "final_selection/final_selection_pt-min8GeV_dlxy_ratio_v2-max0p1_",
    // "final_selection/final_selection_pt-min8GeV_dlxyz_ratio_v2-max0p1_",

    // "final_selection/final_selection_pt-min5GeV_mass-cuts_",
    // "final_selection/final_selection_pt-min5GeV_mass-cuts_dR-max0p1_",
    // "final_selection/final_selection_pt-min5GeV_mass-cuts_dR-max0p2_",
    // "final_selection/final_selection_pt-min5GeV_mass-cuts_dR-max0p05_",
    // "final_selection/final_selection_pt-min5GeV_mass-cuts_dlxy-max0p1mm_",
    // "final_selection/final_selection_pt-min5GeV_mass-cuts_dlxyz-max0p1mm_",
    // "final_selection/final_selection_pt-min5GeV_mass-cuts_dlxy_ratio-max0p1_",
    // "final_selection/final_selection_pt-min5GeV_mass-cuts_dlxyz_ratio-max0p1_",
    // "final_selection/final_selection_pt-min5GeV_mass-cuts_dlxy_ratio_v2-max0p1_",
    // "final_selection/final_selection_pt-min5GeV_mass-cuts_dlxyz_ratio_v2-max0p1_",

    // "final_selection/final_selection_pt-min5GeV_dR-max0p1_",
    // "final_selection/final_selection_pt-min5GeV_dR-max0p2_",
    // "final_selection/final_selection_pt-min5GeV_dR-max0p05_",
    // "final_selection/final_selection_pt-min5GeV_dlxy-max0p1mm_",
    // "final_selection/final_selection_pt-min5GeV_dlxyz-max0p1mm_",
    // "final_selection/final_selection_pt-min5GeV_dlxy_ratio-max0p1_",
    // "final_selection/final_selection_pt-min5GeV_dlxyz_ratio-max0p1_",
    // "final_selection/final_selection_pt-min5GeV_dlxy_ratio_v2-max0p1_",
    // "final_selection/final_selection_pt-min5GeV_dlxyz_ratio_v2-max0p1_",

    // "final_selection/final_selection_mass-cuts_",
    // "final_selection/final_selection_mass-cuts_dR-max0p1_",
    // "final_selection/final_selection_mass-cuts_dR-max0p2_",
    // "final_selection/final_selection_mass-cuts_dR-max0p05_",
    // "final_selection/final_selection_mass-cuts_dlxy-max0p1mm_",
    // "final_selection/final_selection_mass-cuts_dlxyz-max0p1mm_",
    // "final_selection/final_selection_mass-cuts_dlxy_ratio-max0p1_",
    // "final_selection/final_selection_mass-cuts_dlxyz_ratio-max0p1_",
    // "final_selection/final_selection_mass-cuts_dlxy_ratio_v2-max0p1_",
    // "final_selection/final_selection_mass-cuts_dlxyz_ratio_v2-max0p1_",
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
  
  auto legend = new TLegend(0.6, 0.7, 0.9, 0.9);
  legend->SetNColumns(2);
  vector<string> in_legend;
  
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
          auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel] = params;
          
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
    
        auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel] = params;

        auto c = new TCanvas("c", "c");
        c->cd();

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
          ghost_hist->GetYaxis()->SetTitle("number of events [a.u.]");
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
        stacks_background[full_hist_name]->GetYaxis()->SetTitle("number of events [a.u.]");
        stacks_background[full_hist_name]->GetXaxis()->SetRangeUser(xMin, xMax);
        gPad->Modified();
        if(logy) c->SetLogy();
        if(logx) c->SetLogx();

        legend->Draw();

        c->Update();
        
        string file_name = output_path + full_hist_name + ".pdf";
        c->SaveAs(file_name.c_str());

        delete c;
        if(hist_name == "dimuon_mass" || hist_name == "dimuon_mass_log")
        {
          delete ghost_hist;
        }
      }
    }
  }

}
