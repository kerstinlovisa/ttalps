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
  
  bool has_orphant_muons();
  bool has_two_opposite_sign_muons();
  bool has_ttbar_pair();
  bool are_non_top_muons_siblings();
  
  std::vector<Particle*> particles;
  std::vector<Particle*> muons;
  
private:
  void setup_particle_mothers();
  void find_muons();
  void setup_motherless_particles();
};

#endif /* Event_hpp */
