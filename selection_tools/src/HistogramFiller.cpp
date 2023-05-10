//
//  HistogramFiller.cpp
//  selections
//
//  Created by Jeremi Niedziela on 06/04/2023.
//

#include "HistogramFiller.hpp"
#include "Helpers.hpp"

using namespace std;

HistogramFiller::HistogramFiller(bool reduce_hists, bool include_alp_ancestor_hists)
{
  cutsManager = CutsManager();
  reduceHists=reduceHists;
  
  vector<string> particle_names = {
    // "single_muon",
    // "single_muon_first_mother",
    "os_maxlxy-muon",
    "os_minlxy-muon",
    "os_minpt-muon",
    // "ss_muon",
    // "os_dimuon",
    // "ss_dimuon",
    // "os_first_mother",
    // "ss_first_mother",
  };

  vector<string> hist_names = {
    "", // this is without any selection
    "alp_selection_",
  };

  if(!reduce_hists)
  {
    particle_names.push_back("os_dimuon");
    particle_names.push_back("os_first_mother");
    
    particle_names.push_back("os_first_maxlxy-muon");
    particle_names.push_back("os_first_minlxy-muon");
    particle_names.push_back("os_first_minpt-muon");
    particle_names.push_back("os_first_dimuon");
    particle_names.push_back("os_first_mother_maxlxy-muon");
    particle_names.push_back("os_first_mother_minlxy-muon");
    particle_names.push_back("os_first_mother_minpt-muon");
    particle_names.push_back("os_first_mother_dimuon");
    particle_names.push_back("os_last_mother_maxlxy-muon");
    particle_names.push_back("os_last_mother_minlxy-muon");
    particle_names.push_back("os_last_mother_minpt-muon");
    particle_names.push_back("os_last_mother_dimuon");

    hist_names.push_back("sel_mass-cuts_");
    hist_names.push_back("sel_deltalxy-max0p3mm_");
    hist_names.push_back("sel_deltalxy_ratio_abs-max0p05_");
    hist_names.push_back("sel_deltalxy_ratio_abs-max0p1_");
    hist_names.push_back("sel_deltalxy_ratio_abs-max0p5_");
    hist_names.push_back("sel_eta-max0p1_");
  }
  if(include_alp_ancestor_hists){
    hist_names.push_back("alp_");
    hist_names.push_back("alp_reboosted_");
    hist_names.push_back("alp_final_selection_");
    hist_names.push_back("alp_final_selection_reboosted_");
  }

  ptCuts = {0, 5, 10, 15};

  for(double ptCut : ptCuts){
    string ptName = to_nice_string(ptCut);
    
    if(!reduceHists) hist_names.push_back("sel_pt-min"+ptName+"GeV_");
    hist_names.push_back("final_selection_pt-min"+ptName+"GeV_mass-cuts_");
    
    hist_names.push_back("final_selection_pt-min"+ptName+"GeV_mass-cuts_deltalxy-max0p3mm_");
    hist_names.push_back("final_selection_pt-min"+ptName+"GeV_mass-cuts_deltalxy_ratio_abs-max0p05_");
    hist_names.push_back("final_selection_pt-min"+ptName+"GeV_mass-cuts_deltalxy_ratio_abs-max0p1_");
    hist_names.push_back("final_selection_pt-min"+ptName+"GeV_mass-cuts_deltalxy_ratio_abs-max0p5_");
    
    hist_names.push_back("final_selection_pt-min"+ptName+"GeV_deltalxy-max0p3mm_");
    hist_names.push_back("final_selection_pt-min"+ptName+"GeV_deltalxy_ratio_abs-max0p05_");
    hist_names.push_back("final_selection_pt-min"+ptName+"GeV_deltalxy_ratio_abs-max0p1_");
    hist_names.push_back("final_selection_pt-min"+ptName+"GeV_deltalxy_ratio_abs-max0p5_");
  }
  
  for(string hist : hist_names){
    for(string particle : particle_names){
      string name = hist + particle;
      histSets[name] = new HistogramSet(name, reduce_hists);
    }
  }
  if(!include_alp_ancestor_hists) return;
  histSets["alp_os_first_mother"] = new HistogramSet("alp_os_first_mother", reduce_hists);
  histSets["alp_reboosted_os_first_mother"] = new HistogramSet("alp_reboosted_os_first_mother", reduce_hists);
  histSets["alp_final_selection_os_first_mother"] = new HistogramSet("alp_final_selection_os_first_mother", reduce_hists);
  histSets["alp_final_selection_reboosted_os_first_mother"] = new HistogramSet("alp_final_selection_reboosted_os_first_mother", reduce_hists);
}

HistogramFiller::~HistogramFiller()
{
  for(auto &[setName, histSet] : histSets){
    for(auto &[histName, hist] : histSet->hists){
      delete hist;
    }
    for(auto &[histName, hist] : histSet->hists2d){
      delete hist;
    }
  }
}

void HistogramFiller::fill_deltaR_deltal_selections(const Particle* particle_1,
                                                    const Particle* particle_2,
                                                    const Event* event,
                                                    string sign, string prefix)
{
  float epsilon = 1e-10;
  float x1 = particle_1->x;
  float y1 = particle_1->y;
  float x2 = particle_2->x + epsilon;
  float y2 = particle_2->y + epsilon;

  float delta_lxy = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
  float delta_lxy_ratio_abs = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))/sqrt(pow(abs(x1) + abs(x2), 2) + pow(abs(y1) + abs(y2), 2));

  const Particle* particle_minpt;
  if(particle_1->pt() < particle_1->pt()) {particle_minpt = particle_1;}
  else {particle_minpt = particle_2;}

  if(delta_lxy <= 0.3){
    histSets[prefix + "_deltalxy-max0p3mm_"+sign+"_maxlxy-muon"]->fill(particle_1, event);
    histSets[prefix + "_deltalxy-max0p3mm_"+sign+"_minlxy-muon"]->fill(particle_2, event);
    histSets[prefix + "_deltalxy-max0p3mm_"+sign+"_minpt-muon"]->fill(particle_minpt, event);
    if(!reduceHists) histSets[prefix + "_deltalxy-max0p3mm_"+sign+"_dimuon"]->fill(particle_1, particle_2, event);
  }

  if(delta_lxy_ratio_abs <= 0.05){
    histSets[prefix + "_deltalxy_ratio_abs-max0p05_"+sign+"_maxlxy-muon"]->fill(particle_1, event);
    histSets[prefix + "_deltalxy_ratio_abs-max0p05_"+sign+"_minlxy-muon"]->fill(particle_2, event);
    histSets[prefix + "_deltalxy_ratio_abs-max0p05_"+sign+"_minpt-muon"]->fill(particle_minpt, event);
    if(!reduceHists) histSets[prefix + "_deltalxy_ratio_abs-max0p05_"+sign+"_dimuon"]->fill(particle_1, particle_2, event);
  }
  if(delta_lxy_ratio_abs <= 0.1){
    histSets[prefix + "_deltalxy_ratio_abs-max0p1_"+sign+"_maxlxy-muon"]->fill(particle_1, event);
    histSets[prefix + "_deltalxy_ratio_abs-max0p1_"+sign+"_minlxy-muon"]->fill(particle_2, event);
    histSets[prefix + "_deltalxy_ratio_abs-max0p1_"+sign+"_minpt-muon"]->fill(particle_minpt, event);
    if(!reduceHists) histSets[prefix + "_deltalxy_ratio_abs-max0p1_"+sign+"_dimuon"]->fill(particle_1, particle_2, event);
  }
  if(delta_lxy_ratio_abs <= 0.5){
    histSets[prefix + "_deltalxy_ratio_abs-max0p5_"+sign+"_maxlxy-muon"]->fill(particle_1, event);
    histSets[prefix + "_deltalxy_ratio_abs-max0p5_"+sign+"_minlxy-muon"]->fill(particle_2, event);
    histSets[prefix + "_deltalxy_ratio_abs-max0p5_"+sign+"_minpt-muon"]->fill(particle_minpt, event);
    if(!reduceHists) histSets[prefix + "_deltalxy_ratio_abs-max0p5_"+sign+"_dimuon"]->fill(particle_1, particle_2, event);
  }
}

void HistogramFiller::fill_hists(const Particle* particle_1, const Particle* particle_2, const Event *event, string sign)
{
  if(!particle_1 || !particle_2) return;
  
  float lxy1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2));
  float lxy2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2));
  const Particle* particle_maxlxy;
  const Particle* particle_minlxy;
  const Particle* particle_minpt;
  if (lxy1>=lxy2){
    particle_maxlxy = particle_1;
    particle_minlxy = particle_2;
  }
  else {
    particle_maxlxy = particle_2;
    particle_minlxy = particle_1;
  }
  if(particle_1->pt() < particle_1->pt()) {particle_minpt = particle_1;}
  else {particle_minpt = particle_2;}
    
  histSets[sign+"_maxlxy-muon"]->fill(particle_maxlxy, event);
  histSets[sign+"_minlxy-muon"]->fill(particle_minlxy, event);
  histSets[sign+"_minpt-muon"]->fill(particle_minpt, event);
  if(!reduceHists) histSets[sign+"_dimuon"]->fill(particle_1, particle_2, event);
  
  if(!reduceHists)
  {
    TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;
    // Independent selections:
    for(double ptCut : ptCuts){
      if(particle_1->four_vector.Pt() < ptCut || particle_2->four_vector.Pt() < ptCut) continue;
      
      string ptName = to_nice_string(ptCut);
      
      histSets["sel_pt-min"+ptName+"GeV_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy, event);
      histSets["sel_pt-min"+ptName+"GeV_"+sign+"_minlxy-muon"]->fill(particle_minlxy, event);
      histSets["sel_pt-min"+ptName+"GeV_"+sign+"_minpt-muon"]->fill(particle_minpt, event);
      histSets["sel_pt-min"+ptName+"GeV_"+sign+"_dimuon"]->fill(particle_1, particle_2, event);
    }
    
    if(cutsManager.passes_mass_cuts(diparticle)){
      histSets["sel_mass-cuts_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy, event);
      histSets["sel_mass-cuts_"+sign+"_minlxy-muon"]->fill(particle_minlxy, event);
      histSets["sel_mass-cuts_"+sign+"_minpt-muon"]->fill(particle_minpt, event);
      histSets["sel_mass-cuts_"+sign+"_dimuon"]->fill(particle_1, particle_2, event);
    }

    if(abs(particle_1->four_vector.Eta()) < 0.1 && abs(particle_1->four_vector.Eta()) < 0.1)
    {
      histSets["sel_eta-max0p1_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy, event);
      histSets["sel_eta-max0p1_"+sign+"_minlxy-muon"]->fill(particle_minlxy, event);
      histSets["sel_eta-max0p1_"+sign+"_minpt-muon"]->fill(particle_minpt, event);
      histSets["sel_eta-max0p1_"+sign+"_dimuon"]->fill(particle_1, particle_2, event);
    }
    
    fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, event, sign, "sel");
  }
}

void HistogramFiller::fill_final_selection_hists(const Particle* particle_1, const Particle* particle_2, const Event *event, string sign)
{
  if(!particle_1 || !particle_2) return;
  
  float lxy1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2));
  float lxy2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2));
  const Particle* particle_maxlxy;
  const Particle* particle_minlxy;
  const Particle* particle_minpt;
  if(lxy1 >= lxy2){
    particle_maxlxy = particle_1;
    particle_minlxy = particle_2;
  }
  else {
    particle_maxlxy = particle_2;
    particle_minlxy = particle_1;
  }
  if(particle_1->pt() < particle_1->pt()) {particle_minpt = particle_1;}
  else {particle_minpt = particle_2;}

  TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;
  
  for(double ptCut : ptCuts){
    if(particle_1->four_vector.Pt() < ptCut || particle_2->four_vector.Pt() < ptCut) continue;
      
    string ptName = to_nice_string(ptCut);
    
    if(cutsManager.passes_mass_cuts(diparticle)){
      histSets["final_selection_pt-min"+ptName+"GeV_mass-cuts_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy, event);
      histSets["final_selection_pt-min"+ptName+"GeV_mass-cuts_"+sign+"_minlxy-muon"]->fill(particle_minlxy, event);
      histSets["final_selection_pt-min"+ptName+"GeV_mass-cuts_"+sign+"_minpt-muon"]->fill(particle_minpt, event);
      if(!reduceHists) histSets["final_selection_pt-min"+ptName+"GeV_mass-cuts_"+sign+"_dimuon"]->fill(particle_1, particle_2, event);
      
      fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, event, sign, "final_selection_pt-min"+ptName+"GeV_mass-cuts");
    }
    else{
      fill_deltaR_deltal_selections(particle_maxlxy, particle_minlxy, event, sign, "final_selection_pt-min"+ptName+"GeV");
    }
  }
};

void HistogramFiller::fill_alp_in_preselection_hists(const Particle* particle_1, const Particle* particle_2, const Particle* mother, const Event *event, string sign)
{
  if(!particle_1 || !particle_2) return;
  
  float lxy1 = sqrt(pow(particle_1->x, 2) + pow(particle_1->y, 2));
  float lxy2 = sqrt(pow(particle_2->x, 2) + pow(particle_2->y, 2));
  const Particle* particle_maxlxy;
  const Particle* particle_minlxy;
  const Particle* particle_minpt;
  if (lxy1>=lxy2){
    particle_maxlxy = particle_1;
    particle_minlxy = particle_2;
  }
  else {
    particle_maxlxy = particle_2;
    particle_minlxy = particle_1;
  }
  if(particle_1->pt() < particle_1->pt()) {particle_minpt = particle_1;}
  else {particle_minpt = particle_2;}
    
  histSets["alp_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy);
  histSets["alp_"+sign+"_minlxy-muon"]->fill(particle_minlxy);
  histSets["alp_"+sign+"_minpt-muon"]->fill(particle_minpt);
  histSets["alp_"+sign+"_first_mother"]->fill(mother);
  histSets["alp_"+sign+"_dimuon"]->fill(particle_1, particle_2);
  histSets["alp_"+sign+"_first_mother"]->fill_2d(particle_1, particle_2, mother);

  TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;

  if(particle_1->four_vector.Pt() > 10 || particle_2->four_vector.Pt() > 10)
  {
    if(cutsManager.passes_mass_cuts(diparticle))
    {
      float epsilon = 1e-10;
      float x1 = particle_1->x;
      float y1 = particle_1->y;
      float x2 = particle_2->x + epsilon;
      float y2 = particle_2->y + epsilon;

      float delta_lxy = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
      float delta_lxy_ratio_abs = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))/sqrt(pow(abs(x1) + abs(x2), 2) + pow(abs(y1) + abs(y2), 2));
      if(delta_lxy_ratio_abs <= 0.05){
        histSets["alp_final_selection_"+sign+"_maxlxy-muon"]->fill(particle_maxlxy);
        histSets["alp_final_selection_"+sign+"_minlxy-muon"]->fill(particle_minlxy);
        histSets["alp_final_selection_"+sign+"_minpt-muon"]->fill(particle_minpt);
        histSets["alp_final_selection_"+sign+"_first_mother"]->fill(mother);
        histSets["alp_final_selection_"+sign+"_dimuon"]->fill(particle_1, particle_2);
        histSets["alp_final_selection_"+sign+"_first_mother"]->fill_2d(particle_1, particle_2, mother);
      }
    }
  }
}

void HistogramFiller::fill_first_muon_from_alp_selection_hists(const Particle* particle, const Event *event)
{
  if(!particle) return;
  histSets["alp_selection_os_minlxy-muon"]->fill(particle, event);
};

void HistogramFiller::fill_2d_hists(const Particle* particle_1, const Particle* particle_2, string sign)
{
  if(!particle_1 || !particle_2) return;
  histSets[sign+"_dimuon"]->fill_2d(particle_1, particle_2);
}

void HistogramFiller::save_histograms(std::string output_path)
{
  auto output_file = new TFile(output_path.c_str(), "recreate");
  output_file->cd();
  output_file->mkdir("final_selection");
  output_file->mkdir("alp_selections");
  if(!reduceHists){
    output_file->mkdir("intermediate_selections");
    output_file->mkdir("alp");
  }

  // if (reduceHists){
  //   for(auto &[hist_name, hist_set] : histSets){
  //     if(hist_name.substr(0,15) == "final_selection"){
  //       output_file->cd("final_selection");
  //     }
  //     if(hist_name.substr(0,5) == "alp_s"){
  //       output_file->cd("alp_selections");
  //     }
  //     for(auto &[tmp, hist] : hist_set->hists){
  //       hist->Write();
  //     }
  //     output_file->cd();
  //   }
  // }
  // else {
    for(auto &[hist_name, hist_set] : histSets){
      if(hist_name.substr(0,15) == "final_selection"){
        output_file->cd("final_selection");
      }
      if(hist_name.substr(0,3) == "sel"){
        output_file->cd("intermediate_selections");
      }
      if(hist_name.substr(0,5) == "alp_s"){
        output_file->cd("alp_selections");
      }
      else if(hist_name.substr(0,3) == "alp"){
        output_file->cd("alp");
      }
      for(auto &[tmp, hist] : hist_set->hists){
        hist->Write();
      }
      for(auto &[tmp, hist2d] : hist_set->hists2d){
        hist2d->Write();
      }
      output_file->cd();
    }
  // }
  output_file->Close();
}
