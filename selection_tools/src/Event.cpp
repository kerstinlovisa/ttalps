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
//  setup_motherless_particles();
}

void Event::setup_particle_mothers()
{
  for(int i_particle=0; i_particle<particles.size(); i_particle++){
    for(int daughter_index : particles[i_particle]->daughters){
      if(daughter_index >= 0){
        if(daughter_index != i_particle) particles.at(daughter_index)->mothers.push_back(i_particle);
        else particles.at(daughter_index)->is_selfmother = true;
      }
    }
  }
}

void Event::setup_motherless_particles()
{
  for(auto particle : particles){
    if(particle->mothers.size() !=0 ) continue; // skip if has mother(s)
    if(particle->is_selfmother) continue; // skip if it is its own mother (e.g. p -> p g)
    if(particle->pdgid == 21) continue; // skip gluons, which do crazy stuff we don't care about
    if(particle->status == 71) continue; // skip "copied partons to collect into contiguous colour singlet"
    
//    cout<<"\n\nWARNING -- encountered a motherless particle. This may happen when HEPMC event had a vertex "<<endl;
//    cout<<"with more particles attached to it than we were willing to store.\n\n"<<endl;
//    particle->print();
    particle->mothers.push_back(-1);
  }
}

int Event::get_n_muons()
{
  int n_muons = 0;
  for(auto particle : particles) if(abs(particle->pdgid)==13) n_muons++;
  return n_muons;
}

int Event::get_n_non_top_muons()
{
  int n_muons = 0;
  for(auto particle : particles){
    if(abs(particle->pdgid)!=13) continue;
    if(particle->has_top_ancestor(particles)) continue;
    n_muons++;
  }
  return n_muons;
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
    
    if(particle->pdgid == 6 && particle->status == 62) top_found = true;
    else if(particle->pdgid == -6 && particle->status == 62) atop_found = true;
  }
  
  return top_found && atop_found;
}

vector<int> Event::get_sisters_indices(Particle *mother, int i_particle)
{
  int sister_1_index = -1;
  int sister_2_index = -1;
  
  vector<int> sister_indices;
  
  for(int daughter_index : mother->daughters){
    if(daughter_index != i_particle) sister_indices.push_back(daughter_index);
  }
  
  return sister_indices;
}

tuple<bool, bool> Event::check_sister(int sister_index, Particle *particle, vector<Particle*> particles)
{
  if(sister_index < 0) return {false, false};
  
  auto sister = particles[sister_index];
  
  if(abs(sister->pdgid) != 13) return {false, false};
  
  bool same_sign_sister = false;
  bool opposite_sign_sister = false;
  
  if(particle->pdgid == sister->pdgid)  same_sign_sister = true;
  else                                  opposite_sign_sister = true;
  
  return {same_sign_sister, opposite_sign_sister};
}

bool Event::are_non_top_muons_siblings()
{
  int n_non_top_muons = 0;
  int n_opposite_sign_pairs = 0;
  int n_same_sign_pairs = 0;
  int n_motherless_muons = 0;
  
  vector<int> muon_status;
  vector<int> already_accounted_for;
  
  int i_particle = -1;
  
  for(auto particle : particles){
    i_particle++;
    
    if(!particle->is_final()) continue;
    if(abs(particle->pdgid) != 13) continue;
    if(particle->has_top_ancestor(particles)) continue;
    
    n_non_top_muons++;
    muon_status.push_back(particle->status);
    
    if(find(already_accounted_for.begin(), already_accounted_for.end(), i_particle) != already_accounted_for.end()) continue;
    
//    check for motherless muons
    if(particle->mothers.size() == 0){
      cout<<"Found weird particle with no mothers... skipping."<<endl;
      particle->print();
      n_motherless_muons++;
      continue;
    }
    int mother_index = particle->mothers[0];
    if(mother_index < 0){
      n_motherless_muons++;
      continue;
    }
    
    auto mother = particles[particle->mothers[0]];
    vector<int> sister_indices = get_sisters_indices(mother, i_particle);
    
    for(int sister_index : sister_indices){
      already_accounted_for.push_back(sister_index);
      
      auto [same_sign, opposite_sign] = check_sister(sister_index, particle, particles);
      n_same_sign_pairs += same_sign;
      n_opposite_sign_pairs += opposite_sign;
    }
    
    
  }
  
  cout<<"n_muons: "<<n_non_top_muons<<" (";
  for(int status : muon_status) cout<<status<<",";
  cout<<"), ";
  cout<<"N motherless muons: "<<n_motherless_muons<<", ";
  cout<<"N same sign pairs: "<<n_same_sign_pairs<<", ";
  cout<<"N opposite sign pairs: "<<n_opposite_sign_pairs<<endl;
  
  return n_opposite_sign_pairs > 0;
  
}


