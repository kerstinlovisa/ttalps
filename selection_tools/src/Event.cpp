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
  vector<int> sister_indices;
  
  for(int daughter_index : mother->daughters){
    if(daughter_index != i_particle) sister_indices.push_back(daughter_index);
  }
  
  return sister_indices;
}

int Event::check_sister(int sister_index, Particle *particle, vector<Particle*> particles)
{
  // 0: bad particle, -1: opposite sign, +1: same sign
  if(sister_index < 0) return 0;
  sister_index = get_final_state_particle_index(sister_index, particles);
  auto sister = particles[sister_index];

  if(!sister->is_good_non_top_muon(particles)) return 0;
  if(particle->pdgid == sister->pdgid)  return 1;
  else                                  return -1;
}

int Event::get_final_state_particle_index(int particle_index, vector<Particle*> particles)
{
  bool daughter_exists = true;
  int new_particle_index = particle_index;
  while(daughter_exists){
    daughter_exists = false;
    for (auto daughter_index : particles[new_particle_index]->daughters){
      if (daughter_index > 0) {
        if (particles[daughter_index]->pdgid == particles[particle_index]->pdgid){
          daughter_exists = true;
          new_particle_index = daughter_index;
        }
      }
    }
  }
  return new_particle_index;
}

int Event::passes_preselection(bool include_lxy_selection)
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
    
    if(!particle->is_good_non_top_muon(particles, include_lxy_selection)) continue;
    
    if(particle->is_motherless()){
      cout<<"Found weird particle with no mothers... skipping."<<endl;
      particle->print();
      n_motherless_muons++;
      continue;
    }
    
    n_non_top_muons++;
    muon_status.push_back(particle->status);
    
    if(find(already_accounted_for.begin(), already_accounted_for.end(), i_particle) != already_accounted_for.end()) continue;
    
    // look for sisters
    auto mother = particles[particle->mothers[0]];
    auto last_muon_index = i_particle;
    while (abs(mother->pdgid) == 13) {
      last_muon_index = mother->index;
      mother = particles[mother->mothers[0]];
    }
    vector<int> sister_indices = get_sisters_indices(mother, last_muon_index);
    
    for(int sister_index : sister_indices){
      already_accounted_for.push_back(sister_index);
      
      int sister_code = check_sister(sister_index, particle, particles);
      
      if(sister_code == -1) n_opposite_sign_pairs++;
      else if(sister_code == 1) n_same_sign_pairs++;
    }
  }
  
  if(n_same_sign_pairs != 0){
    // should never happen
    cout<<"\n\nWARNING -- found same sign siblings\n\n"<<endl;
  }
  
  // single muon category
  if(n_non_top_muons == 1) return 1;
  // pair category
  if(n_opposite_sign_pairs >= 1) return 2;
  // non-pair category
  if(n_non_top_muons >= 2) return 3;
  // doesn't pass preselection
  return 0;
}

Particle* Event::get_single_muon()
{
  for(auto particle : particles){
    if(!particle->is_good_non_top_muon(particles)) continue;
    return particle;
  }
  
  return nullptr;
}


vector<tuple<Particle*, Particle*>> Event::get_muon_pair()
{
  vector<int> already_accounted_for;
  
  vector<tuple<Particle*, Particle*>> muons;
  
  int i_particle = -1;
  
  for(auto particle : particles){
    i_particle++;
    
    if(!particle->is_good_non_top_muon(particles)) continue;
    
    if(find(already_accounted_for.begin(), already_accounted_for.end(), i_particle) != already_accounted_for.end()) continue;
    
    // look for sisters
    if(particle->mothers.size() == 0) continue;
    
    auto mother = particles[particle->mothers[0]];
    vector<int> sister_indices = get_sisters_indices(mother, i_particle);
    
    for(int sister_index : sister_indices){
      already_accounted_for.push_back(sister_index);
      
      int sister_code = check_sister(sister_index, particle, particles);
      
      if(sister_code == -1){
        muons.push_back(std::make_tuple(particle,particles[sister_index]));
      }
    }
  }
  
  return muons;
}

tuple<Particle*, Particle*> Event::get_smallest_deltaR_muon_pair(vector<tuple<Particle*, Particle*>> muon_pairs)
{
  tuple<Particle*, Particle*> muons;
  double deltaR_min = 1000.0;
  for(auto muon_pair : muon_pairs){
    auto muon_1 = get<0>(muon_pair);
    auto muon_2 = get<1>(muon_pair);
    double deltaR = muon_1->four_vector.DeltaR(muon_2->four_vector);
    if(deltaR < deltaR_min){
      muons = {muon_1, muon_2};
      deltaR_min = deltaR;
    }
  }
  return muons;
}

tuple<Particle*, Particle*> Event::get_smallest_deltaR_same_sign_muon_non_pair()
{  
  int muon1_index = -1;
  int muon2_index= -1;
  double deltaR_min = 1000.0;
  for(int i=0; i<particles.size(); i++){
    if(!particles[i]->is_good_non_top_muon(particles)) continue;
    for(int j=i+1; j<particles.size(); j++)
    {
      if (j==i) continue;
      if (particles[i]->pdgid != particles[j]->pdgid) continue;
      if(!particles[j]->is_good_non_top_muon(particles)) continue;

      double deltaR = particles[i]->four_vector.DeltaR(particles[j]->four_vector);
      if (deltaR < deltaR_min)
      {
        muon1_index= i;
        muon2_index= j;
        deltaR_min = deltaR;
      }
    }
  }
  if (muon1_index>0 && muon2_index>0) return {particles[muon1_index],particles[muon2_index]};
  return {nullptr, nullptr};
}

tuple<Particle*, Particle*> Event::get_smallest_deltaR_opposite_sign_muon_non_pair()
{
  int muon1_index = -1;
  int muon2_index= -1;
  double deltaR_min = 1000.0;
  for(int i=0; i<particles.size(); i++){
    if(!particles[i]->is_good_non_top_muon(particles)) {
      continue;
    }
    for(int j=i+1; j<particles.size(); j++)
    {
      if (j==i) continue;
      if (particles[i]->pdgid == particles[j]->pdgid) continue;
      if(!particles[j]->is_good_non_top_muon(particles)) continue;

      double deltaR = particles[i]->four_vector.DeltaR(particles[j]->four_vector);
      if (deltaR < deltaR_min)
      {
        muon1_index= i;
        muon2_index= j;
        deltaR_min = deltaR;
      }
    }
  }
  if (muon1_index>0 && muon2_index>0) {
    return {particles[muon1_index],particles[muon2_index]};
  }
  return {nullptr, nullptr};
}

std::tuple<Particle*, Particle*> Event::get_smallest_deltaLxyRatio_opposite_sign_muons()
{
  int muon1_index = -1;
  int muon2_index= -1;
  double ratio_min = 1000.0;
  float epsilon = 1e-10;
  float x1, x2, y1, y2;
  for(int i=0; i<particles.size(); i++){
    if(!particles[i]->is_good_non_top_muon(particles)) {
      continue;
    }
    for(int j=i+1; j<particles.size(); j++)
    {
      if (j==i) continue;
      if (particles[i]->pdgid == particles[j]->pdgid) continue;
      if(!particles[j]->is_good_non_top_muon(particles)) continue;

      x1 = particles[i]->x;
      y1 = particles[i]->y;
      x2 = particles[j]->x + epsilon;
      y2 = particles[j]->y + epsilon;

      float delta_lxy_ratio = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))/sqrt(pow(x1 + x2, 2) + pow(y1 + y2, 2));

      if (delta_lxy_ratio < ratio_min)
      {
        muon1_index= i;
        muon2_index= j;
        ratio_min = delta_lxy_ratio;
      }
    }
  }
  if (muon1_index>0 && muon2_index>0) {
    return {particles[muon1_index],particles[muon2_index]};
  }
  return {nullptr, nullptr};
}

double Event::get_proper_lifetime()
{
  for(auto muon : particles){
    if(!muon->is_muon()) continue;;
    if(!muon->has_alp_ancestor(particles)) continue;
    
    auto mother = particles[muon->mothers[0]];
    return muon->ctau/(mother->momentum()/mother->mass);
  }
  
  return -1;
}
