//
//  CutsManager.cpp
//  selections
//
//  Created by Jeremi Niedziela on 04/04/2023.
//

#include "CutsManager.hpp"

using namespace std;

CutsManager::CutsManager()
{
  masses["rho"] = 0.78;
  masses["phi"] = 1.02;
  masses["Jpsi"] = 3.09;
  masses["psi"] = 3.68;
  masses["Z"] = 91.19;
  
  mass_cuts["rho"] = 0.04;
  mass_cuts["phi"] = 0.05;
  mass_cuts["Jpsi"] = 0.04;
  mass_cuts["psi"] = 0.18;
  mass_cuts["Z"] = 4.56;
  
  for(auto &[particle_name, mass] : masses){
    mass_min[particle_name] = mass - mass_cuts[particle_name];
    mass_max[particle_name] = mass + mass_cuts[particle_name];
  }
}

bool CutsManager::passes_mass_cuts(const TLorentzVector &diparticle)
{
  float mass = diparticle.M();
  
  for(auto &[particle_name, min] : mass_min){
    float max = mass_max[particle_name];
    if(mass < max && mass > min) return false;
  }
  
  return true;
}
