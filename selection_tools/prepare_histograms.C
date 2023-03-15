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

using namespace std;

int max_events = -1;
int n_daughters = 100;

// Some final selections maxima/minima
float Jpsi_mass = 3.096900; // GeV
// widths = sigma based on EXO-20-014
float Jpsi_width = 36e-3; // GeV 
float Jpsi_mass_min = Jpsi_mass - 5*Jpsi_width;
float Jpsi_mass_max = Jpsi_mass + 5*Jpsi_width;
float rho_omega_mass = 780e-3; // GeV
float rho_omega_width = 11e-3; // GeV
float rho_omega_mass_min = rho_omega_mass - 5*rho_omega_width;
float rho_omega_mass_max = rho_omega_mass + 5*rho_omega_width;
float dlxy_max = 0.1; // mm
float dlxyz_max = 0.1; // mm
float dlxy_ratio_max = 0.1;
float dlxyz_ratio_max = 0.1;
float dlxy_ratio_v2_max = 0.1;
float dlxyz_ratio_v2_max = 0.1;

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
    "os_muon",
    // "ss_muon",
    "os_dimuon",
    // "ss_dimuon",
    // "os_first_mother",
    // "ss_first_mother",
  };

  vector<string> hist_names = {
    "", // this is without any selection
  
    "sel_pt-min10GeV_",
    "sel_pt-min8GeV_",
    "sel_pt-min5GeV_",

    "sel_mass-Jpsi_",
    "sel_mass-rho_omega_",
    "sel_mass-max20GeV_",

    "sel_dlxy-max0p1mm_",
    "sel_dlxyz-max0p1mm_",
    "sel_dlxy_ratio-max0p1_",
    "sel_dlxyz_ratio-max0p1_",
    "sel_dlxy_ratio_v2-max0p1_",
    "sel_dlxyz_ratio_v2-max0p1_",

    "sel_dR-max0p05_",
    "sel_dR-max0p1_",
    "sel_dR-max0p2_",

    "final_selection_pt-min10GeV_mass-cuts_",
    "final_selection_pt-min10GeV_mass-cuts_dR-max0p1_",
    "final_selection_pt-min10GeV_mass-cuts_dR-max0p2_",
    "final_selection_pt-min10GeV_mass-cuts_dR-max0p05_",
    "final_selection_pt-min10GeV_mass-cuts_dlxy-max0p1mm_",
    "final_selection_pt-min10GeV_mass-cuts_dlxyz-max0p1mm_",
    "final_selection_pt-min10GeV_mass-cuts_dlxy_ratio-max0p1_",
    "final_selection_pt-min10GeV_mass-cuts_dlxyz_ratio-max0p1_",
    "final_selection_pt-min10GeV_mass-cuts_dlxy_ratio_v2-max0p1_",
    "final_selection_pt-min10GeV_mass-cuts_dlxyz_ratio_v2-max0p1_",

    "final_selection_pt-min10GeV_dR-max0p1_",
    "final_selection_pt-min10GeV_dR-max0p2_",
    "final_selection_pt-min10GeV_dR-max0p05_",
    "final_selection_pt-min10GeV_dlxy-max0p1mm_",
    "final_selection_pt-min10GeV_dlxyz-max0p1mm_",
    "final_selection_pt-min10GeV_dlxy_ratio-max0p1_",
    "final_selection_pt-min10GeV_dlxyz_ratio-max0p1_",
    "final_selection_pt-min10GeV_dlxy_ratio_v2-max0p1_",
    "final_selection_pt-min10GeV_dlxyz_ratio_v2-max0p1_",
    "final_selection_pt-min10GeV_dlxy_ratio_v2-max0p1_",
    "final_selection_pt-min10GeV_dlxyz_ratio_v2-max0p1_",

    "final_selection_pt-min8GeV_mass-cuts_",
    "final_selection_pt-min8GeV_mass-cuts_dR-max0p1_",
    "final_selection_pt-min8GeV_mass-cuts_dR-max0p2_",
    "final_selection_pt-min8GeV_mass-cuts_dR-max0p05_",
    "final_selection_pt-min8GeV_mass-cuts_dlxy-max0p1mm_",
    "final_selection_pt-min8GeV_mass-cuts_dlxyz-max0p1mm_",
    "final_selection_pt-min8GeV_mass-cuts_dlxy_ratio-max0p1_",
    "final_selection_pt-min8GeV_mass-cuts_dlxyz_ratio-max0p1_",
    "final_selection_pt-min8GeV_mass-cuts_dlxy_ratio_v2-max0p1_",
    "final_selection_pt-min8GeV_mass-cuts_dlxyz_ratio_v2-max0p1_",

    "final_selection_pt-min8GeV_dR-max0p1_",
    "final_selection_pt-min8GeV_dR-max0p2_",
    "final_selection_pt-min8GeV_dR-max0p05_",
    "final_selection_pt-min8GeV_dlxy-max0p1mm_",
    "final_selection_pt-min8GeV_dlxyz-max0p1mm_",
    "final_selection_pt-min8GeV_dlxy_ratio-max0p1_",
    "final_selection_pt-min8GeV_dlxyz_ratio-max0p1_",
    "final_selection_pt-min8GeV_dlxy_ratio_v2-max0p1_",
    "final_selection_pt-min8GeV_dlxyz_ratio_v2-max0p1_",

    "final_selection_pt-min5GeV_mass-cuts_",
    "final_selection_pt-min5GeV_mass-cuts_dR-max0p1_",
    "final_selection_pt-min5GeV_mass-cuts_dR-max0p2_",
    "final_selection_pt-min5GeV_mass-cuts_dR-max0p05_",
    "final_selection_pt-min5GeV_mass-cuts_dlxy-max0p1mm_",
    "final_selection_pt-min5GeV_mass-cuts_dlxyz-max0p1mm_",
    "final_selection_pt-min5GeV_mass-cuts_dlxy_ratio-max0p1_",
    "final_selection_pt-min5GeV_mass-cuts_dlxyz_ratio-max0p1_",
    "final_selection_pt-min5GeV_mass-cuts_dlxy_ratio_v2-max0p1_",
    "final_selection_pt-min5GeV_mass-cuts_dlxyz_ratio_v2-max0p1_",

    "final_selection_pt-min5GeV_dR-max0p1_",
    "final_selection_pt-min5GeV_dR-max0p2_",
    "final_selection_pt-min5GeV_dR-max0p05_",
    "final_selection_pt-min5GeV_dlxy-max0p1mm_",
    "final_selection_pt-min5GeV_dlxyz-max0p1mm_",
    "final_selection_pt-min5GeV_dlxy_ratio-max0p1_",
    "final_selection_pt-min5GeV_dlxyz_ratio-max0p1_",
    "final_selection_pt-min5GeV_dlxy_ratio_v2-max0p1_",
    "final_selection_pt-min5GeV_dlxyz_ratio_v2-max0p1_",

    "final_selection_mass-cuts_",
    "final_selection_mass-cuts_dR-max0p1_",
    "final_selection_mass-cuts_dR-max0p2_",
    "final_selection_mass-cuts_dR-max0p05_",
    "final_selection_mass-cuts_dlxy-max0p1mm_",
    "final_selection_mass-cuts_dlxyz-max0p1mm_",
    "final_selection_mass-cuts_dlxy_ratio-max0p1_",
    "final_selection_mass-cuts_dlxyz_ratio-max0p1_",
    "final_selection_mass-cuts_dlxy_ratio_v2-max0p1_",
    "final_selection_mass-cuts_dlxyz_ratio_v2-max0p1_",
  };

  vector<string> single_muon_names = {
    "single_muon",
    // "single_muon_first_mother",
    "sel_pt-10GeV_single_muon",
    // "sel_pt-10GeV_single_muon_first_mother",
  };
  
  map<string, HistogramSet*> histSets;
  for(string hist : hist_names){
    for(string particle : particle_names){
      string name = hist + particle;
      histSets[name] = new HistogramSet(name);
    }
  }
  for(string name : single_muon_names){histSets[name] = new HistogramSet(name);}
  
  auto fill_single_muon_hists = [&](const Particle* particle, const Event *event){
    // TODO: handle properly multiple mothers case (?)
    auto mother = event->particles[particle->mothers[0]];
    
    histSets["single_muon"]->fill(particle);
    // histSets["single_muon_first_mother"]->fill(mother);

    if(particle->four_vector.Pt() > 10){
      histSets["sel_pt-10GeV_single_muon"]->fill(particle);
      // histSets["sel_pt-10GeV_single_muon_first_mother"]->fill(mother);
    }
  };

  auto fill_deltaR_deltal_selections = [&](const Particle* particle_1, const Particle* particle_2, string sign, string prefix){
    
    float delta_lxy = sqrt(pow(particle_1->x - particle_2->x, 2) + pow(particle_1->y - particle_2->y, 2));
    float delta_lxyz = sqrt(pow(particle_1->x - particle_2->x, 2) + pow(particle_1->y - particle_2->y, 2) + pow(particle_1->z - particle_2->z, 2));
    float delta_R = particle_1->four_vector.DeltaR(particle_2->four_vector);
    float lxy_1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2));
    float lxy_2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2));
    float lxyz_1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2) + pow(particle_1->z, 2));
    float lxyz_2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2) + pow(particle_2->z, 2));
    // (lxy1 - lxy2) / (lxy1 + lxy2)
    float delta_lxy_ratio = abs(lxy_1-lxy_2)/(lxy_1+lxy_2);
    float delta_lxyz_ratio = abs(lxyz_1-lxyz_2)/(lxyz_1+lxyz_2);
    // sqrt((x1-x2)^2 +(y1-y2)^2) / sqrt((x1+x2)^2 + (y1+y2)^2)
    float delta_lxy_ratio_v2 = sqrt(pow(particle_1->x - particle_2->x, 2) + pow(particle_1->y - particle_2->y, 2))/sqrt(pow(particle_1->x + particle_2->x, 2) + pow(particle_1->y + particle_2->y, 2));
    float delta_lxyz_ratio_v2 = sqrt(pow(particle_1->x - particle_2->x, 2) + pow(particle_1->y - particle_2->y, 2) + pow(particle_1->z - particle_2->z, 2))/sqrt(pow(particle_1->x + particle_2->x, 2) + pow(particle_1->y + particle_2->y, 2) + pow(particle_1->z + particle_2->z, 2));

    if(delta_lxy <= dlxy_max){
      histSets[prefix + "_dlxy-max0p1mm_"+sign+"_muon"]->fill(particle_1);
      histSets[prefix + "_dlxy-max0p1mm_"+sign+"_muon"]->fill(particle_2);
      histSets[prefix + "_dlxy-max0p1mm_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets[prefix + "_dlxy-max0p1mm_"+sign+"_first_mother"]->fill(mother);
    }
    if(delta_lxyz <= dlxyz_max){
      histSets[prefix + "_dlxyz-max0p1mm_"+sign+"_muon"]->fill(particle_1);
      histSets[prefix + "_dlxyz-max0p1mm_"+sign+"_muon"]->fill(particle_2);
      histSets[prefix + "_dlxyz-max0p1mm_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets[prefix + "_dlxyz-max0p1mm_"+sign+"_first_mother"]->fill(mother);
    }
    if(delta_lxy_ratio <= dlxy_ratio_max){
      histSets[prefix + "_dlxy_ratio-max0p1_"+sign+"_muon"]->fill(particle_1);
      histSets[prefix + "_dlxy_ratio-max0p1_"+sign+"_muon"]->fill(particle_2);
      histSets[prefix + "_dlxy_ratio-max0p1_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets[prefix + "_dlxy_ratio-max0p1_"+sign+"_first_mother"]->fill(mother);
    }
    if(delta_lxyz_ratio <= dlxyz_ratio_max){
      histSets[prefix + "_dlxyz_ratio-max0p1_"+sign+"_muon"]->fill(particle_1);
      histSets[prefix + "_dlxyz_ratio-max0p1_"+sign+"_muon"]->fill(particle_2);
      histSets[prefix + "_dlxyz_ratio-max0p1_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets[prefix + "_dlxyz_ratio-max0p1_"+sign+"_first_mother"]->fill(mother);
    }
    if(delta_lxy_ratio_v2 <= dlxy_ratio_v2_max){
      histSets[prefix + "_dlxy_ratio_v2-max0p1_"+sign+"_muon"]->fill(particle_1);
      histSets[prefix + "_dlxy_ratio_v2-max0p1_"+sign+"_muon"]->fill(particle_2);
      histSets[prefix + "_dlxy_ratio_v2-max0p1_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets[prefix + "_dlxy_ratio_v2-max0p1_"+sign+"_first_mother"]->fill(mother);
    }
    if(delta_lxyz_ratio_v2 <= dlxyz_ratio_v2_max){
      histSets[prefix + "_dlxyz_ratio_v2-max0p1_"+sign+"_muon"]->fill(particle_1);
      histSets[prefix + "_dlxyz_ratio_v2-max0p1_"+sign+"_muon"]->fill(particle_2);
      histSets[prefix + "_dlxyz_ratio_v2-max0p1_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets[prefix + "_dlxyz_ratio_v2-max0p1_"+sign+"_first_mother"]->fill(mother);
    }
    if(delta_R <= 0.05){
      histSets[prefix + "_dR-max0p05_"+sign+"_muon"]->fill(particle_1);
      histSets[prefix + "_dR-max0p05_"+sign+"_muon"]->fill(particle_2);
      histSets[prefix + "_dR-max0p05_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets[prefix + "_dR-max0p05_"+sign+"_first_mother"]->fill(mother);
    }
    if(delta_R <= 0.1){
      histSets[prefix + "_dR-max0p1_"+sign+"_muon"]->fill(particle_1);
      histSets[prefix + "_dR-max0p1_"+sign+"_muon"]->fill(particle_2);
      histSets[prefix + "_dR-max0p1_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets[prefix + "_dR-max0p1_"+sign+"_first_mother"]->fill(mother);
    }
    if(delta_R <= 0.2){
      histSets[prefix + "_dR-max0p2_"+sign+"_muon"]->fill(particle_1);
      histSets[prefix + "_dR-max0p2_"+sign+"_muon"]->fill(particle_2);
      histSets[prefix + "_dR-max0p2_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets[prefix + "_dR-max0p2_"+sign+"_first_mother"]->fill(mother);
    }
  };
  
  auto fill_pair_hists = [&](const Particle* particle_1, const Particle* particle_2, const Event *event){
    // TODO: handle the full chain of mother (and multiple mothers) correctly
    auto mother = event->particles[particle_1->mothers[0]];
    
    histSets["os_muon"]->fill(particle_1);
    histSets["os_muon"]->fill(particle_2);
    histSets["os_dimuon"]->fill(particle_1, particle_2);
    // histSets["os_first_mother"]->fill(mother);
    
    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;

    // Independent selections:
    if(particle_1->four_vector.Pt() > 5 && particle_2->four_vector.Pt() > 5){
      histSets["sel_pt-min5GeV_os_muon"]->fill(particle_1);
      histSets["sel_pt-min5GeV_os_muon"]->fill(particle_2);
      histSets["sel_pt-min5GeV_os_dimuon"]->fill(particle_1, particle_2);
      // histSets["sel_pt-min5GeV_os_first_mother"]->fill(mother);
    }
    if(particle_1->four_vector.Pt() > 8 && particle_2->four_vector.Pt() > 8){
      histSets["sel_pt-min8GeV_os_muon"]->fill(particle_1);
      histSets["sel_pt-min8GeV_os_muon"]->fill(particle_2);
      histSets["sel_pt-min8GeV_os_dimuon"]->fill(particle_1, particle_2);
      // histSets["sel_pt-8GeV_os_first_mother"]->fill(mother);
    }
    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){
      histSets["sel_pt-min10GeV_os_muon"]->fill(particle_1);
      histSets["sel_pt-min10GeV_os_muon"]->fill(particle_2);
      histSets["sel_pt-min10GeV_os_dimuon"]->fill(particle_1, particle_2);
      // histSets["sel_pt-10GeV_os_first_mother"]->fill(mother);
    }
    if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
        histSets["sel_mass-Jpsi_os_muon"]->fill(particle_1);
        histSets["sel_mass-Jpsi_os_muon"]->fill(particle_2);
        histSets["sel_mass-Jpsi_os_dimuon"]->fill(particle_1, particle_2);
        // histSets["sel_mass-Jpsi_os_first_mother"]->fill(mother);
    }
    if((diparticle.M() < (rho_omega_mass_min)) || (diparticle.M() > (rho_omega_mass_max))){
        histSets["sel_mass-rho_omega_os_muon"]->fill(particle_1);
        histSets["sel_mass-rho_omega_os_muon"]->fill(particle_2);
        histSets["sel_mass-rho_omega_os_dimuon"]->fill(particle_1, particle_2);
        // histSets["sel_mass-rho_omega_os_first_mother"]->fill(mother);
    }
    if((diparticle.M() < (20)) || (diparticle.M() > (20))){
        histSets["sel_mass-max20GeV_os_muon"]->fill(particle_1);
        histSets["sel_mass-max20GeV_os_muon"]->fill(particle_2);
        histSets["sel_mass-max20GeV_os_dimuon"]->fill(particle_1, particle_2);
        // histSets["sel_mass-20GeV_os_first_mother"]->fill(mother);
    }

    fill_deltaR_deltal_selections(particle_1, particle_2, "os", "sel");
  };

  auto fill_non_pair_hists = [&](const Particle* particle_1, const Particle* particle_2, const Event *event, string sign){
    if(!particle_1 || !particle_2) return;
    
    auto mother_1 = event->particles[particle_1->mothers[0]];
    auto mother_2 = event->particles[particle_2->mothers[0]];
      
    histSets[sign+"_muon"]->fill(particle_1);
    histSets[sign+"_muon"]->fill(particle_2);
    histSets[sign+"_dimuon"]->fill(particle_1, particle_2);
    // histSets[sign+"_first_mother"]->fill(mother_1);
    // histSets[sign+"_first_mother"]->fill(mother_2);
    
    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;
    float delta_lxy = sqrt(pow(particle_1->x - particle_2->x, 2) + pow(particle_1->y - particle_2->y, 2));
    float delta_lxyz = sqrt(pow(particle_1->x - particle_2->x, 2) + pow(particle_1->y - particle_2->y, 2) + pow(particle_1->z - particle_2->z, 2));
    float delta_R = particle_1->four_vector.DeltaR(particle_2->four_vector);
    float lxy_1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2));
    float lxy_2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2));
    float delta_lxy_ratio = abs(lxy_1-lxy_2)/(lxy_1+lxy_2);

    // Independent selections:
    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){
      histSets["sel_pt-min5GeV_"+sign+"_muon"]->fill(particle_1);
      histSets["sel_pt-min5GeV_"+sign+"_muon"]->fill(particle_2);
      histSets["sel_pt-min5GeV_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets["sel_pt-5GeV_"+sign+"_first_mother"]->fill(mother_1);
      // histSets["sel_pt-5GeV_"+sign+"_first_mother"]->fill(mother_2);
    }
    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){
      histSets["sel_pt-min8GeV_"+sign+"_muon"]->fill(particle_1);
      histSets["sel_pt-min8GeV_"+sign+"_muon"]->fill(particle_2);
      histSets["sel_pt-min8GeV_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets["sel_pt-8GeV_"+sign+"_first_mother"]->fill(mother_1);
      // histSets["sel_pt-8GeV_"+sign+"_first_mother"]->fill(mother_2);
    }
    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){
      histSets["sel_pt-min10GeV_"+sign+"_muon"]->fill(particle_1);
      histSets["sel_pt-min10GeV_"+sign+"_muon"]->fill(particle_2);
      histSets["sel_pt-min10GeV_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets["sel_pt-10GeV_"+sign+"_first_mother"]->fill(mother_1);
      // histSets["sel_pt-10GeV_"+sign+"_first_mother"]->fill(mother_2);
    }
    if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
      histSets["sel_mass-Jpsi_"+sign+"_muon"]->fill(particle_1);
      histSets["sel_mass-Jpsi_"+sign+"_muon"]->fill(particle_2);
      histSets["sel_mass-Jpsi_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets["sel_mass-Jpsi_"+sign+"_first_mother"]->fill(mother_1);
      // histSets["sel_mass-Jpsi_"+sign+"_first_mother"]->fill(mother_2);
    }
    if((diparticle.M() < (rho_omega_mass_min)) || (diparticle.M() > (rho_omega_mass_max))){
      histSets["sel_mass-rho_omega_"+sign+"_muon"]->fill(particle_1);
      histSets["sel_mass-rho_omega_"+sign+"_muon"]->fill(particle_2);
      histSets["sel_mass-rho_omega_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets["sel_mass-rho_omega_"+sign+"_first_mother"]->fill(mother_1);
      // histSets["sel_mass-rho_omega_"+sign+"_first_mother"]->fill(mother_2);
    }
    if((diparticle.M() < (20)) || (diparticle.M() > (20))){
      histSets["sel_mass-max20GeV_"+sign+"_muon"]->fill(particle_1);
      histSets["sel_mass-max20GeV_"+sign+"_muon"]->fill(particle_2);
      histSets["sel_mass-max20GeV_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      // histSets["sel_mass-20GeV_"+sign+"_first_mother"]->fill(mother_1);
      // histSets["sel_mass-20GeV_"+sign+"_first_mother"]->fill(mother_2);
    }
    fill_deltaR_deltal_selections(particle_1, particle_2, sign, "sel");
  };

  auto fill_final_selection_pair_hists = [&](const Particle* particle_1, const Particle* particle_2, const Event *event){

    auto mother = event->particles[particle_1->mothers[0]];
    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;

    // With muon pT > 10 GeV
    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){
      // With dimuon mass cuts
      if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
        if((diparticle.M() < (rho_omega_mass_min)) || (diparticle.M() > (rho_omega_mass_max))){
          if(diparticle.M() < 20){
            histSets["final_selection_pt-min10GeV_mass-cuts_os_muon"]->fill(particle_1);
            histSets["final_selection_pt-min10GeV_mass-cuts_os_muon"]->fill(particle_2);
            histSets["final_selection_pt-min10GeV_mass-cuts_os_dimuon"]->fill(particle_1, particle_2);
            // histSets["final_selection_pt-min10GeV_mass-cuts_os_first_mother"]->fill(mother);

            fill_deltaR_deltal_selections(particle_1, particle_2, "os", "final_selection_pt-min10GeV_mass-cuts");
          }
        }
      }
      // Without dimuon mass cuts
      fill_deltaR_deltal_selections(particle_1, particle_2, "os", "final_selection_pt-min10GeV");
    }
    // With muon pT > 8 GeV
    if(particle_1->four_vector.Pt() > 8 && particle_2->four_vector.Pt() > 8){
      // With dimuon mass cuts
      if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
        if((diparticle.M() < (rho_omega_mass_min)) || (diparticle.M() > (rho_omega_mass_max))){
          if(diparticle.M() < 20){
            histSets["final_selection_pt-min8GeV_mass-cuts_os_muon"]->fill(particle_1);
            histSets["final_selection_pt-min8GeV_mass-cuts_os_muon"]->fill(particle_2);
            histSets["final_selection_pt-min8GeV_mass-cuts_os_dimuon"]->fill(particle_1, particle_2);
            // histSets["final_selection_pt-min8GeV_mass-cuts_os_first_mother"]->fill(mother);

            fill_deltaR_deltal_selections(particle_1, particle_2, "os", "final_selection_pt-min8GeV_mass-cuts");
          }
        }
      }
      // Without dimuon mass cuts
      fill_deltaR_deltal_selections(particle_1, particle_2, "os", "final_selection_pt-min8GeV");
    }
    // With muon pT > 5 GeV
    if(particle_1->four_vector.Pt() > 5 && particle_2->four_vector.Pt() > 5){
      // With dimuon mass cuts
      if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
        if((diparticle.M() < (rho_omega_mass_min)) || (diparticle.M() > (rho_omega_mass_max))){
          if(diparticle.M() < 20){
            histSets["final_selection_pt-min5GeV_mass-cuts_os_muon"]->fill(particle_1);
            histSets["final_selection_pt-min5GeV_mass-cuts_os_muon"]->fill(particle_2);
            histSets["final_selection_pt-min5GeV_mass-cuts_os_dimuon"]->fill(particle_1, particle_2);
            // histSets["final_selection_pt-min5GeV_mass-cuts_os_first_mother"]->fill(mother);

            fill_deltaR_deltal_selections(particle_1, particle_2, "os", "final_selection_pt-min5GeV_mass-cuts");
          }
        }
      }
      // Without dimuon mass cuts
      fill_deltaR_deltal_selections(particle_1, particle_2, "os", "final_selection_pt-min5GeV");
    }
    // Without muon pT cut
    if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
      if((diparticle.M() < (rho_omega_mass_min)) || (diparticle.M() > (rho_omega_mass_max))){
        if(diparticle.M() < 20){
          histSets["final_selection_mass-cuts_os_muon"]->fill(particle_1);
          histSets["final_selection_mass-cuts_os_muon"]->fill(particle_2);
          histSets["final_selection_mass-cuts_os_dimuon"]->fill(particle_1, particle_2);
          // histSets["final_selection_mass-cuts_os_first_mother"]->fill(mother);

          fill_deltaR_deltal_selections(particle_1, particle_2, "os", "final_selection_mass-cuts");
        }
      }
    }
  };
  
  auto fill_final_selection_non_pair_hists = [&](const Particle* particle_1, const Particle* particle_2, const Event *event, string sign){
    if(!particle_1 || !particle_2) return;
    
    auto mother_1 = event->particles[particle_1->mothers[0]];
    auto mother_2 = event->particles[particle_2->mothers[0]];
    
    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;
    float delta_lxy = sqrt(pow(particle_1->x - particle_2->x, 2) + pow(particle_1->y - particle_2->y, 2));
    float delta_lxyz = sqrt(pow(particle_1->x - particle_2->x, 2) + pow(particle_1->y - particle_2->y, 2) + pow(particle_1->z - particle_2->z, 2));
    float delta_R = particle_1->four_vector.DeltaR(particle_2->four_vector);
    float lxy_1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2));
    float lxy_2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2));
    float delta_lxy_ratio = abs(lxy_1-lxy_2)/(lxy_1+lxy_2);
    
    // With muon pT > 10 GeV
    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){     
      // With dimuon mass cuts
      if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
        if((diparticle.M() < (rho_omega_mass_min)) || (diparticle.M() > (rho_omega_mass_max))){
          if(diparticle.M() < 20){
            histSets["final_selection_pt-min10GeV_mass-cuts_"+sign+"_muon"]->fill(particle_1);
            histSets["final_selection_pt-min10GeV_mass-cuts_"+sign+"_muon"]->fill(particle_2);
            histSets["final_selection_pt-min10GeV_mass-cuts_"+sign+"_dimuon"]->fill(particle_1, particle_2);
            // histSets["final_selection_pt-min10GeV_mass-cuts_"+sign+"_first_mother"]->fill(mother_1);
            // histSets["final_selection_pt-min10GeV_mass-cuts_"+sign+"_first_mother"]->fill(mother_2);

            fill_deltaR_deltal_selections(particle_1, particle_2, sign, "final_selection_pt-min10GeV_mass-cuts");
          }
        }
      }
      // Without dimuon mass cuts
      fill_deltaR_deltal_selections(particle_1, particle_2, sign, "final_selection_pt-min10GeV");
    }
    // With muon pT > 8 GeV
    if(particle_1->four_vector.Pt() > 8 && particle_2->four_vector.Pt() > 8){     
      // With dimuon mass cuts
      if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
        if((diparticle.M() < (rho_omega_mass_min)) || (diparticle.M() > (rho_omega_mass_max))){
          if(diparticle.M() < 20){
            histSets["final_selection_pt-min8GeV_mass-cuts_"+sign+"_muon"]->fill(particle_1);
            histSets["final_selection_pt-min8GeV_mass-cuts_"+sign+"_muon"]->fill(particle_2);
            histSets["final_selection_pt-min8GeV_mass-cuts_"+sign+"_dimuon"]->fill(particle_1, particle_2);
            // histSets["final_selection_pt-min8GeV_mass-cuts_"+sign+"_first_mother"]->fill(mother_1);
            // histSets["final_selection_pt-min8GeV_mass-cuts_"+sign+"_first_mother"]->fill(mother_2);

            fill_deltaR_deltal_selections(particle_1, particle_2, sign, "final_selection_pt-min8GeV_mass-cuts");
          }
        }
      }
      // Without dimuon mass cuts
      fill_deltaR_deltal_selections(particle_1, particle_2, sign, "final_selection_pt-min8GeV");
    }
    // With muon pT > 5 GeV
    if(particle_1->four_vector.Pt() > 5 && particle_2->four_vector.Pt() > 5){     
      // With dimuon mass cuts
      if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
        if((diparticle.M() < (rho_omega_mass_min)) || (diparticle.M() > (rho_omega_mass_max))){
          if(diparticle.M() < 20){
            histSets["final_selection_pt-min5GeV_mass-cuts_"+sign+"_muon"]->fill(particle_1);
            histSets["final_selection_pt-min5GeV_mass-cuts_"+sign+"_muon"]->fill(particle_2);
            histSets["final_selection_pt-min5GeV_mass-cuts_"+sign+"_dimuon"]->fill(particle_1, particle_2);
            // histSets["final_selection_pt-min10GeV_mass-cuts_"+sign+"_first_mother"]->fill(mother_1);
            // histSets["final_selection_pt-min10GeV_mass-cuts_"+sign+"_first_mother"]->fill(mother_2);

            fill_deltaR_deltal_selections(particle_1, particle_2, sign, "final_selection_pt-min5GeV_mass-cuts");
          }
        }
      }
      // Without dimuon mass cuts
      fill_deltaR_deltal_selections(particle_1, particle_2, sign, "final_selection_pt-min5GeV");
    }
    // Without muon pT cut
    if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
      if((diparticle.M() < (rho_omega_mass_min)) || (diparticle.M() > (rho_omega_mass_max))){
        if(diparticle.M() < 20){
          histSets["final_selection_mass-cuts_"+sign+"_muon"]->fill(particle_1);
          histSets["final_selection_mass-cuts_"+sign+"_muon"]->fill(particle_2);
          histSets["final_selection_mass-cuts_"+sign+"_dimuon"]->fill(particle_1, particle_2);
          // histSets["final_selection_mass-cuts_"+sign+"_first_mother"]->fill(mother_1);
          // histSets["final_selection_mass-cuts_"+sign+"_first_mother"]->fill(mother_2);

          fill_deltaR_deltal_selections(particle_1, particle_2, sign, "final_selection_mass-cuts");
        }
      }
    }
  };

  for(auto event : events){
    
    if(!event->has_ttbar_pair()) continue;
    int preselection_code = event->passes_preselection();
    
    if(preselection_code == 0){
      continue;
    }
    else if(preselection_code == 1){ // single muon tree
      auto muon = event->get_single_muon();
      fill_single_muon_hists(muon, event);
    }
    else if(preselection_code == 2){ // pair category
      auto muons = event->get_muon_pair();
      
      for(auto muon_pair : muons){
        auto muon_1 = get<0>(muon_pair);
        auto muon_2 = get<1>(muon_pair);
        fill_pair_hists(muon_1, muon_2, event);
        fill_final_selection_pair_hists(muon_1, muon_2, event);
      }
    }
    else if(preselection_code == 3){ // non-pair category
      auto [opposite_sign_muon_1, opposite_sign_muon_2] = event->get_smallest_deltaR_opposite_sign_muon_non_pair();
      auto [same_sign_muon_1, same_sign_muon_2] = event->get_smallest_deltaR_same_sign_muon_non_pair();
      
      fill_non_pair_hists(opposite_sign_muon_1, opposite_sign_muon_2, event, "os");
      // fill_non_pair_hists(same_sign_muon_1, same_sign_muon_2, event, "ss");
      fill_final_selection_non_pair_hists(opposite_sign_muon_1, opposite_sign_muon_2, event, "os");
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
