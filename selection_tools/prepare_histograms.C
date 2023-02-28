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
float Jpsi_mass = 3096.900e-3; // GeV
float Jpsi_width = 92.6e-6; // GeV
float Jpsi_mass_min = Jpsi_mass - 5*Jpsi_width;
float Jpsi_mass_max = Jpsi_mass + 5*Jpsi_width;

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
    cout<<"Usage: ./apply_selections input_path output_path"<<endl;
    exit(0);
  }
  
  string input_path = argv[1];
  string output_path = argv[2];
  
  auto input_tree = get_input_tree(input_path);
  auto output_file = new TFile(output_path.c_str(), "recreate");
  
// load events
  auto event_reader = EventReader(max_events, n_daughters);
  auto events = event_reader.read_events(input_tree);
  
  vector<string> hist_names = {
    "single_muon",
    "single_muon_first_mother",
    "os_muon",
    "ss_muon",
    "os_dimuon",
    "ss_dimuon",
    "os_first_mother",
    "ss_first_mother",
    "sel_pt-10GeV_single_muon",
    "sel_pt-10GeV_single_muon_first_mother",
    "sel_pt-10GeV_os_muon",
    "sel_pt-10GeV_ss_muon",
    "sel_pt-10GeV_os_dimuon",
    "sel_pt-10GeV_ss_dimuon",
    "sel_pt-10GeV_os_first_mother",
    "sel_pt-10GeV_ss_first_mother",
    "sel_pt-10GeV_mass-Jpsi_os_muon",
    "sel_pt-10GeV_mass-Jpsi_ss_muon",
    "sel_pt-10GeV_mass-Jpsi_os_dimuon",
    "sel_pt-10GeV_mass-Jpsi_ss_dimuon",
    "sel_pt-10GeV_mass-Jpsi_os_first_mother",
    "sel_pt-10GeV_mass-Jpsi_ss_first_mother",

    "sel_pt-10GeV_lxy-2p4cm_single_muon",
    "sel_pt-10GeV_lxy-2p4cm_single_muon_first_mother",
    "sel_pt-10GeV_lxy-2p4cm_os_muon",
    "sel_pt-10GeV_lxy-2p4cm_ss_muon",
    "sel_pt-10GeV_lxy-2p4cm_os_first_mother",
    "sel_pt-10GeV_lxy-2p4cm_ss_first_mother",
    "sel_pt-10GeV_mass-Jpsi_lxy-2p4cm_os_muon",
    "sel_pt-10GeV_mass-Jpsi_lxy-2p4cm_ss_muon",
    "sel_pt-10GeV_mass-Jpsi_lxy-2p4cm_os_first_mother",
    "sel_pt-10GeV_mass-Jpsi_lxy-2p4cm_ss_first_mother",

    "sel_pt-10GeV_lxy-3p1cm_single_muon",
    "sel_pt-10GeV_lxy-3p1cm_single_muon_first_mother",
    "sel_pt-10GeV_lxy-3p1cm_os_muon",
    "sel_pt-10GeV_lxy-3p1cm_ss_muon",
    "sel_pt-10GeV_lxy-3p1cm_os_first_mother",
    "sel_pt-10GeV_lxy-3p1cm_ss_first_mother",
    "sel_pt-10GeV_mass-Jpsi_lxy-3p1cm_os_muon",
    "sel_pt-10GeV_mass-Jpsi_lxy-3p1cm_ss_muon",
    "sel_pt-10GeV_mass-Jpsi_lxy-3p1cm_os_first_mother",
    "sel_pt-10GeV_mass-Jpsi_lxy-3p1cm_ss_first_mother",
    
    "sel_pt-10GeV_lxy-7p0cm_single_muon",
    "sel_pt-10GeV_lxy-7p0cm_single_muon_first_mother",
    "sel_pt-10GeV_lxy-7p0cm_os_muon",
    "sel_pt-10GeV_lxy-7p0cm_ss_muon",
    "sel_pt-10GeV_lxy-7p0cm_os_first_mother",
    "sel_pt-10GeV_lxy-7p0cm_ss_first_mother",
    "sel_pt-10GeV_mass-Jpsi_lxy-7p0cm_os_muon",
    "sel_pt-10GeV_mass-Jpsi_lxy-7p0cm_ss_muon",
    "sel_pt-10GeV_mass-Jpsi_lxy-7p0cm_os_first_mother",
    "sel_pt-10GeV_mass-Jpsi_lxy-7p0cm_ss_first_mother",

    "sel_pt-10GeV_lxy-11p0cm_single_muon",
    "sel_pt-10GeV_lxy-11p0cm_single_muon_first_mother",
    "sel_pt-10GeV_lxy-11p0cm_os_muon",
    "sel_pt-10GeV_lxy-11p0cm_ss_muon",
    "sel_pt-10GeV_lxy-11p0cm_os_first_mother",
    "sel_pt-10GeV_lxy-11p0cm_ss_first_mother",
    "sel_pt-10GeV_mass-Jpsi_lxy-11p0cm_os_muon",
    "sel_pt-10GeV_mass-Jpsi_lxy-11p0cm_ss_muon",
    "sel_pt-10GeV_mass-Jpsi_lxy-11p0cm_os_first_mother",
    "sel_pt-10GeV_mass-Jpsi_lxy-11p0cm_ss_first_mother",

    "final_selection_muon",
    "final_selection_dimuon",
    "final_selection_first_mother",
    "final_selection_mass-Jpsi_muon",
    "final_selection_mass-Jpsi_dimuon",
    "final_selection_mass-Jpsi_first_mother",
    "final_selection_mass-max20GeV_muon",
    "final_selection_mass-max20GeV_dimuon",
    "final_selection_mass-max20GeV_first_mother",
  };

  vector<double> lxy_regions = {2.4, 3.1, 7.0, 11.0};
  vector<string> lxy_str = {"2p4", "3p1", "7p0", "11p0"};
  
  map<string, HistogramSet*> histSets;
  for(string name : hist_names) histSets[name] = new HistogramSet(name);
  
  auto fill_single_muon_hists = [&](const Particle* particle, const Event *event){
    // TODO: handle properly multiple mothers case (?)
    auto mother = event->particles[particle->mothers[0]];
    
    histSets["single_muon"]->fill(particle);
    histSets["single_muon_first_mother"]->fill(mother);

    if(particle->four_vector.Pt() > 10){
      histSets["sel_pt-10GeV_single_muon"]->fill(particle);
      histSets["sel_pt-10GeV_single_muon_first_mother"]->fill(mother);
      double lxy = sqrt(pow(particle->x, 2) + pow(particle->y, 2));
      for(int i=0; i<lxy_regions.size(); i++){
        if(lxy<=lxy_regions[i]){
          histSets["sel_pt-10GeV_lxy-"+lxy_str[i]+"cm_single_muon"]->fill(particle);
          histSets["sel_pt-10GeV_lxy-"+lxy_str[i]+"cm_single_muon_first_mother"]->fill(mother);
          break;
        }
      }
    }
  };
  
  auto fill_pair_hists = [&](const Particle* particle_1, const Particle* particle_2, const Event *event){
    // TODO: handle the full chain of mother (and multiple mothers) correctly
    auto mother = event->particles[particle_1->mothers[0]];
    
    histSets["os_muon"]->fill(particle_1);
    histSets["os_muon"]->fill(particle_2);
    histSets["os_dimuon"]->fill(particle_1, particle_2);
    histSets["os_first_mother"]->fill(mother);
    
    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;
    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){
      histSets["sel_pt-10GeV_os_muon"]->fill(particle_1);
      histSets["sel_pt-10GeV_os_muon"]->fill(particle_2);
      histSets["sel_pt-10GeV_os_dimuon"]->fill(particle_1, particle_2);
      histSets["sel_pt-10GeV_os_first_mother"]->fill(mother);
      double lxy_1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2));
      double lxy_2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2));
      for(int i=0; i<lxy_regions.size(); i++){
        if(lxy_1<=lxy_regions[i]){
          histSets["sel_pt-10GeV_lxy-"+lxy_str[i]+"cm_os_muon"]->fill(particle_1);
          histSets["sel_pt-10GeV_lxy-"+lxy_str[i]+"cm_os_first_mother"]->fill(mother);
          break;
        }
      }    
      for(int i=0; i<lxy_regions.size(); i++){
        if(lxy_2<=lxy_regions[i]){
          histSets["sel_pt-10GeV_lxy-"+lxy_str[i]+"cm_os_muon"]->fill(particle_2);
          // histSets["sel_pt-10GeV_mass-Jpsi_lxy-"+lxy_str[i]+"cm_os_first_mother"]->fill(mother);
          break;
        }
      }
      if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
        histSets["sel_pt-10GeV_mass-Jpsi_os_muon"]->fill(particle_1);
        histSets["sel_pt-10GeV_mass-Jpsi_os_muon"]->fill(particle_2);
        histSets["sel_pt-10GeV_mass-Jpsi_os_dimuon"]->fill(particle_1, particle_2);
        histSets["sel_pt-10GeV_mass-Jpsi_os_first_mother"]->fill(mother);
        for(int i=0; i<lxy_regions.size(); i++){
          if(lxy_1<=lxy_regions[i]){
            histSets["sel_pt-10GeV_mass-Jpsi_lxy-"+lxy_str[i]+"cm_os_muon"]->fill(particle_1);
            histSets["sel_pt-10GeV_mass-Jpsi_lxy-"+lxy_str[i]+"cm_os_first_mother"]->fill(mother);
            break;
          }
        }    
        for(int i=0; i<lxy_regions.size(); i++){
          if(lxy_2<=lxy_regions[i]){
            histSets["sel_pt-10GeV_mass-Jpsi_lxy-"+lxy_str[i]+"cm_os_muon"]->fill(particle_2);
            // histSets["sel_pt-10GeV_mass-Jpsi_lxy-"+lxy_str[i]+"cm_os_first_mother"]->fill(mother);
            break;
          }
        }
      }
    }
  };
  
  auto fill_non_pair_hists = [&](const Particle* particle_1, const Particle* particle_2, const Event *event, string sign){
    if(!particle_1 || !particle_2) return;
    
    auto mother_1 = event->particles[particle_1->mothers[0]];
    auto mother_2 = event->particles[particle_2->mothers[0]];
    
    histSets[sign+"_muon"]->fill(particle_1);
    histSets[sign+"_muon"]->fill(particle_2);
    histSets[sign+"_dimuon"]->fill(particle_1, particle_2);
    histSets[sign+"_first_mother"]->fill(mother_1);
    histSets[sign+"_first_mother"]->fill(mother_2);
    
    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;
    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){
      histSets["sel_pt-10GeV_"+sign+"_muon"]->fill(particle_1);
      histSets["sel_pt-10GeV_"+sign+"_muon"]->fill(particle_2);
      histSets["sel_pt-10GeV_"+sign+"_dimuon"]->fill(particle_1, particle_2);
      histSets["sel_pt-10GeV_"+sign+"_first_mother"]->fill(mother_1);
      histSets["sel_pt-10GeV_"+sign+"_first_mother"]->fill(mother_2);
      double lxy_1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2));
      double lxy_2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2));
      for(int i=0; i<lxy_regions.size(); i++){
        if(lxy_1<=lxy_regions[i]){
          histSets["sel_pt-10GeV_lxy-"+lxy_str[i]+"cm_"+sign+"_muon"]->fill(particle_1);
          histSets["sel_pt-10GeV_lxy-"+lxy_str[i]+"cm_"+sign+"_first_mother"]->fill(mother_1);
          break;
        }
      }    
      for(int i=0; i<lxy_regions.size(); i++){
        if(lxy_2<=lxy_regions[i]){
          histSets["sel_pt-10GeV_lxy-"+lxy_str[i]+"cm_"+sign+"_muon"]->fill(particle_2);
          histSets["sel_pt-10GeV_lxy-"+lxy_str[i]+"cm_"+sign+"_first_mother"]->fill(mother_2);
          break;
        }
      }
      if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
        histSets["sel_pt-10GeV_mass-Jpsi_"+sign+"_muon"]->fill(particle_1);
        histSets["sel_pt-10GeV_mass-Jpsi_"+sign+"_muon"]->fill(particle_2);
        histSets["sel_pt-10GeV_mass-Jpsi_"+sign+"_dimuon"]->fill(particle_1, particle_2);
        histSets["sel_pt-10GeV_mass-Jpsi_"+sign+"_first_mother"]->fill(mother_1);
        histSets["sel_pt-10GeV_mass-Jpsi_"+sign+"_first_mother"]->fill(mother_2);
        for(int i=0; i<lxy_regions.size(); i++){
          if(lxy_1<=lxy_regions[i]){
            histSets["sel_pt-10GeV_mass-Jpsi_lxy-"+lxy_str[i]+"cm_"+sign+"_muon"]->fill(particle_1);
            histSets["sel_pt-10GeV_mass-Jpsi_lxy-"+lxy_str[i]+"cm_"+sign+"_first_mother"]->fill(mother_1);
            break;
          }
        }    
        for(int i=0; i<lxy_regions.size(); i++){
          if(lxy_2<=lxy_regions[i]){
            histSets["sel_pt-10GeV_mass-Jpsi_lxy-"+lxy_str[i]+"cm_"+sign+"_muon"]->fill(particle_2);
            histSets["sel_pt-10GeV_mass-Jpsi_lxy-"+lxy_str[i]+"cm_"+sign+"_first_mother"]->fill(mother_2);
            break;
          }
        }
      }
    }
  };

  auto fill_final_selection_pair_hists = [&](const Particle* particle_1, const Particle* particle_2, const Event *event){

    auto mother = event->particles[particle_1->mothers[0]];
    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;

    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){

      float delta_lxy = sqrt(pow(particle_1->x - particle_2->x, 2) + pow(particle_1->y - particle_2->y, 2));

      if(delta_lxy <= 0.1){
        histSets["final_selection_muon"]->fill(particle_1);
        histSets["final_selection_muon"]->fill(particle_2);
        histSets["final_selection_dimuon"]->fill(particle_1, particle_2);
        histSets["final_selection_first_mother"]->fill(mother);
        if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
          histSets["final_selection_mass-Jpsi_muon"]->fill(particle_1);
          histSets["final_selection_mass-Jpsi_muon"]->fill(particle_2);
          histSets["final_selection_mass-Jpsi_dimuon"]->fill(particle_1, particle_2);
          histSets["final_selection_mass-Jpsi_first_mother"]->fill(mother);

          if(diparticle.M() < 20){
            histSets["final_selection_mass-max20GeV_muon"]->fill(particle_1);
            histSets["final_selection_mass-max20GeV_muon"]->fill(particle_2);
            histSets["final_selection_mass-max20GeV_dimuon"]->fill(particle_1, particle_2);
            histSets["final_selection_mass-max20GeV_first_mother"]->fill(mother);
          }
        }
      }
    }
  };
  
  auto fill_final_selection_non_pair_hists = [&](const Particle* particle_1, const Particle* particle_2, const Event *event){
    if(!particle_1 || !particle_2) return;
    
    auto mother_1 = event->particles[particle_1->mothers[0]];
    auto mother_2 = event->particles[particle_2->mothers[0]];
    
    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;

    if(particle_1->four_vector.Pt() > 10 && particle_2->four_vector.Pt() > 10){
      float delta_lxy = sqrt(pow(particle_1->x - particle_2->x, 2) + pow(particle_1->y - particle_2->y, 2));

      if(delta_lxy <= 0.1){
        histSets["final_selection_muon"]->fill(particle_1);
        histSets["final_selection_muon"]->fill(particle_2);
        histSets["final_selection_dimuon"]->fill(particle_1, particle_2);
        histSets["final_selection_first_mother"]->fill(mother_1);
        histSets["final_selection_first_mother"]->fill(mother_2);
        if((diparticle.M() < (Jpsi_mass_min)) || (diparticle.M() > (Jpsi_mass_max))){
          histSets["final_selection_mass-Jpsi_muon"]->fill(particle_1);
          histSets["final_selection_mass-Jpsi_muon"]->fill(particle_2);
          histSets["final_selection_mass-Jpsi_dimuon"]->fill(particle_1, particle_2);
          histSets["final_selection_mass-Jpsi_first_mother"]->fill(mother_1);
          histSets["final_selection_mass-Jpsi_first_mother"]->fill(mother_2);

          if(diparticle.M() < 20){
            histSets["final_selection_mass-max20GeV_muon"]->fill(particle_1);
            histSets["final_selection_mass-max20GeV_muon"]->fill(particle_2);
            histSets["final_selection_mass-max20GeV_dimuon"]->fill(particle_1, particle_2);
            histSets["final_selection_mass-max20GeV_first_mother"]->fill(mother_1);
            histSets["final_selection_mass-max20GeV_first_mother"]->fill(mother_2);
          }
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
      fill_non_pair_hists(same_sign_muon_1, same_sign_muon_2, event, "ss");
      fill_final_selection_non_pair_hists(opposite_sign_muon_1, opposite_sign_muon_2, event);
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
