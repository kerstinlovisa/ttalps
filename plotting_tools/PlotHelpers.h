TH1D* get_hist_with_same_width_bins(TH1D* input_hist, string input_hist_name, vector<int> lxy_bins, float rebin, float int_lumi, float cross_sec, float BR, float N_tot)
{
  int n_bins = lxy_bins.size();
  TH1D* hist = new TH1D((input_hist_name+"_1widthbins").c_str(), (input_hist_name+"_1widthbins").c_str(), n_bins-1, 0, n_bins-1);
  for(int i=0; i<n_bins-1; i++)
  {
    hist->SetBinContent(i+1, input_hist->GetBinContent(i+1));
  }
  hist->GetXaxis()->SetLabelSize(0.04);
  return hist;
}

TH1D* get_lxy_with_outer_tracker(TH1D* input_hist, string input_hist_name, vector<int> lxy_bins, float x_max, float rebin, float int_lumi, float cross_sec, float BR, float N_tot)
{
  float binListExtended[8] = {0, 2, 10, 24, 31, 70, 110, x_max}; // mm
  int n_bins_max = 8;
  int n_bins = 7;
  int n_bins_i = 0;
  for(int i=0; i<n_bins_max; i++)
  {
    float value = input_hist->GetBinContent(i+1)*rebin*int_lumi*cross_sec*BR/N_tot;
    if( value < 0.00001) break;
    n_bins_i++;
  }
  // TH1D* hist = input_hist.Clone();
  double outer_tracker_content;
  if(n_bins_i >= 8) {
    outer_tracker_content = input_hist->GetBinContent(7+1);
    n_bins = n_bins_i;
  }
  else {n_bins = n_bins_i+1;}
  float binList[n_bins];
  for(int i=0; i<n_bins_i+1; i++)
  {
    binList[i] = binListExtended[i];
  }
  if(n_bins_i < 8) {binList[n_bins_i] = binList[n_bins_i-1] + 1e-10;}
  
  TH1D* hist = new TH1D((input_hist_name+"_outer-tracker").c_str(), (input_hist_name+"_outer-tracker").c_str(), n_bins-1, binList);
  for(int i=0; i<n_bins_i; i++)
  {
    // if(input_hist->GetBinContent(i+1) < y_max) break;
    hist->SetBinContent(i+1, input_hist->GetBinContent(i+1));
  }
  if(n_bins_i >= 8) {
    std::cout << n_bins_i << std::endl;
    hist->SetBinContent(n_bins_i+1, outer_tracker_content);
  }
  if(n_bins_i < 8) {binList[n_bins_i+1] = 1e-10;}
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
  if (hist_name == "minlxy-muon_lxy_rebinned_extended") {lxy_bins = {0, 2, 10, 24, 31, 70, 110, 1300, 3000, 7300};} 
  if (hist_name == "minlxy-muon_lxy_rebinned_extended_gen") {lxy_bins = {0, 110, 1300, 3000, 7300};}
  if (hist_name == "minlxy-muon_lxy_rebinned_extended_general") {lxy_bins = {0, 110, 1300, 3000, 7300};}
  for(int i=0; i<hist->GetNbinsX(); i++){
    hist->SetBinContent(i+1, hist->GetBinContent(i+1)/(lxy_bins[i+1]-lxy_bins[i]));
  }
  return lxy_bins;
}

void set_hist_layout(THStack* stack, tuple<bool, bool, bool, int, double, double, double, double, string, string> params, bool weighted)
{
  auto [logy, logx, rebinned, rebin, xMin, xMax, yMin, yMax, xlabel, ylabel] = params;
  stack->GetXaxis()->SetLimits(xMin, xMax);
  if(yMax != 0){
    stack->SetMaximum(yMax);
    stack->SetMinimum(yMin);
  }
  stack->GetXaxis()->SetTitle(xlabel.c_str());
  stack->GetXaxis()->SetTitleSize(0.050);
  stack->GetXaxis()->SetLabelSize(0.050);
  stack->GetYaxis()->SetTitleSize(0.050);
  stack->GetYaxis()->SetLabelSize(0.050);
  if (weighted) stack->GetYaxis()->SetTitle(ylabel.c_str());
  else stack->GetYaxis()->SetTitle("Fraction of events");
  stack->GetXaxis()->SetRangeUser(xMin, xMax);
  stack->GetXaxis()->SetTitleOffset(1.2);
}

void set_legend_layout(TLegend* legend)
{
  legend->SetNColumns(1);
  legend->SetBorderSize(0);
  legend->SetTextSize(0.050);
  legend->SetTextFont(42);
}

void draw_legends_and_text(TLegend* legend_sig, TLegend* legend_bkg, vector<const char*> selections, string prefix, double x_selection, bool weighted, bool include_ctau) {
  
  vector<const char*> preselections = {
    "l_{xy} > 200 #mum",
    "|#eta^{#mu}| < 2.5",
    "p_{T}^{#mu} > 5 GeV",
  };

  if(legend_sig) legend_sig->Draw();
  legend_bkg->Draw();
  TLatex latex;
  latex.SetTextSize(0.050);
  latex.SetTextFont(42);
  latex.SetNDC(kTRUE);
  if(weighted) latex.DrawLatex(0.53, 0.91, "L = 150 fb^{-1}, #sqrt{s} = 13 TeV");
  else latex.DrawLatex(0.73, 0.91, "#sqrt{s} = 13 TeV");
  double y = 0.84;
  if(prefix.substr(0,15) == "final_selection") {
    for(auto sel : selections){
      latex.DrawLatex(x_selection, y, sel);
      y -= 0.06;
    }
  } else {
    for(auto sel : preselections){
      latex.DrawLatex(x_selection, y, sel);
      y -= 0.06;
    }
  }
  if(include_ctau) latex.DrawLatex(0.46, 0.84, "m_{a} = 0.35 GeV");
}

void add_epsilon_to_zero_bins(TH1D* hist, float epsilon){
  for(int i=0; i<hist->GetNbinsX()+1; i++){
    if(hist->GetBinContent(i) == 0) {
      hist->SetBinContent(i, epsilon);
    }
  }
}

vector<TH1D*> break_into_smaller_histograms(TH1D* hist, float ymax, bool logx) {
  vector<vector<tuple<float,float,int> > > hist_values;
  vector<tuple<float,float,int> > values; 
  bool in_hist = false;

  for(int i=0; i<hist->GetNbinsX(); i++){
    float value = hist->GetBinContent(i+1);
    
    if (value <= ymax) {
      if (in_hist) {
        in_hist = false;
        hist_values.push_back(values);
        values = {};
      }
      continue;
    } else {
      in_hist = true;
      values.push_back(make_tuple(hist->GetBinCenter(i+1), value, i+1));
    }
  }
  if(in_hist) {hist_values.push_back(values);}

  float bin_width = hist->GetBinWidth(1);
  vector<TH1D*> hists;
  
  for(int i=0; i<hist_values.size(); i++) {
    vector<tuple<float,float,int> > v = hist_values[i];

    int n_bins = int((get<0>(v.back()) - get<0>(v[0]))/bin_width) + 1;

    float min_x = get<0>(v[0]) - bin_width/2;
    float max_x = get<0>(v.back()) + bin_width/2;

    float* bin_list;

    if(logx){
      n_bins = get<2>(v.back()) - get<2>(v[0]) + 1;
      float bin_width_min = hist->GetBinWidth(get<2>(v[0]));
      float bin_width_max = hist->GetBinWidth(get<2>(v.back()));
      min_x = get<0>(v[0]) - bin_width_min/2;
      max_x = get<0>(v.back()) + bin_width_max/2;

      bin_list = new float[n_bins+3];
      int j=1;
      for (int k=0; k<n_bins+2; k++) {
        bin_list[j] = (pow(10,log10(min_x)+((log10(max_x)-log10(min_x))/n_bins)*k));
        j++;
      }
    }
    else{
        bin_list = new float[n_bins+3];

        int j=1;
        for(float bin_edge=min_x; bin_edge<max_x; bin_edge+=bin_width){
            bin_list[j] = bin_edge;
            j++;
        }
    }
    bin_list[n_bins+1] = max_x;
    bin_list[0] = min_x - 1e-10;
    bin_list[n_bins+2] = max_x + 1e-10;

    for(int k=0; k<= n_bins+2; k++){
    }

    auto hist_new =  new TH1D(("hist_" + to_string(i)).c_str(), ("hist_" + to_string(i)).c_str(), n_bins+2, bin_list);
    hists.push_back(hist_new);

    hists.back()->SetBinContent(1, 1e-10);
    for(int i=0; i<v.size(); i++){
      hists.back()->SetBinContent(i+2, get<1>(v[i]));
    }
    hists.back()->SetBinContent(n_bins+2, 1e-10);
  }
      
  return hists;
}

