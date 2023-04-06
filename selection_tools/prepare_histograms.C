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

TTree* get_input_tree(string input_path)
{
  input_file = TFile::Open(input_path.c_str());
  
  if(!input_file){
    cout<<"ERROR -- could not open input file: "<<input_path<<endl;
    exit(0);
  }
  
  return (TTree*)input_file->Get("Events");
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

  histogramFiller.save_histograms(output_path);
  input_file->Close();
  return 0;
}
