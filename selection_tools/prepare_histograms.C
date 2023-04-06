#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#include <TFile.h>
#include <TTree.h>
#include <TH1D.h>

#include "Particle.hpp"
#include "Event.hpp"
#include "EventReader.hpp"
#include "HistogramSet.hpp"
#include "Helpers.hpp"
#include "HistogramFiller.hpp"

using namespace std;

int max_events = 1000;
int n_daughters = 100;

TFile *input_file;
TH1D *baseline_hist;

TTree* get_input_tree(string input_path)
{
  input_file = TFile::Open(input_path.c_str());
  
  if(!input_file){
    cout<<"ERROR -- could not open input file: "<<input_path<<endl;
    exit(0);
  }
  
  return (TTree*)input_file->Get("Events");
}

TH1D* fill_and_save_histograms(const vector<Event*> &events, string output_path)
{
  auto histogramFiller = HistogramFiller();
  
  for(auto event : events){
    if(!event->has_ttbar_pair()) continue;
    int preselection_code = event->passes_preselection();
    
    if(preselection_code == 0){
      continue;
    }
    else if(preselection_code == 2 || preselection_code == 3){ // pair or non-pair category
      auto [muon_1, muon_2] = event->get_smallest_deltaLxyRatio_opposite_sign_muons();
      
      histogramFiller.fill_hists(muon_1, muon_2, event, "os");
      histogramFiller.fill_final_selection_hists(muon_1, muon_2, event, "os");
    }
    
    for(auto muon : event->particles){
      if(!muon->is_muon()) continue;;
      if(!muon->has_alp_ancestor(event->particles)) continue;
      histogramFiller.fill_alp_selection_hists(muon, event);
      break;
    }
  }
  auto baseline_hist = new TH1D(*histogramFiller.histSets["alp_selection_os_minlxy-muon"]->hists["proper_ctau"]);
  
  histogramFiller.save_histograms(output_path);
  
  return baseline_hist;
}

TH1D* get_weights_histogram(TH1D* baseline_hist, double destination_lifetime)
{
  double fit_max = 0.1;
  
  auto scaled_lifetime_function = new TF1("scaled_lifetime_function", "[0]*exp(-x/[1])", 0, fit_max);
  scaled_lifetime_function->SetParameter(0, 1);
  scaled_lifetime_function->FixParameter(1, destination_lifetime);
  
  baseline_hist->Fit(scaled_lifetime_function, "", "", 0, fit_max);
  
  auto hist_tmp= new TH1D("hist_scaled", "hist_scaled",
                           baseline_hist->GetNbinsX(),
                           baseline_hist->GetXaxis()->GetBinLowEdge(1),
                           baseline_hist->GetXaxis()->GetBinLowEdge(baseline_hist->GetNbinsX())+baseline_hist->GetXaxis()->GetBinWidth(baseline_hist->GetNbinsX()));
  
  auto weights = new TH1D("weights", "weights",
                          baseline_hist->GetNbinsX(),
                          baseline_hist->GetXaxis()->GetBinLowEdge(1),
                          baseline_hist->GetXaxis()->GetBinLowEdge(baseline_hist->GetNbinsX())+baseline_hist->GetXaxis()->GetBinWidth(baseline_hist->GetNbinsX()));
  
  for(int i_bin=1; i_bin<baseline_hist->GetNbinsX()+1; i_bin++){
    double value = baseline_hist->GetXaxis()->GetBinCenter(i_bin);
    double content = baseline_hist->GetBinContent(i_bin);
    double weight = 0;
    if(content > 0) weight = scaled_lifetime_function->Eval(value)/content;
    
    hist_tmp->SetBinContent(i_bin, content*weight);
    weights->SetBinContent(i_bin, weight);
  }
  double scale = baseline_hist->Integral()/hist_tmp->Integral();
  weights->Scale(scale);
  
  return weights;
}

int main(int argc, char *argv[])
{
  if(argc != 3){
    cout<<"Usage: ./prepare_histograms input_path output_path"<<endl;
    exit(0);
  }
  
  string input_path = argv[1];
  string output_path = argv[2];
  
  auto input_tree = get_input_tree(input_path);
  
  
// load events
  auto event_reader = EventReader(max_events, n_daughters);
  auto events = event_reader.read_events(input_tree);
  
  TH1D *baseline_hist = fill_and_save_histograms(events, output_path);
  
  vector<double> destination_lifetimes = {1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4}; // mm
  
  for(double destination_lifetime : destination_lifetimes){
    
    TH1D *weights_hist = get_weights_histogram(baseline_hist, destination_lifetime);
    
    // set new event weights
    for(auto event : events){
      double event_proper_lifetime = event->get_proper_lifetime();
      int weight_bin = weights_hist->GetXaxis()->FindFixBin(event_proper_lifetime);
      double weight = weights_hist->GetBinContent(weight_bin);
      if(weight < 0){
        cout<<"Found event for which weight cannot be calculated..."<<endl;
        weight = 1;
      }
      event->weight = weight;
    }
    
    string lifetime_output_path = replace_all(output_path, ".root", "_ctau-"+to_nice_string(destination_lifetime, 6)+"mm.root");
    fill_and_save_histograms(events, lifetime_output_path);
  }
  
  input_file->Close();
  return 0;
}
