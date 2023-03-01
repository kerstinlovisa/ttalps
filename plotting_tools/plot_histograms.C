void plot_histograms()
{
  // Options for plotting:
  bool save_plots = false;
  bool one_canvas = true;

  string base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps/data.nosync/hists/";
  // string base_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/hists/";
  // string base_path = "/nfs/dust/cms/user/lrygaard/ttalps/hists/";
  // string output_path = "/afs/desy.de/user/l/lrygaard/ALPpheno/plots/";

  
  map<string, tuple<int, string>> file_names = {
    {"muon_siblings/ttj.root",                  {kRed, "ttj pair"}},
    {"muon_siblings/ttmumu.root",               {kOrange, "tt#mu#mu pair"}},
    {"muon_siblings/tta_mAlp-0p3GeV.root",      {kOrange+2, "0.3 GeV pair"}},
    
    {"single_muon/ttj.root",                    {kViolet, "ttj single"}},
    {"single_muon/ttmumu.root",                 {kBlue, "tt#mu#mu single"}},
    {"single_muon/tta_mAlp-0p3GeV.root",        {kCyan+1, "0.3 GeV single"}},
    
    {"muon_non_siblings/ttj.root",              {kBlack, "ttj non-pair"}},
    {"muon_non_siblings/ttmumu.root",           {kBlack, "tt#mu#mu non-pair"}},
    {"muon_non_siblings/tta_mAlp-0p3GeV.root",  {kBlack, "0.3 GeV non-pair"}},
  };
  
  map<string, tuple<bool, bool, int, double, double>> hist_names = {
//                          logy  logx    rebin   xMin    xMax
    {"muon_pt",             {true, false,  1,      0,      100   }},
    {"muon_pz",             {true, false,  10,     0,      100   }},
    {"muon_mass",           {true, false,  10,     0.1,    100   }},
    {"muon_lxy",            {true, false,  1,      0,      20    }},
    {"muon_lxy_rebinned",   {true, false,  1,      0,      11    }},
    {"muon_lz",             {true, false,  1,      0,      20    }},
    {"muon_lxyz",           {true, false,  1,      0,      20    }},
    {"muon_ctau",           {true, false,  1,      0,      20    }},
    {"muon_boost",          {true, false,  20,     0,      120   }},
    {"dimuon_pt",           {true, false,  10,     0,      100   }},
    {"dimuon_pz",           {true, false,  10,     0,      100   }},
    {"dimuon_mass",         {true, true ,  10,     0.1,    100   }},
    {"first_mother_pt",     {true, false,  1,      0,      100   }},
    {"first_mother_pz",     {true, false,  10,     0,      100   }},
    {"first_mother_mass",   {true, false,  10,     0.1,    100   }},
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
    "final_selection/final_selection_",
    "intermediate_selections/sel_pt-10GeV_os_",
    // "intermediate_selections/sel_pt-10GeV_ss_",
    "intermediate_selections/sel_pt-10GeV_mass-Jpsi_os_",
    // "intermediate_selections/sel_pt-10GeV_mass-Jpsi_ss_",
    //  "intermediate_selections/sel_pt-10GeV_mass-Jpsi_dlxy-max0p1cm_os",
    //  "intermediate_selections/sel_pt-10GeV_mass-Jpsi_dlxy-max0p1cm_ss",
  };
  
  map<string, THStack*> stacks;
  for(auto &[hist_name, tmp] : hist_names){
    for(auto prefix : prefixes){
      string full_hist_name =  prefix + hist_name;
      stacks[full_hist_name] = new THStack();
    }
  }
  
  auto legend = new TLegend(0.75, 0.75, 0.9, 0.9);
  vector<string> in_legend;
  
  for(auto &[file_name, params] : file_names){
    auto [color, title] = params;
    
    cout<<"Loading file: "<<file_name<<endl;
    
    auto input_file = TFile::Open((base_path+file_name).c_str());
    
    for(auto &[hist_name, params] : hist_names){
      for (auto prefix : prefixes){
        string full_hist_name = prefix + hist_name;

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
        input_file->cd();
      }
    }
  }
  
  if(one_canvas){
    auto canvas = new TCanvas("canvas", "canvas", 2000, 4000);
    canvas->Divide(4, 4);

    int i_pad = 1;
    for(auto &[hist_name, params] : hist_names){
      for(auto prefix : prefixes){
        string full_hist_name =  prefix + hist_name;
      
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

  if(save_plots){
    cout << "Saving all plots in: " << output_path << endl;
    gROOT->SetBatch(kTRUE);
    for(auto &[hist_name, params] : hist_names){
      for(auto prefix : prefixes){
        string full_hist_name = prefix + hist_name;
    
        auto [logy, logx, rebin, xMin, xMax] = params;

        auto c = new TCanvas("c", "c");
        c->cd();
        if(logy) c->SetLogy();
        if(logx) c->SetLogx();
        stacks[full_hist_name]->Draw();
        stacks[full_hist_name]->GetXaxis()->SetLimits(xMin, xMax);
      
        legend->Draw(); 

        c->Update();
        
        string file_name = output_path + full_hist_name + ".pdf";
        c->SaveAs(file_name.c_str());
      }
    }
  }

}
