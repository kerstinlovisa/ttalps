void plot_histograms()
{
  // string base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/";
  string base_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/hists/";
  // string base_path = "/nfs/dust/cms/user/lrygaard/ttalps/hists/";
  
  map<string, tuple<int, string>> file_names = {
    {"muon_siblings/ttj.root",                  {kRed, "ttj pair"}},
    // {"muon_siblings/ttmumu.root",               {kOrange, "tt#mu#mu pair"}},
    // {"muon_siblings/tta_mAlp-0p3GeV.root",      {kOrange+2, "0.3 GeV pair"}},
    
    // {"single_muon/ttj.root",                    {kViolet, "ttj single"}},
    // {"single_muon/ttmumu.root",                 {kBlue, "tt#mu#mu single"}},
    // {"single_muon/tta_mAlp-0p3GeV.root",        {kCyan+1, "0.3 GeV single"}},
    
    {"muon_non_siblings/ttj.root",              {kBlack, "ttj non-pair"}},
    // {"muon_non_siblings/ttmumu.root",           {kBlack, "tt#mu#mu non-pair"}},
    // {"muon_non_siblings/tta_mAlp-0p3GeV.root",  {kBlack, "0.3 GeV non-pair"}},
  };
  
  map<string, tuple<bool, bool, int, double, double>> hist_names = {
//                          logy  logx    rebin   xMin    xMax
    {"muon_pt",             {true, false,  1,      0,      100   }},
    {"muon_pz",             {true, false,  10,     -1000,  1000  }},
    {"muon_mass",           {true, false,  1,      0,      20    }},
    {"muon_lxy",            {true, false,  1,      0,      20    }},
    {"muon_lz",             {true, false,  1,      0,      20    }},
    {"muon_lxyz",           {true, false,  1,      0,      20    }},
    {"muon_ctau",           {true, false,  1,      0,      20    }},
    {"muon_boost",          {true, false,  20,     0,      120   }},
    {"dimuon_pt",           {true, false,  10,     0,      1000  }},
    {"dimuon_pz",           {true, false,  10,     -400,   400   }},
    {"dimuon_mass",         {true, true ,  1,      0.1,    10    }},
    {"first_mother_pt",     {true, false,  1,      0,      200   }},
    {"first_mother_pz",     {true, false,  10,     -1000,  1000  }},
    {"first_mother_mass",   {true, false,  1,      0,      250   }},
    {"first_mother_lxy",    {true, false,  1,      0,      10    }},
    {"first_mother_lz",     {true, false,  1,      0,      10    }},
    {"first_mother_lxyz",   {true, false,  1,      0,      10    }},
    {"first_mother_ctau",   {true, false,  1,      0,      10    }},
    {"first_mother_boost",  {true, false,  20,     0,      120   }},
  };

  vector<string> prefixes = {
    "os_",
    // "ss_",
    // "single_",
  };

  vector<string> selections = {
    "",
    "sel_pt-10GeV_",
    "sel_pt-10GeV_mass-Jpsi_",
    "sel_pt-10GeV_mass-Jpsi_lxy-2p4cm_",
    "sel_pt-10GeV_mass-Jpsi_lxy-3p1cm_",
    "sel_pt-10GeV_mass-Jpsi_lxy-7p0cm_",
    "sel_pt-10GeV_mass-Jpsi_lxy-11p0cm_",
  };
  
  map<string, THStack*> stacks;
  for(auto &[hist_name, tmp] : hist_names){
    for(auto prefix : prefixes){
      string full_hist_name = prefix + hist_name;
      stacks[full_hist_name] = new THStack();
    }
  }
  
  auto canvas = new TCanvas("canvas", "canvas", 2000, 4000);
  canvas->Divide(4, 4);
  
  auto legend = new TLegend(0.6, 0.6, 0.9, 0.9);
  vector<string> in_legend;
  
  for(auto &[file_name, params] : file_names){
    auto [color, title] = params;
    
    cout<<"Loading file: "<<file_name<<endl;
    
    auto input_file = TFile::Open((base_path+file_name).c_str());
    
    for(auto &[hist_name, params] : hist_names){
      for (auto prefix : prefixes){
        // for(auto sel : selections){
        string full_hist_name = prefix + hist_name;
        cout << full_hist_name << endl;
        auto hist = (TH1D*)input_file->Get(full_hist_name.c_str());
        auto [logy, logx, rebin, xMin, xMax] = params;
        
        if(hist->GetEntries() == 0) continue;
        
        hist->SetLineColor(color);
        hist->Rebin(rebin);
        hist->Scale(rebin/hist->GetEntries());
        hist->Sumw2(false);
        
        stacks[full_hist_name]->Add(hist);
        stacks[full_hist_name]->SetTitle(hist->GetTitle());
      
        if(find(in_legend.begin(), in_legend.end(), file_name) == in_legend.end()){
          legend->AddEntry(hist, title.c_str(), "l");
          in_legend.push_back(file_name);
        }
      } 
    }
  }
  
  int i_pad = 1;
  for(auto &[hist_name, params] : hist_names){
    for(auto prefix : prefixes){
      string full_hist_name = prefix + hist_name;
    
      auto [logy, logx, rebin, xMin, xMax] = params;
    
      canvas->cd(i_pad++);
      if(logy) gPad->SetLogy();
      if(logx) gPad->SetLogx();
      stacks[full_hist_name]->Draw();

      stacks[full_hist_name]->GetXaxis()->SetLimits(xMin, xMax);
      
      legend->Draw(); 
    }
  }
  
  canvas->Update();
  canvas->SaveAs("hists.pdf");
}
