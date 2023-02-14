//
// Created by Jeremi Niedziela on 10/02/2023.
//
#include <cstdlib>
#include <vector>
#include <iostream>

#include "Particle.hpp"

using namespace std;

Particle::Particle(float _x, float _y, float _z, float _px, float _py, float _pz, float _energy, float _mass, float _ctau,
                   int _pdgid, int _daughter_1, int _daughter_2, int _daughter_3, int _status, int _index, int _barcode):
x(_x), y(_y), z(_z), px(_px), py(_py), pz(_pz), energy(_energy), mass(_mass), ctau(_ctau),
pdgid(_pdgid), status(_status), index(_index), barcode(_barcode)
{
  daughters.push_back(_daughter_1);
  daughters.push_back(_daughter_2);
  daughters.push_back(_daughter_3);
}

void Particle::print()
{
  cout<<"Particle "<<index<<" ("<<pdgid<<"), daughters: ";
  for(int daughter : daughters) cout<<"\t"<<daughter;
  cout<<"\tn_mothers: "<<mothers.size()<<"\tbar: "<<barcode<<endl;
}


bool Particle::has_top_ancestor(const vector<Particle*> &other_particles)
{
  if(abs(pdgid) == 6) return true;
  if(mothers.size()==0) return false;
  
  for(int mother_index : mothers){
    if(mother_index<0) continue;
    
    auto mother = other_particles.at(mother_index);
    if(mother->has_top_ancestor(other_particles)) return true;
  }
  return false;
}

bool Particle::is_final()
{
  if(abs(pdgid) == 6) return status == 62;
  
  return true;
}
