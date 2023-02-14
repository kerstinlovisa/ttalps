#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#include <TFile.h>
#include <TTree.h>

#include "Particle.hpp"
#include "Event.hpp"
#include "EventReader.hpp"

using namespace std;

int max_events = 1000;

TFile *input_file, *output_file_siblings, *output_file_non_siblings;

TTree* get_input_tree(string input_path)
{
  input_file = TFile::Open(input_path.c_str());
  
  if(!input_file){
    cout<<"ERROR -- could not open input file: "<<input_path<<endl;
    exit(0);
  }
  
  return (TTree*)input_file->Get("Events");
}

tuple<TTree*, TTree*> get_output_trees(TTree *input_tree, string siblings_path, string non_siblings_path, string file_name)
{
  system(("mkdir -p " + siblings_path).c_str());
  system(("mkdir -p " + non_siblings_path).c_str());
  
  output_file_siblings = new TFile((siblings_path + file_name).c_str(), "recreate");
  output_file_non_siblings = new TFile((non_siblings_path + file_name).c_str(), "recreate");
  
  output_file_siblings->cd();
  auto tree_siblings = input_tree->CloneTree(0);
  
  output_file_non_siblings->cd();
  auto tree_non_siblings = input_tree->CloneTree(0);
  
  return {tree_siblings, tree_non_siblings};
}

int main(int argc, char *argv[])
{
  if(argc != 5){
    cout<<"Usage: ./apply_selections file_name input_path output_siblings_path output_non_siblings_path"<<endl;
    exit(0);
  }
  
  string file_name = argv[1];
  string input_path = argv[2];
  
  auto input_tree = get_input_tree(input_path+file_name);
  auto [output_tree_siblings, output_tree_non_siblings] = get_output_trees(input_tree, argv[3], argv[4], file_name);
  
// load events
  auto event_reader = EventReader(max_events);
  auto events = event_reader.read_events(input_tree);
  
// fill output tree and cut flow
  map<string, int> cut_flow = {
    {"0_initial", 0},
//    {"1_no_orphant_muons", 0},
    
    {"1_tt_pair", 0},
    {"2_n_muons_ge_2", 0},
    {"3_os_muons", 0},
    {"4_sibling_muons", 0}
  };
  
  int i_event=0;
  
  for(auto event : events){
    output_tree_siblings->GetEntry(i_event);
    output_tree_non_siblings->GetEntry(i_event);
    
    i_event++;
    
    cut_flow["0_initial"]++;
    
    if(!event->has_ttbar_pair()) continue;
    cut_flow["1_tt_pair"]++;
    
    if(event->muons.size() < 2) continue;
    cut_flow["2_n_muons_ge_2"]++;
    
    if(!event->has_two_opposite_sign_muons()) continue;
    cut_flow["3_os_muons"]++;
    
    if(!event->are_non_top_muons_siblings()){
      output_file_non_siblings->cd();
      output_tree_non_siblings->Fill();
      continue;
    }
    cut_flow["4_sibling_muons"]++;
    
    output_file_siblings->cd();
    output_tree_siblings->Fill();
  }
  
  cout<<"\n\nCut flow: "<<endl;
  for(auto &[cut_name, n_events] : cut_flow){
    cout<<cut_name<<": "<<n_events<<endl;
  }
  
  // close files
  output_tree_siblings->AutoSave();
  output_tree_non_siblings->AutoSave();
  
  output_file_siblings->Close();
  output_file_non_siblings->Close();
  input_file->Close();
  
  return 0;
}
