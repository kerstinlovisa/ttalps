#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#include <TFile.h>
#include <TTree.h>
#include <TH1D.h>

#include "Particle.hpp"
#include "Event.hpp"
#include "EventReader.hpp"

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
  
  map<string, TH1D*> hists = {
    {"muon_pt",  new TH1D("muon_pt", "muon_pt", 1000, 0, 1000)},
    {"muon_pz",  new TH1D("muon_pz", "muon_pz", 1000, -1000, 1000)},
    {"muon_mass",  new TH1D("muon_mass", "muon_mass", 1000, 0, 10)},
    {"muon_eta",  new TH1D("muon_eta", "muon_eta", 1000, -100, 100)},
    {"muon_phi",  new TH1D("muon_phi", "muon_phi", 1000, -100, 100)},
    {"muon_y",  new TH1D("muon_y", "muon_y", 1000, -100, 100)},
    {"muon_theta",  new TH1D("muon_theta", "muon_theta", 1000, -100, 100)},
    {"muon_lxy",  new TH1D("muon_lxy", "muon_lxy", 1000, 0, 100)},
    {"muon_lz",  new TH1D("muon_lz", "muon_lz", 1000, 0, 100)},
    {"muon_lxyz",  new TH1D("muon_lxyz", "muon_lxyz", 1000, 0, 100)},
    {"muon_ctau",  new TH1D("muon_ctau", "muon_ctau", 1000, 0, 100)},
    {"muon_boost",  new TH1D("muon_boost", "muon_boost", 1000, 0, 1000)},

    {"muon_deltaR",  new TH1D("muon_deltaR", "muon_deltaR", 1000, 0, 100)},
    {"muon_deltaPhi",  new TH1D("muon_deltaPhi", "muon_deltaPhi", 1000, -100, 100)},
    
    {"dimuon_pt",  new TH1D("dimuon_pt", "dimuon_pt", 1000, 0, 1000)},
    {"dimuon_pz",  new TH1D("dimuon_pz", "dimuon_pz", 1000, -1000, 1000)},
    {"dimuon_mass",  new TH1D("dimuon_mass", "dimuon_mass", 1000, 0, 100)},
    {"dimuon_eta",  new TH1D("dimuon_eta", "dimuon_eta", 1000, -100, 100)},
    {"dimuon_phi",  new TH1D("dimuon_phi", "dimuon_phi", 1000, -100, 100)},
    
    {"first_mother_pt",  new TH1D("first_mother_pt", "first_mother_pt", 1000, 0, 1000)},
    {"first_mother_pz",  new TH1D("first_mother_pz", "first_mother_pz", 1000, -1000, 1000)},
    {"first_mother_mass",  new TH1D("first_mother_mass", "first_mother_mass", 1000, 0, 200)},
    {"first_mother_eta",  new TH1D("first_mother_eta", "first_mother_eta", 1000, -100, 100)},
    {"first_mother_phi",  new TH1D("first_mother_phi", "first_mother_phi", 1000, -100, 100)},
    {"first_mother_lxy",  new TH1D("first_mother_lxy", "first_mother_lxy", 1000, 0, 100)},
    {"first_mother_lz",  new TH1D("first_mother_lz", "first_mother_lz", 1000, 0, 100)},
    {"first_mother_lxyz",  new TH1D("first_mother_lxyz", "first_mother_lxyz", 1000, 0, 100)},
    {"first_mother_ctau",  new TH1D("first_mother_ctau", "first_mother_ctau", 1000, 0, 100)},
    {"first_mother_boost",  new TH1D("first_mother_boost", "first_mother_boost", 1000, 0, 100)},
  };
  
  
  auto fill_single_muon_hists = [&](const Particle *muon)->void {
    hists["muon_pt"]->Fill(muon->four_vector.Pt());
    hists["muon_pz"]->Fill(muon->four_vector.Pz());
    hists["muon_mass"]->Fill(muon->four_vector.M());
    hists["muon_eta"]->Fill(muon->four_vector.Eta());
    hists["muon_phi"]->Fill(muon->four_vector.Phi());
    hists["muon_y"]->Fill(muon->four_vector.Rapidity());
    hists["muon_theta"]->Fill(muon->four_vector.Theta());
    hists["muon_lxy"]->Fill(sqrt(pow(muon->x, 2) + pow(muon->y, 2)));
    hists["muon_lz"]->Fill(muon->z);
    hists["muon_lxyz"]->Fill(sqrt(pow(muon->x, 2) + pow(muon->y, 2) + pow(muon->z, 2)));
    hists["muon_ctau"]->Fill(muon->ctau);
    hists["muon_boost"]->Fill(muon->momentum()/muon->mass);
  };

  auto fill_double_muon_hists =  [&](const Particle *muon1,const Particle *muon2)->void {
    hists["muon_deltaPhi"]->Fill(muon1->four_vector.DeltaPhi(muon2->four_vector));
    hists["muon_deltaR"]->Fill(muon1->four_vector.DeltaR(muon2->four_vector));
  };
  
  auto fill_dimuon_hists = [&](const TLorentzVector &dimuon)->void {
    hists["dimuon_pt"]->Fill(dimuon.Pt());
    hists["dimuon_pz"]->Fill(dimuon.Pz());
    hists["dimuon_mass"]->Fill(dimuon.M());
    hists["dimuon_eta"]->Fill(dimuon.Eta());
    hists["dimuon_phi"]->Fill(dimuon.Phi());
  };
  
  auto fill_first_mother_hists = [&](const Particle *mother)->void {
    hists["first_mother_pt"]->Fill(mother->four_vector.Pt());
    hists["first_mother_pz"]->Fill(mother->four_vector.Pz());
    hists["first_mother_mass"]->Fill(mother->four_vector.M());
    hists["first_mother_eta"]->Fill(mother->four_vector.Eta());
    hists["first_mother_phi"]->Fill(mother->four_vector.Phi());
    hists["first_mother_lxy"]->Fill(sqrt(pow(mother->x, 2) + pow(mother->y, 2)));
    hists["first_mother_lz"]->Fill(mother->z);
    hists["first_mother_lxyz"]->Fill(sqrt(pow(mother->x, 2) + pow(mother->y, 2) + pow(mother->z, 2)));
    hists["first_mother_ctau"]->Fill(mother->ctau);
    hists["first_mother_boost"]->Fill(mother->momentum()/mother->mass);
  };
  
  int i_event=0;
  
  for(auto event : events){
    
    i_event++;
    
    if(!event->has_ttbar_pair()) continue;
    int preselection_code = event->passes_preselection();
    
    if(preselection_code == 0){
      continue;
    }
    else if(preselection_code == 1){ // single muon tree
      auto muon = event->get_single_muon();
      
      if(!muon){
        cout<<"\n\nERROR -- single muon not found in an event passing single muon preselection...\n\n"<<endl;
        continue;
      }
      
      fill_single_muon_hists(muon);
      
      // TODO: handle properly multiple mothers case
      auto mother = event->particles[muon->mothers[0]];
      fill_first_mother_hists(mother);
    }
    else if(preselection_code == 2){ // pair category
      auto muons = event->get_muon_pair();
      
      for(auto muon_pair : muons){
        auto muon_1 = get<0>(muon_pair);
        auto muon_2 = get<1>(muon_pair);
        
        fill_single_muon_hists(muon_1);
        fill_single_muon_hists(muon_2);
        
        TLorentzVector dimuon = muon_1->four_vector + muon_2->four_vector;
        fill_dimuon_hists(dimuon);
        fill_double_muon_hists(muon_1, muon_2);
        
        // TODO: handle the full chain of mother (and multiple mothers) correctly
        auto mother = event->particles[muon_1->mothers[0]];
        fill_first_mother_hists(mother);
      }
    }
    else if(preselection_code == 3){ // non-pair category
      
      // Fill in hists for the opposite sign non-pair (if exists)
      auto [opposite_sign_muon_1, opposite_sign_muon_2] = event->get_smallest_deltaR_opposite_sign_muon_non_pair();
      
      if(opposite_sign_muon_1 && opposite_sign_muon_2){
        fill_single_muon_hists(opposite_sign_muon_1);
        fill_single_muon_hists(opposite_sign_muon_2);
        TLorentzVector dimuon = opposite_sign_muon_1->four_vector + opposite_sign_muon_2->four_vector;
        fill_dimuon_hists(dimuon);
        fill_double_muon_hists(opposite_sign_muon_1,opposite_sign_muon_2);
        
        auto mother_1 = event->particles[opposite_sign_muon_1->mothers[0]];
        fill_first_mother_hists(mother_1);
        
        auto mother_2 = event->particles[opposite_sign_muon_2->mothers[0]];
        fill_first_mother_hists(mother_2);
      }
      
      // Fill in hists for the opposite sign non-pair (if exists)
      auto [same_sign_muon_1, same_sign_muon_2] = event->get_smallest_deltaR_same_sign_muon_non_pair();
      
      if(same_sign_muon_1 && same_sign_muon_2){
        fill_single_muon_hists(same_sign_muon_1);
        fill_single_muon_hists(same_sign_muon_2);
        TLorentzVector dimuon = same_sign_muon_1->four_vector + same_sign_muon_2->four_vector;
        fill_dimuon_hists(dimuon);
        fill_double_muon_hists(same_sign_muon_1,same_sign_muon_1);
        
        auto mother_1 = event->particles[same_sign_muon_1->mothers[0]];
        fill_first_mother_hists(mother_1);
        
        auto mother_2 = event->particles[same_sign_muon_2->mothers[0]];
        fill_first_mother_hists(mother_2);
      }
      
      // TODO: decide what to do with same vs. opposite sign cases (different histograms? separate output files?)
    }
  }
  
  // close files
  output_file->cd();
  for(auto &[name, hist] : hists) hist->Write();
  
  input_file->Close();
  output_file->Close();
  
  return 0;
}
