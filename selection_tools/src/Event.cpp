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
//  setup_motherless_particles();
}

void Event::setup_particle_mothers()
{
  for(int i_particle=0; i_particle<particles.size(); i_particle++){
    for(int daughter_index : particles[i_particle]->daughters){
      if(daughter_index >= 0 && daughter_index != i_particle) particles.at(daughter_index)->mothers.push_back(i_particle);
    }
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

tuple<int, int> Event::get_sisters_indices(Particle *mother, int i_particle)
{
  int sister_1_index = -1;
  int sister_2_index = -1;
  
  if(mother->daughters[0] == i_particle){
    sister_1_index = mother->daughters[1];
    sister_2_index = mother->daughters[2];
  }
  if(mother->daughters[1] == i_particle){
    sister_1_index = mother->daughters[0];
    sister_2_index = mother->daughters[2];
  }
  if(mother->daughters[2] == i_particle){
    sister_1_index = mother->daughters[0];
    sister_2_index = mother->daughters[1];
  }
  
  return {sister_1_index, sister_2_index};
}

tuple<bool, bool> Event::check_sister(int sister_index, Particle *particle, vector<Particle*> particles)
{
  bool found_same_sign_muon_siblings = false;
  bool found_non_top_muon_siblings = false;
  
  if(sister_index >= 0){
    auto sister = particles[sister_index];
    
    if(abs(sister->pdgid) == 13){
      if(particle->pdgid == sister->pdgid)  found_same_sign_muon_siblings = true;
      else                                  found_non_top_muon_siblings = true;
    }
  }
  return {found_same_sign_muon_siblings, found_non_top_muon_siblings};
}

bool Event::are_non_top_muons_siblings()
{
  int n_tops = 0;
  int n_atops = 0;
  int n_non_top_muons = 0;
 
  vector<int> top_status;
  vector<int> muon_status;
  
  bool found_opposite_sign_muon_siblings = false;
  bool found_same_sign_muon_siblings = false;
  bool found_muon = false;
  bool found_amuon = false;
  
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
        auto [sister_1_index, sister_2_index] = get_sisters_indices(mother, i_particle);
        
        auto [same_sign, opposite_sign] = check_sister(sister_1_index, particle, particles);
        found_same_sign_muon_siblings |= same_sign;
        found_opposite_sign_muon_siblings |= opposite_sign;
        
        auto [same_sign_2, opposite_sign_2] = check_sister(sister_2_index, particle, particles);
        found_same_sign_muon_siblings |= same_sign_2;
        found_opposite_sign_muon_siblings |= opposite_sign_2;
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
  
  return found_opposite_sign_muon_siblings;
  
}


