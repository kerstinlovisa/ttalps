//
// Created by Jeremi Niedziela on 10/02/2023.
//
#include <cstdlib>
#include <vector>
#include <iostream>
#include <TLorentzRotation.h>

#include "Particle.hpp"

using namespace std;

Particle::Particle(float _x, float _y, float _z, float _px, float _py, float _pz, float _energy, float _mass, float _ctau,
                   int _pdgid, vector<int> _daughters, int _status, int _index, int _barcode):
x(_x), y(_y), z(_z), px(_px), py(_py), pz(_pz), energy(_energy), mass(_mass), ctau(_ctau),
pdgid(_pdgid), daughters(_daughters), status(_status), index(_index), barcode(_barcode)
{
  is_selfmother = false;
  
  four_vector = TLorentzVector();
  four_vector.SetPxPyPzE(px, py, pz, energy);
}

Particle::Particle(TVector3 boost, Particle* particle):
ctau(particle->ctau), pdgid(particle->pdgid), daughters(particle->daughters), 
status(particle->status), index(particle->index), barcode(particle->barcode)
{
  TLorentzRotation rotation(boost);
  rotation.Invert();
  TLorentzVector transformed_four_vector = rotation * four_vector;

  x = transformed_four_vector.X();
  y = transformed_four_vector.Y();
  z = transformed_four_vector.Z();
  px = transformed_four_vector.Px(); 
  py = transformed_four_vector.Py();
  pz = transformed_four_vector.Pz();
  energy = transformed_four_vector.E();
  mass = transformed_four_vector.M();
}

void Particle::print()
{
  cout<<"Particle "<<index<<" (pdg: "<<pdgid<<", status: "<<status<<"), daughters: ";
  for(int daughter : daughters) cout<<"\t"<<daughter;
  cout<<"\tmothers: ";
  for(int mother : mothers) cout<<"\t"<<mother;
  cout<<"\tbar: "<<barcode<<endl;
}

bool Particle::is_good_non_top_muon(const vector<Particle*> &particles, bool include_lxy_selection)
{
  if(!is_final()) return false;
  if(abs(pdgid) != 13) return false;
  if(fabs(eta()) > 2.5) return false;
  if(pt() < 5) return false;
  if(has_top_ancestor(particles)) return false;
  if(pow(energy, 2) - pow(momentum(), 2) < 0) return false;
  if(include_lxy_selection) {if(is_prompt()) return false;}
  
  return true;
}

bool Particle::is_motherless()
{
  if(mothers.size() == 0) return true;
  
  for(int mother_index : mothers){
    if(mother_index < 0) return true;
  }
  
  return false;
}

bool Particle::has_top_ancestor(const vector<Particle*> &other_particles)
{
  if(abs(pdgid) == 6 && status >= 60) return true;
  if(mothers.size()==0) return false;
  
  for(int mother_index : mothers){
//    if(mother_index<0) continue;
    
    auto mother = other_particles.at(mother_index);
    if(mother->has_top_ancestor(other_particles)) return true;
  }
  return false;
}

bool Particle::has_alp_ancestor(const vector<Particle*> &other_particles)
{
  if(abs(pdgid) == 9000005) return true;
  if(mothers.size()==0) return false;
  
  for(int mother_index : mothers){
    auto mother = other_particles.at(mother_index);
    if(mother->has_alp_ancestor(other_particles)) return true;
  }
  return false;
}

bool Particle::is_final()
{
  if(abs(pdgid) == 6) return status == 62;
  if(abs(pdgid) == 13) return status == 1;
  
  return true;
}

bool Particle::is_prompt()
{
  if(sqrt(pow(x, 2) + pow(y, 2)) > 0.2) return false;

  return true;
}

double Particle::eta()
{
  return four_vector.Eta();
}

double Particle::momentum() const
{
  return four_vector.P();
}

double Particle::pt() const
{
  return four_vector.Pt();
}

TVector3 Particle::get_boost() const
{
  return four_vector.BoostVector();
}

