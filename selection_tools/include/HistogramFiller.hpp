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
  HistogramFiller(bool reduce_hists=false, bool include_alp_ancestor_hists=false);
  ~HistogramFiller();
  
  void fill_deltaR_deltal_selections(const Particle* particle_1, const Particle* particle_2, const Event *event,
                                     std::string sign, std::string prefix);
  
  void fill_hists(const Particle* particle_1, const Particle* particle_2, const Event *event, std::string sign);
  void fill_final_selection_hists(const Particle* particle_1, const Particle* particle_2, const Event *event, std::string sign);
  void fill_first_muon_from_alp_selection_hists(const Particle* particle, const Event *event);
  void fill_alp_in_preselection_hists(const Particle* particle_1, const Particle* particle_2, const Particle* mother, const Event *event, std::string sign);
  
  void fill_2d_hists(const Particle* particle_1, const Particle* particle_2, std::string sign);

  void save_histograms(std::string output_path);
  std::map<std::string, HistogramSet*> histSets;
  
private:
  CutsManager cutsManager;
  std::vector<double> ptCuts;
  bool reduceHists=false;
};

#endif /* HistogramFiller_hpp */
