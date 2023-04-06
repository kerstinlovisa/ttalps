//
//  HistogramFiller.hpp
//  selections
//
//  Created by Jeremi Niedziela on 06/04/2023.
//

#ifndef HistogramFiller_hpp
#define HistogramFiller_hpp

#include <string>
#include <map>

#include "Particle.hpp"
#include "HistogramSet.hpp"
#include "CutsManager.hpp"
#include "Event.hpp"

class HistogramFiller {
public:
  HistogramFiller();
  ~HistogramFiller(){}
  
  void fill_deltaR_deltal_selections(const Particle* particle_1, const Particle* particle_2,
                                     std::string sign, std::string prefix);
  
  void fill_hists(const Particle* particle_1, const Particle* particle_2, const Event *event, std::string sign);
  void fill_final_selection_hists(const Particle* particle_1, const Particle* particle_2, const Event *event, std::string sign);
  void fill_alp_selection_hists(const Particle* particle, const Event *event);
  
  void save_histograms(std::string output_path);
  
private:
  std::map<std::string, HistogramSet*> histSets;
  CutsManager cutsManager;
  
  std::vector<double> ptCuts;
};

#endif /* HistogramFiller_hpp */
