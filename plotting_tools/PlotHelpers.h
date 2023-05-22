TH1D* get_hist_with_same_width_bins(TH1D* input_hist, string input_hist_name, vector<int> lxy_bins)
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

TH1D* get_lxy_with_outer_tracker(TH1D* input_hist, string input_hist_name, vector<int> lxy_bins, float x_max)
{
  float binListExtended[8] = {0, 2, 10, 24, 31, 70, 110, x_max}; // mm
  int n_bins = 7;
  // TH1D* hist = input_hist.Clone();
  double outer_tracker_content = input_hist->GetBinContent(7+1);
  TH1D* hist = new TH1D((input_hist_name+"_outer-tracker").c_str(), (input_hist_name+"_outer-tracker").c_str(), n_bins, binListExtended);
  for(int i=0; i<n_bins; i++)
  {
    hist->SetBinContent(i+1, input_hist->GetBinContent(i+1));
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
  if (hist_name == "minlxy-muon_lxy_rebinned_extended") {lxy_bins = {0, 2, 10, 24, 31, 70, 110, 1300, 3000, 7300};} 
  if (hist_name == "minlxy-muon_lxy_rebinned_extended_gen") {lxy_bins = {0, 110, 1300, 3000, 7300};}
  if (hist_name == "minlxy-muon_lxy_rebinned_extended_general") {lxy_bins = {0, 110, 1300, 3000, 7300};}
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
  stack->GetXaxis()->SetTitleSize(0.050);
  stack->GetXaxis()->SetLabelSize(0.050);
  stack->GetYaxis()->SetTitleSize(0.050);
  stack->GetYaxis()->SetLabelSize(0.050);
  stack->GetYaxis()->SetTitle(ylabel.c_str());
  stack->GetXaxis()->SetRangeUser(xMin, xMax);
  stack->GetXaxis()->SetTitleOffset(1.2);
}

void add_epsilon_to_zero_bins(TH1D* hist, float epsilon){
  for(int i=0; i<hist->GetNbinsX()+1; i++){
    if(hist->GetBinContent(i) == 0) {
      std::cout << hist->GetBinContent(i) << std::endl;
      hist->SetBinContent(i, epsilon);
      std::cout << hist->GetBinContent(i) << std::endl;
    }
  }
}