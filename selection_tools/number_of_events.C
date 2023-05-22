
double B(vector<double> n_vec){
  double n_tot = 0;
  for (double n : n_vec){
    n_tot += n;
  }
  return n_tot;
}

double B_sigma(vector<double> sigma_vec){
  double sigma2 = 0;
  for (double s : sigma_vec){
    sigma2 += s*s;
  }
  return sqrt(sigma2);
}

vector<double> figure_of_merit(vector<double> sig_events, double bkg_n, double bkg_sigma){
  vector<double> fom;
  for(double sig : sig_events){
    fom.push_back(sig/sqrt(sig+bkg_n+bkg_sigma));
  }
  return fom;
}

void print_latex(string output_file, vector<string> hist_names, vector<vector<double> > s, vector<vector<double> > s_sigma, vector<vector<double> > b, vector<vector<double> > b_sigma)
{
  // Create and open a text file
  ofstream output(output_file);
  vector<double> s0 = s[0];
  vector<double> b0 = b[0];

  output << "\\begin{table}[H] \n    \\centering \n    \\resizebox{\\textwidth}{!}{ \n    \\begin{tabular}{|l|";
  for(int i=0; i<(s0.size()+b0.size()); i++){ output << "c|";}
  output << "} \\hline" << endl;
  output << "        cuts:";
  for(int i=0; i<(s0.size()+b0.size()); i++){
    output << " & " << " ";
  }
  output << " \\\\" << endl;
  output << "        \\hline" << endl;
  for(int i=0; i<hist_names.size(); i++){
    vector<double> ss = s[i];
    vector<double> ssigma = s_sigma[i];
    vector<double> bb = b[i];
    vector<double> bsigma = b_sigma[i];
    output << "        " << hist_names[i];
    for(int j=0; j<ss.size(); j++){
      output << " & " << ss[j] << " $\\pm$ " << ssigma[j];
    }
    for(int j=0; j<bb.size(); j++){
      output << " & " << bb[j] << " $\\pm$ " << bsigma[j];
    }
    output << " \\\\" << endl;
  }
  output << "        \\hline \n    \\end{tabular}} \n    \\caption{Caption} \n    \\label{tab:my_label} \n\\end{table}" << endl;

  output.close();
}


void number_of_events()
{
  int int_lumi = 150e3;

  // string base_path = "/nfs/dust/cms/user/lrygaard/ttalps/hists/";
  // string base_path_sig = "/nfs/dust/cms/user/lrygaard/ttalps/signals_default_ptAlp-ge5GeV/hists/";
  string base_path_sig = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-default_new-dimuon-mass-cuts/hists/";
  // string base_path_sig = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-default_non-prompt-selection/hists/";
  // string base_path_sig = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-default_non-muon-mothers/hists/";
  // string base_path_sig = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-default_muon-status/hists/";
  // string base_path_sig = "/nfs/dust/cms/user/lrygaard/ttalps/signals_ctau-default/hists/";
  string base_path_bkg = "/nfs/dust/cms/user/lrygaard/ttalps/backgrounds_new-dimuon-mass-cuts/hists/";
  // string base_path_bkg = "/nfs/dust/cms/user/lrygaard/ttalps/backgrounds_non-prompt-selection/hists/";
  // string base_path_bkg = "/nfs/dust/cms/user/lrygaard/ttalps/backgrounds_non-muon-mothers/hists/";
  // string base_path_bkg = "/nfs/dust/cms/user/lrygaard/ttalps/backgrounds_JA-dir_updated/hists/";
  string output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/selections/";

  map<string, tuple<int, string, bool, float, int, float> > background_files = {
    // file name                                // color        // legend           // signal   // cross-sec  // Ntot
    {"01_ttj.root",                     {kAzure+6,   "ttj",         false,      395.3,        12540000,   1}},
    {"02_ttmumu.root",                  {kAzure+6,   "ttmumu",      false,      0.02091,        9940000,    1}},
  };

  map<string, tuple<int, string, bool, float, int, float> > signal_files = {
    // file name                                // color        // legend            // signal   // cross-sec  // Ntot      // BR(a->mumu)
    {"05_tta_mAlp-0p3GeV.root",                    {kCyan,      "m_{a} = 0.3 GeV",    true,       0.1485,       990000,    0.9999516480656298 }},
    {"06_tta_mAlp-0p35GeV.root",                   {kSpring-5,  "m_{a} = 0.35 GeV",    true,       0.1480,       1000000,   0.999954381388671 }},
    // {"07_tta_mAlp-0p5GeV.root",                    {kSpring-5,  "m_{a} = 0.5 GeV",    true,       0.1483,       1000000,   0.9998929187578673 }},
    {"08_tta_mAlp-0p9GeV.root",                    {kOrange,    "m_{a} = 0.9 GeV",     true,       0.1486,       1000000,   0.9994465135087311 }},
    // {"09_tta_mAlp-1p25GeV.root",                   {kOrange,    "m_{a} = 1.25 GeV"    true,       0.1482,       990000,    0.24705198671664572 }},
    {"10_tta_mAlp-2GeV.root",                      {kMagenta,   "m_{a} = 2 GeV",       true,       0.1483,       1000000,   0.17681064813740055 }},
    // {"11_tta_mAlp-4GeV.root",                      {kMagenta,   "m_{a} = 4 GeV",      true,       0.1479,       1000000,    0.0018272180991503392 }},
    {"12_tta_mAlp-8GeV.root",                      {kBlue,      "m_{a} = 8 GeV",       true,       0.1459,       990000,    0.0010447039648636659 }},
    // {"13_tta_mAlp-10GeV.root",                     {kBlue,      "m_{a} = 10 GeV",     true,       0.1449,       980000,    1.35213783949236e-05 }},
  };

  vector<string> hist_names = {
    // "os_minlxy-muon_lxy_rebinned_extended",
    // "intermediate_selections/sel_pt-min10p0GeV_os_minlxy-muon_lxy_rebinned_extended",
    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_os_minlxy-muon_lxy_rebinned_extended",
    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_os_minlxy-muon_lxy_rebinned_extended",

    "os_first_minlxy-muon_lxy_rebinned_extended",
    "intermediate_selections/sel_pt-min10p0GeV_os_first_minlxy-muon_lxy_rebinned_extended",
    "final_selection/final_selection_pt-min10p0GeV_mass-cuts_os_first_minlxy-muon_lxy_rebinned_extended",
    "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_os_first_minlxy-muon_lxy_rebinned_extended",

    // "os_minlxy-muon_lxy_rebinned",
    // "intermediate_selections/sel_pt-min10p0GeV_os_minlxy-muon_lxy_rebinned",
    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_os_minlxy-muon_lxy_rebinned",
    // "final_selection/final_selection_pt-min10p0GeV_mass-cuts_deltalxy_ratio_abs-max0p05_os_minlxy-muon_lxy_rebinned",
  };

  vector<string> cut_str = {
    "pre-selection",
    "muon pt<10GeV",
    "dimuon mass",
    "Rlxy<0.05",
  };

  vector<vector<double>> bkg_events_hists;
  vector<vector<double>> bkg_sigmas_hists;
  vector<vector<double>> bkg_eff_hists;
  vector<vector<double>> bkg_eff_sigmas_hists;
  vector<vector<double>> sig_events_hists;
  vector<vector<double>> sig_sigmas_hists;
  vector<vector<double>> sig_eff_hists;
  vector<vector<double>> sig_eff_sigmas_hists;

  // Background:
  double n_events;
  double n_events_weighted;
  double n_events_sigma;
  vector<double> bkg_events;
  vector<double> bkg_sigmas;
  vector<double> bkg_eff;
  vector<double> bkg_eff_sigmas;

  for(string hist_name : hist_names){
    bkg_events = {};
    bkg_sigmas = {};
    bkg_eff = {};
    bkg_eff_sigmas = {};
    for(auto &[file_name_, params] : background_files){
      string file_name = file_name_;
      file_name.erase(0,3);
      auto [color, title, signal, cross_sec, N_tot, BR] = params;
      auto input_file = TFile::Open((base_path_bkg+file_name).c_str());

      auto hist = (TH1D*)input_file->Get(hist_name.c_str());
      
      std::cout << hist_name << std::endl;
      n_events = hist->GetEntries();
      n_events_weighted = n_events*int_lumi*cross_sec*BR/N_tot;
      std::cout << BR << std::endl;
      // cout << n_events << "\t" << n_events_weighted << endl;
      n_events_sigma = sqrt(n_events)*int_lumi*cross_sec*BR/N_tot;
      // bkg_events.push_back(n_events_weighted);
      bkg_events.push_back(n_events_weighted);
      bkg_sigmas.push_back(n_events_sigma);
      bkg_eff.push_back(100*n_events/N_tot);
      bkg_eff_sigmas.push_back(100*sqrt(n_events)/N_tot);
    }
    bkg_events_hists.push_back(bkg_events);
    bkg_sigmas_hists.push_back(bkg_sigmas);
    bkg_eff_hists.push_back(bkg_eff);
    bkg_eff_sigmas_hists.push_back(bkg_eff_sigmas);
  }

  cout << "  ----------------  " << endl;
  vector<double> sig_events;
  vector<double> sig_sigmas;
  vector<double> sig_eff;
  vector<double> sig_eff_sigmas;
  for(string hist_name : hist_names){
    cout << hist_name << endl;
    sig_events = {};
    sig_sigmas = {};
    sig_eff = {};
    sig_eff_sigmas = {};
    for(auto &[file_name_, params] : signal_files){
      string file_name = file_name_;
      file_name.erase(0,3);
      cout << file_name << endl;
      auto [color, title, signal, cross_sec, N_tot, BR] = params;
      auto input_file = TFile::Open((base_path_sig+file_name).c_str());
    
      auto hist = (TH1D*)input_file->Get(hist_name.c_str());
      
      n_events = 0;
      for(int i=0; i < hist->GetNbinsX()+1; i++)
      {
        n_events += hist->GetBinContent(i);
      }
      n_events_weighted = n_events*int_lumi*cross_sec*BR/N_tot;
      // cout << n_events << "\t" << n_events_weighted << endl;
      n_events_sigma = sqrt(n_events)*int_lumi*cross_sec*BR/N_tot;
      // sig_events.push_back(n_events_weighted);
      sig_events.push_back(n_events_weighted);
      sig_sigmas.push_back(n_events_sigma);
      // cout << n_events << "\t" << N_tot << endl;
      sig_eff.push_back(100*n_events/N_tot);
      sig_eff_sigmas.push_back(100*sqrt(n_events)/N_tot);
    }
    sig_events_hists.push_back(sig_events);
    sig_sigmas_hists.push_back(sig_sigmas);
    sig_eff_hists.push_back(sig_eff);
    sig_eff_sigmas_hists.push_back(sig_eff_sigmas);
  }

  double bkg_n;
  double bkg_sigma;
  // for(int i = 0; i<hist_names.size(); i++){
  //   vector<double> s = sig_events_hists[i];
  //   vector<double> s_eff = sig_eff_hists[i];
  //   vector<double> b = bkg_events_hists[i];
  //   vector<double> b_sigma = bkg_sigmas_hists[i];
  //   vector<double> b_eff = bkg_eff_hists[i];
  //   bkg_n = B(bkg_events);
  //   bkg_sigma = B_sigma(bkg_sigmas);
  //   vector<double> fom = figure_of_merit(sig_events, bkg_n, bkg_sigma);
  //   cout << "--- " << hist_names[i] << endl;
  //   cout << "   --- Backgrounds:" << endl;
  //   for(int j=0; j<b.size(); j++){
  //     cout << "\t" << b[j] << "\t" << b_eff[j] << endl;
  //   }
  //   cout << "   --- Signals:" << endl;
  //   for(int j=0; j<s.size(); j++){
  //     cout << "\t" << s[j] << "\t" << s_eff[j] << "\t" << fom[j] << endl;
  //   }
  // }

  // for(int i = 0; i<hist_names.size(); i++){
  vector<double> s_start = sig_events_hists[0];
  int j = 0;
  // for(int j=0; j<s_start.size(); j++){
  for(auto &[file_name_, params] : signal_files){
    auto [color, title, signal, cross_sec, N_tot, BR] = params;
    std::cout << "---------------------- SIGNAL: " << title << " ---------------------- " << std::endl;
    for(int i = 0; i<hist_names.size(); i++){
      vector<double> s = sig_events_hists[i];
      vector<double> s_sig = sig_sigmas_hists[i];
      vector<double> s_eff = sig_eff_hists[i];
      vector<double> s_eff_sig = sig_eff_sigmas_hists[i];
      std::cout << cut_str[i] << "\t\t\t" << s[j] << "  +-  " << s_sig[j] << "\t\t\t" << s_eff[j] << "  +-  " << s_eff_sig[j] << std::endl;
    }
    j++;
  }
  // }

  vector<double> b_start = bkg_events_hists[0];
  j = 0;
  // for(int j=0; j<b_start.size(); j++){
  for(auto &[file_name_, params] : background_files){
    auto [color, title, signal, cross_sec, N_tot, BR] = params;
    std::cout << "---------------------- BACKGROUND: " << title << " ---------------------- " << std::endl;
    for(int i = 0; i<hist_names.size(); i++){
      vector<double> b = bkg_events_hists[i];
      vector<double> b_sig = bkg_sigmas_hists[i];
      vector<double> b_eff = bkg_eff_hists[i];
      vector<double> b_eff_sig = bkg_eff_sigmas_hists[i];
      std::cout << cut_str[i] << "\t\t\t" << b[j] << "  +-  " << b_sig[j] << "\t\t\t" << b_eff[j] << "  +-  " << b_eff_sig[j] << std::endl;
    }
    j++;
  }

  string output_file =  "test.txt";
  print_latex(output_file, hist_names, sig_events_hists, sig_sigmas_hists, bkg_events_hists, bkg_sigmas_hists);

  output_file =  "test_eff.txt";
  print_latex(output_file, hist_names, sig_eff_hists, sig_eff_sigmas_hists, bkg_eff_hists, bkg_eff_sigmas_hists);

};
