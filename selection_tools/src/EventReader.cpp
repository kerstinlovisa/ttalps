//
//  EventReader.cpp
//  selections
//
//  Created by Jeremi Niedziela on 13/02/2023.
//

#include <iostream>

#include "EventReader.hpp"

using namespace std;

std::vector<Event*> EventReader::read_events(TTree *tree)
{
  float cross_section;
  float cross_section_err;

  int n_particles;

  float particle_x[5000];
  float particle_y[5000];
  float particle_z[5000];

  float particle_px[5000];
  float particle_py[5000];
  float particle_pz[5000];

  float particle_energy[5000];
  float particle_mass[5000];

  float particle_ctau[5000];
  int  particle_pid[5000];
  float particle_barcode[5000];

  int particle_daughter[n_daughters][5000];
  
  int particle_status[5000];

  tree->SetBranchAddress("Xsection_value", &cross_section);
  tree->SetBranchAddress("Xsection_error", &cross_section_err);
  
  tree->SetBranchAddress("Event_numberP", &n_particles);
  
  tree->SetBranchAddress("Particle_x", &particle_x);
  tree->SetBranchAddress("Particle_y", &particle_y);
  tree->SetBranchAddress("Particle_z", &particle_z);
  
  tree->SetBranchAddress("Particle_px", &particle_px);
  tree->SetBranchAddress("Particle_py", &particle_py);
  tree->SetBranchAddress("Particle_pz", &particle_pz);
  
  tree->SetBranchAddress("Particle_energy", &particle_energy);
  tree->SetBranchAddress("Particle_mass", &particle_mass);
  
  tree->SetBranchAddress("Particle_ctau", &particle_ctau);
  tree->SetBranchAddress("Particle_pid", &particle_pid);
  tree->SetBranchAddress("Particle_barcode", &particle_barcode);
  
  for(int i=0; i<n_daughters; i++){
    tree->SetBranchAddress(("Particle_d"+to_string(i)).c_str(), &particle_daughter[i]);
  }
  
  tree->SetBranchAddress("Particle_status", &particle_status);
  
//  int particle_index[99999];
  //    for(auto branch : *input_tree->GetListOfBranches()){
  //        if(branch->GetName() == "Particle_index"){
  //            input_tree->SetBranchAddress("Particle_index", particle_index);
  //        }
  //    }
  
  vector<Event*> events;
  
  for(int i_event = 0; i_event < tree->GetEntries(); i_event++){
    if(i_event % 100 == 0)
      cout<<"Event: "<<i_event<<endl;
    if(max_events >= 0 && i_event>=max_events) break;
    
    tree->GetEntry(i_event);
    
    auto event = new Event();
    
    for(int i_particle=0; i_particle<n_particles; i_particle++){
      
      vector<int> daughters = {-1};
      for(int i=0; i<n_daughters; i++){
        daughters.push_back(particle_daughter[i][i_particle]);
        if(particle_daughter[i][i_particle] == -1) break;
      }
      
      auto particle = new Particle(particle_x[i_particle], particle_y[i_particle], particle_z[i_particle],
                                   particle_px[i_particle], particle_py[i_particle], particle_pz[i_particle],
                                   particle_energy[i_particle], particle_mass[i_particle], particle_ctau[i_particle],
                                   particle_pid[i_particle],
                                   daughters,
                                   particle_status[i_particle], i_particle, particle_barcode[i_particle]);
      
      event->add_particle(particle);
    }
    
    event->setup();
    events.push_back(event);
  }
  
  return events;
}

