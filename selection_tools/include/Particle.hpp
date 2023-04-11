//
// Created by Jeremi Niedziela on 10/02/2023.
//

#ifndef SELECTION_TOOLS_PARTICLE_H
#define SELECTION_TOOLS_PARTICLE_H

#include <vector>

#include <TLorentzVector.h>

class Particle
{
public:
  Particle(float _x, float _y, float _z, float _px, float _py, float _pz, float _energy, float _mass, float _ctau,
           int _pdgid, std::vector<int> _daughters, int _status, int _index, int _barcode);
  ~Particle(){}
  
  void print();
  
  bool is_muon(){return abs(pdgid)==13;}
  bool is_good_non_top_muon(const std::vector<Particle*> &particles);
  bool is_motherless();
  
  bool has_top_ancestor(const std::vector<Particle*> &other_particles);
  bool has_alp_ancestor(const std::vector<Particle*> &other_particles);
  bool is_final();
  
  double eta();
  double momentum() const;
  double pt() const;
  TVector3 boost() const;  
  Particle* transform(TVector3 boost);

  float x, y, z, px, py, pz, energy, mass, ctau;
  std::vector<int> mothers, daughters;
  int pdgid, status, index, barcode;
  bool is_selfmother;
  
  TLorentzVector four_vector;
};


#endif //SELECTION_TOOLS_PARTICLE_H
