//
// Created by Jeremi Niedziela on 10/02/2023.
//

#ifndef SELECTION_TOOLS_PARTICLE_H
#define SELECTION_TOOLS_PARTICLE_H

#include <vector>

class Particle
{
public:
  Particle(float _x, float _y, float _z, float _px, float _py, float _pz, float _energy, float _mass, float _ctau,
           int _pdgid, int _daughter_1, int _daughter_2, int _status, int _index, int _barcode);
  ~Particle(){}
  
  void print();
  
  bool is_muon(){return abs(pdgid)==13;}
  
  bool has_top_ancestor(const std::vector<Particle*> &other_particles);
  bool is_final();
  
  float x, y, z, px, py, pz, energy, mass, ctau;
  int pdgid, daughter_1, daughter_2;
  std::vector<int> mothers;
  int status, index, barcode;
};


#endif //SELECTION_TOOLS_PARTICLE_H
