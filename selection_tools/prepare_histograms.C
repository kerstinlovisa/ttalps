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
#include "CutsManager.hpp"

using namespace std;

int max_events = -1;
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
  auto output_file = new TFile(output_path.c_str(), "recreate");
  
// load events
  auto event_reader = EventReader(max_events, n_daughters);
  auto events = event_reader.read_events(input_tree);
  
  vector<string> particle_names = {
    // "single_muon",
    // "single_muon_first_mother",
    "os_maxlxy-muon",
    "os_minlxy-muon",
    // "ss_muon",
    "os_dimuon",
    // "ss_dimuon",
    // "os_first_mother",
    // "ss_first_mother",
  };

  vector<string> hist_names = {
    "", // this is without any selection
  
    // Single (intermediate) selections
    "sel_pt-min5GeV_",
    "sel_pt-min10GeV_",
    "sel_pt-min15GeV_",

    "sel_mass-cuts_",

    "sel_deltalxy-max0p3mm_",
    "sel_deltalxy_ratio_abs-max0p05_",
    "sel_deltalxy_ratio_abs-max0p1_",
    "sel_deltalxy_ratio_abs-max0p5_",

    // Final selections with different combinations for N-1 plots
    // pT > 10 GeV + dimuon mass cuts
    "final_selection_pt-min10GeV_mass-cuts_",
    "final_selection_pt-min5GeV_mass-cuts_",
    "final_selection_pt-min15GeV_mass-cuts_",

    // pT > 10 GeV + dimuon mass cuts + deltalxy cut
    "final_selection_pt-min10GeV_mass-cuts_deltalxy-max0p3mm_",
    "final_selection_pt-min10GeV_mass-cuts_deltalxy_ratio_abs-max0p05_",
    "final_selection_pt-min10GeV_mass-cuts_deltalxy_ratio_abs-max0p1_",
    "final_selection_pt-min10GeV_mass-cuts_deltalxy_ratio_abs-max0p5_",
    // including other pT cut values
    "final_selection_pt-min5GeV_mass-cuts_deltalxy-max0p3mm_",
    "final_selection_pt-min5GeV_mass-cuts_deltalxy_ratio_abs-max0p05_",
    "final_selection_pt-min5GeV_mass-cuts_deltalxy_ratio_abs-max0p1_",
    "final_selection_pt-min5GeV_mass-cuts_deltalxy_ratio_abs-max0p5_",
    "final_selection_pt-min15GeV_mass-cuts_deltalxy-max0p3mm_",
    "final_selection_pt-min15GeV_mass-cuts_deltalxy_ratio_abs-max0p05_",
    "final_selection_pt-min15GeV_mass-cuts_deltalxy_ratio_abs-max0p1_",
    "final_selection_pt-min15GeV_mass-cuts_deltalxy_ratio_abs-max0p5_",

    // pT > 10 GeV + deltalxy cut
    "final_selection_pt-min10GeV_deltalxy-max0p3mm_",
    "final_selection_pt-min10GeV_deltalxy_ratio_abs-max0p05_",
    "final_selection_pt-min10GeV_deltalxy_ratio_abs-max0p1_",
    "final_selection_pt-min10GeV_deltalxy_ratio_abs-max0p5_",

    "final_selection_pt-min5GeV_deltalxy-max0p3mm_",
    "final_selection_pt-min5GeV_deltalxy_ratio_abs-max0p05_",
    "final_selection_pt-min5GeV_deltalxy_ratio_abs-max0p1_",
    "final_selection_pt-min5GeV_deltalxy_ratio_abs-max0p5_",
    "final_selection_pt-min15GeV_deltalxy-max0p3mm_",
    "final_selection_pt-min15GeV_deltalxy_ratio_abs-max0p05_",
    "final_selection_pt-min15GeV_deltalxy_ratio_abs-max0p1_",
    "final_selection_pt-min15GeV_deltalxy_ratio_abs-max0p5_",

    "final_selection_mass-cuts_deltalxy-max0p3mm_",
    "final_selection_mass-cuts_deltalxy_ratio_abs-max0p05_",
    "final_selection_mass-cuts_deltalxy_ratio_abs-max0p1_",
    "final_selection_mass-cuts_deltalxy_ratio_abs-max0p5_",
  };
  
  map<string, HistogramSet*> histSets;
  for(string hist : hist_names){
    for(string particle : particle_names){
      string name = hist + particle;
      histSets[name] = new HistogramSet(name);
    }
  }

  auto cutsManager = CutsManager();
  
  auto fill_deltaR_deltal_selections = [&](const Particle* particle_1, const Particle* particle_2, string sign, string prefix){

    float epsilon = 1e-10;
    float x1 = particle_1->x;
    float y1 = particle_1->y;
    float x2 = particle_2->x + epsilon;
    float y2 = particle_2->y + epsilon;

    float delta_lxy = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
    float delta_lxy_ratio_abs = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))/sqrt(pow(abs(x1) + abs(x2), 2) + pow(abs(y1) + abs(y2), 2));

    if(delta_lxy <= 0.3){
      histSets[prefix + "_deltalxy-max0p3mm_"+sign+"_maxlxy-muon"]->fill(particle_1);
      histSets[prefix + "_deltalxy-max0p3mm_"+sign+"_minlxy-muon"]->fill(particle_2);
      histSets[prefix + "_deltalxy-max0p3mm_"+sign+"_dimuon"]->fill(particle_1, particle_2);
    }

    if(delta_lxy_ratio_abs <= 0.05){
      histSets[prefix + "_deltalxy_ratio_abs-max0p05_"+sign+"_maxlxy-muon"]->fill(particle_1);
      histSets[prefix + "_deltalxy_ratio_abs-max0p05_"+sign+"_minlxy-muon"]->fill(particle_2);
      histSets[prefix + "_deltalxy_ratio_abs-max0p05_"+sign+"_dimuon"]->fill(particle_1, particle_2);
    }
    if(delta_lxy_ratio_abs <= 0.1){
      histSets[prefix + "_deltalxy_ratio_abs-max0p1_"+sign+"_maxlxy-muon"]->fill(particle_1);
      histSets[prefix + "_deltalxy_ratio_abs-max0p1_"+sign+"_minlxy-muon"]->fill(particle_2);
      histSets[prefix + "_deltalxy_ratio_abs-max0p1_"+sign+"_dimuon"]->fill(particle_1, particle_2);
    }
    if(delta_lxy_ratio_abs <= 0.5){
      histSets[prefix + "_deltalxy_ratio_abs-max0p5_"+sign+"_maxlxy-muon"]->fill(particle_1);
      histSets[prefix + "_deltalxy_ratio_abs-max0p5_"+sign+"_minlxy-muon"]->fill(particle_2);
      histSets[prefix + "_deltalxy_ratio_abs-max0p5_"+sign+"_dimuon"]->fill(particle_1, particle_2);
    }
  };

  auto fill_hists = [&](const Particle* particle_1, const Particle* particle_2, const Event *event, string sign){
    if(!particle_1 || !particle_2) return;
    
    float lxy1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2));
    float lxy2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2));
    const Particle* particle_maxlxy;
    const Particle* particle_minlxy;
    if (lxy1>=lxy2){ 
      particle_maxlxy = particle_1;
      particle_minlxy = particle_2;
    }
    else { 
      particle_maxlxy = particle_2;
      particle_minlxy = particle_1;
    }
      
    histSets[sign+"_maxlxy-muon"]->fill(particle_maxlxy);
    histSets[sign+"_minlxy-muon"]->fill(particle_minlxy);
    histSets[sign+"_dimuon"]->fill(particle_1, particle_2);
    
    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;

    // Independent selections:
    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){
      histSets["sel_pt-min10GeV_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy);
      histSets["sel_pt-min10GeV_"+sign+"_minlxy-muon"]->fill(particle_minlxy);
      histSets["sel_pt-min10GeV_"+sign+"_dimuon"]->fill(particle_1, particle_2);
    }
    if(particle_1->four_vector.Pt() > 5 && particle_2->four_vector.Pt() > 5){
      histSets["sel_pt-min5GeV_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy);
      histSets["sel_pt-min5GeV_"+sign+"_minlxy-muon"]->fill(particle_minlxy);
      histSets["sel_pt-min5GeV_"+sign+"_dimuon"]->fill(particle_1, particle_2);
    }
    if(particle_1->four_vector.Pt() > 15 && particle_2->four_vector.Pt() > 15){
      histSets["sel_pt-min15GeV_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy);
      histSets["sel_pt-min15GeV_"+sign+"_minlxy-muon"]->fill(particle_minlxy);
      histSets["sel_pt-min15GeV_"+sign+"_dimuon"]->fill(particle_1, particle_2);
    }
    
    if(cutsManager.passes_mass_cuts(diparticle)){
      histSets["sel_mass-cuts_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy);
      histSets["sel_mass-cuts_"+sign+"_minlxy-muon"]->fill(particle_minlxy);
      histSets["sel_mass-cuts_"+sign+"_dimuon"]->fill(particle_1, particle_2);
    }
    
    fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, sign, "sel");
  };

  auto fill_final_selection_hists = [&](const Particle* particle_1, const Particle* particle_2, const Event *event, string sign){
    if(!particle_1 || !particle_2) return;
    
    float lxy1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2));
    float lxy2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2));
    const Particle* particle_maxlxy;
    const Particle* particle_minlxy;
    if (lxy1>=lxy2){ 
      particle_maxlxy = particle_1;
      particle_minlxy = particle_2;
    }
    else { 
      particle_maxlxy = particle_2;
      particle_minlxy = particle_1;
    }

    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;
    
    // With muon pT > 10 GeV
    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){     
      // With dimuon mass cuts
      if(cutsManager.passes_mass_cuts(diparticle)){
        histSets["final_selection_pt-min10GeV_mass-cuts_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy);
        histSets["final_selection_pt-min10GeV_mass-cuts_"+sign+"_minlxy-muon"]->fill(particle_minlxy);
        histSets["final_selection_pt-min10GeV_mass-cuts_"+sign+"_dimuon"]->fill(particle_1, particle_2);
        
        fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, sign, "final_selection_pt-min10GeV_mass-cuts");
      }
      // Without dimuon mass cuts
      fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, sign, "final_selection_pt-min10GeV");
    }
    // Without muon pT cut
    if(cutsManager.passes_mass_cuts(diparticle)){
      fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, sign, "final_selection_mass-cuts");
    }
    
    // With muon pT > 5 GeV
    if(particle_1->four_vector.Pt() > 5 && particle_2->four_vector.Pt() > 5){     
      // With dimuon mass cuts
      if(cutsManager.passes_mass_cuts(diparticle)){
        histSets["final_selection_pt-min5GeV_mass-cuts_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy);
        histSets["final_selection_pt-min5GeV_mass-cuts_"+sign+"_minlxy-muon"]->fill(particle_minlxy);
        histSets["final_selection_pt-min5GeV_mass-cuts_"+sign+"_dimuon"]->fill(particle_1, particle_2);
        
        fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, sign, "final_selection_pt-min5GeV_mass-cuts");
      }
      // Without dimuon mass cuts
      fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, sign, "final_selection_pt-min5GeV");
    }
    // With muon pT > 15 GeV
    if(particle_1->four_vector.Pt() > 15 && particle_2->four_vector.Pt() > 15){     
      // With dimuon mass cuts
      if(cutsManager.passes_mass_cuts(diparticle)){
        histSets["final_selection_pt-min15GeV_mass-cuts_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy);
        histSets["final_selection_pt-min15GeV_mass-cuts_"+sign+"_minlxy-muon"]->fill(particle_minlxy);
        histSets["final_selection_pt-min15GeV_mass-cuts_"+sign+"_dimuon"]->fill(particle_1, particle_2);
        
        fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, sign, "final_selection_pt-min15GeV_mass-cuts");
      }
      // Without dimuon mass cuts
      fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, sign, "final_selection_pt-min15GeV");
    }
  };

  for(auto event : events){
    
    if(!event->has_ttbar_pair()) continue;
    int preselection_code = event->passes_preselection();
    
    if(preselection_code == 0){
      continue;
    }
    else if(preselection_code == 2 || preselection_code == 3){ // non-pair category

      // auto [opposite_sign_muon_1, opposite_sign_muon_2] = event->get_smallest_deltaR_opposite_sign_muon_non_pair();
      auto [opposite_sign_muon_1, opposite_sign_muon_2] = event->get_smallest_deltaLxyRatio_opposite_sign_muons();
      
      fill_hists(opposite_sign_muon_1, opposite_sign_muon_2, event, "os");
      fill_final_selection_hists(opposite_sign_muon_1, opposite_sign_muon_2, event, "os");
    }
  }
  
  // close files
  output_file->cd();
  output_file->mkdir("final_selection");
  output_file->mkdir("intermediate_selections");
  for(auto &[hist_name, hist_set] : histSets){
    if(hist_name.substr(0,15) == "final_selection"){
      output_file->cd("final_selection");
    }
    if(hist_name.substr(0,3) == "sel"){
      output_file->cd("intermediate_selections");
    }
    for(auto &[tmp_2, hist] : hist_set->hists){
      hist->Write();
    }
    output_file->cd();
  }
  
  input_file->Close();
  output_file->Close();
  
  return 0;
}
