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
#include <TH2D.h>

#include "Particle.hpp"
#include "Event.hpp"

class HistogramSet {
public:
  HistogramSet(std::string prefix, bool reduce_hists=false);
  
  void fill(const Particle* particle, const Event* event=nullptr);
  void fill(const Particle* particle_1, const Particle* particle_2, const Event* event=nullptr);
  void fill_2d(const Particle* particle_1, const Particle* particle_2, const Particle* particle_3=nullptr, const Event* event=nullptr);
  
  std::map<std::string, TH1D*> hists;
  std::map<std::string, TH2D*> hists2d;

  float* logxBins(const int n_bins, const float min, const float max);
private:
  bool reduce_hists_=false;
};

#endif /* HistogramSet_hpp */
