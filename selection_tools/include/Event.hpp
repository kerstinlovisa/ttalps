//
//  Event.hpp
//  selections
//
//  Created by Jeremi Niedziela on 10/02/2023.
//

#ifndef Event_hpp
#define Event_hpp

#include <vector>

#include "Particle.hpp"

class Event
{
public:
  Event(){}
  
  void print_all_particles();
  
  void add_particle(Particle *particle){particles.push_back(particle);}
  
  void setup();
  
  int get_n_muons();
  int get_n_non_top_muons();
  
  bool has_two_opposite_sign_muons();
  bool has_ttbar_pair();
  int passes_preselection();
  
  Particle* get_single_muon();
  std::vector<std::tuple<Particle*, Particle*>> get_muon_pair();
  std::tuple<Particle*, Particle*> get_smallest_deltaR_muon_pair(std::vector<std::tuple<Particle*, Particle*>> muon_pairs);
  std::tuple<Particle*, Particle*> get_smallest_deltaR_same_sign_muon_non_pair();
  std::tuple<Particle*, Particle*> get_smallest_deltaR_opposite_sign_muon_non_pair();
  std::tuple<Particle*, Particle*> get_smallest_deltaLxyRatio_opposite_sign_muons();
  
  std::vector<Particle*> particles;

private:
  void setup_particle_mothers();
  void setup_motherless_particles();
  
  std::vector<int> get_sisters_indices(Particle *mother, int i_particle);
  int check_sister(int sister_index, Particle *particle, std::vector<Particle*> particles);
};

#endif /* Event_hpp */
