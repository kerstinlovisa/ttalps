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

int max_events = 100;
int n_daughters = 100;

TFile *input_file, *output_file_single_muon, *output_file_siblings, *output_file_non_siblings;

TTree* get_input_tree(string input_path)
{
  input_file = TFile::Open(input_path.c_str());
  
  if(!input_file){
    cout<<"ERROR -- could not open input file: "<<input_path<<endl;
    exit(0);
  }
  
  return (TTree*)input_file->Get("Events");
}

tuple<TTree*, TTree*, TTree*> get_output_trees(TTree *input_tree, string file_name,
                                               string single_muon_path, string siblings_path, string non_siblings_path)
{
  system(("mkdir -p " + single_muon_path).c_str());
  system(("mkdir -p " + siblings_path).c_str());
  system(("mkdir -p " + non_siblings_path).c_str());
  
  output_file_single_muon = new TFile((single_muon_path + file_name).c_str(), "recreate");
  output_file_siblings = new TFile((siblings_path + file_name).c_str(), "recreate");
  output_file_non_siblings = new TFile((non_siblings_path + file_name).c_str(), "recreate");
  
  output_file_single_muon->cd();
  auto tree_single = input_tree->CloneTree(0);
  
  output_file_siblings->cd();
  auto tree_siblings = input_tree->CloneTree(0);
  
  output_file_non_siblings->cd();
  auto tree_non_siblings = input_tree->CloneTree(0);
  
  return {tree_single, tree_siblings, tree_non_siblings};
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
  
  
  auto hist = new TH1D("hist", "hist", 100, 0, 1000);
  
  int i_event=0;
  
  for(auto event : events){
    
    i_event++;
    
    if(!event->has_ttbar_pair()) continue;
    int preselection_code = event->passes_preselection();
    
    if(preselection_code == 0){
      continue;
    }
    else if(preselection_code == 1){ // single muon tree
    
    }
    else if(preselection_code == 2){ // pair category
      auto [muon_1, muon_2] = event->get_muon_pair();
      
      hist->Fill(muon_1->px);
      hist->Fill(muon_2->px);
    }
    else if(preselection_code == 3){ // non-pair category
    
    }
  }
  
  // close files
  output_file->cd();
  hist->Write();

  input_file->Close();
  output_file->Close();
  
  return 0;
}
