//
//  HistogramSet.hpp
//  selections
//
//  Created by Jeremi Niedziela on 24/02/2023.
//

#ifndef HistogramSet_hpp
#define HistogramSet_hpp

#include <map>
#include <string>

#include <TH1D.h>

#include "Particle.hpp"

class HistogramSet {
public:
  HistogramSet(std::string prefix);
  
  void fill(const Particle* particle);
  void fill(const Particle* particle_1, const Particle* particle_2);
  
  std::map<std::string, TH1D*> hists;
};

#endif /* HistogramSet_hpp */
