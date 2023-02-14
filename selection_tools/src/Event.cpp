//
//  Event.cpp
//  selections
//
//  Created by Jeremi Niedziela on 10/02/2023.
//

#include <iostream>


#include "Event.hpp"

using namespace std;

void Event::print_all_particles()
{
  for(auto particle : particles) particle->print();
}

void Event::setup()
{
  setup_particle_mothers();
  find_muons();
  setup_motherless_particles();
}

void Event::setup_particle_mothers()
{
  for(int i_particle=0; i_particle<particles.size(); i_particle++){
    int daughter1_index = particles[i_particle]->daughter_1;
    int daughter2_index = particles[i_particle]->daughter_2;
    
    if(daughter1_index >= 0 && daughter1_index != i_particle) particles.at(daughter1_index)->mothers.push_back(i_particle);
    if(daughter2_index >= 0 && daughter2_index != i_particle) particles.at(daughter2_index)->mothers.push_back(i_particle);
  }
}

void Event::setup_motherless_particles()
{
  for(auto particle : particles){
    if(particle->mothers.size()==0){
      particle->mothers.push_back(-1);
    }
  }
}

void Event::find_muons()
{
  for(auto particle : particles){
    if(abs(particle->pdgid)==13) muons.push_back(particle);
  }
}

bool Event::has_two_opposite_sign_muons()
{
  bool positive_muon_found = false;
  bool negative_muon_found = false;
  
  for(auto particle : particles){
    if(abs(particle->pdgid) != 13) continue;
    
    if(particle->has_top_ancestor(particles)) continue;
    
    if(particle->pdgid==13) positive_muon_found = true;
    if(particle->pdgid==-13) negative_muon_found = true;
    
    if(positive_muon_found && negative_muon_found) return true;
  }
  
  return false;
}


bool Event::has_ttbar_pair()
{
  bool top_found = false;
  bool atop_found = false;
  
  for(auto particle : particles){
    if(!particle->is_final()) continue;
    
    if(particle->pdgid == 6) top_found = true;
    else if(particle->pdgid == -6) atop_found = true;
  }
  
  return top_found && atop_found;
}

bool Event::has_orphant_muons()
{
  for(auto particle : particles){
    if(particle->is_muon() && particle->mothers.size()==0) return true;
  }
  return false;
}

bool Event::are_non_top_muons_siblings()
{
  int n_tops = 0;
  int n_atops = 0;
  int n_non_top_muons = 0;
 
  vector<int> top_status;
  vector<int> muon_status;
  
  bool found_non_top_muon_siblings = false;
  bool found_muon = false;
  bool found_amuon = false;
  bool found_same_sign_muon_siblings = false;
  
  int i_particle = 0;
  
  for(auto particle : particles){
    
    if(!particle->is_final()) continue;
    
    if(particle->pdgid == 6){
      n_tops++;
      top_status.push_back(particle->status);
    }
    else if(particle->pdgid == -6){
      n_atops++;
      top_status.push_back(particle->status);
    }
    else if(abs(particle->pdgid)==13 and !particle->has_top_ancestor(particles)){
      n_non_top_muons++;
      muon_status.push_back(particle->status);
      
      if(particle->mothers.size() == 0){
        cout<<"Found weird particle with no mothers... skipping."<<endl;
        particle->print();
        continue;
      }
      
      int mother_index = particle->mothers[0];
      
      if(mother_index >= 0){
      
        auto mother = particles[particle->mothers[0]];
        
        int sister_index = mother->daughter_1 == i_particle ? mother->daughter_2 : mother->daughter_1;
        auto sister = particles[sister_index];
        
        if(abs(sister->pdgid) == 13){
          if(particle->pdgid == sister->pdgid){
            found_same_sign_muon_siblings = true;
          }
          else{
            found_non_top_muon_siblings = true;
          }
        }
      }
      else{
        if(particle->pdgid == 13) found_muon = true;
        if(particle->pdgid == -13) found_amuon = true;
      }
      
      i_particle++;
    }
  }
  
  bool found_motherless_muon_pair = found_muon && found_amuon;
  
  cout<<"n tops: "<<n_tops<<"\tn_atops: "<<n_atops<<" (";
  for(int status : top_status) cout<<status<<",";
  cout<<") "<<"\tn_muons: "<<n_non_top_muons<<" (";
  for(int status : muon_status) cout<<status<<",";
  cout<<") motherless pair: "<<found_motherless_muon_pair<<", ";
  cout<<"same sign pair: "<<found_same_sign_muon_siblings<<endl;
  
  return found_non_top_muon_siblings;
  
}


