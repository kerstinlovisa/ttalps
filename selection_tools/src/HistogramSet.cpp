//
//  HistogramSet.cpp
//  selections
//
//  Created by Jeremi Niedziela on 24/02/2023.
//

#include "HistogramSet.hpp"
#include <iostream>
#include <random>

using namespace std;

HistogramSet::HistogramSet(string prefix)
{
  hists["pt"]       = new TH1D((prefix+"_pt").c_str(),    (prefix+"_pt").c_str(),           1000, 0,      500   );
  hists["pz"]       = new TH1D((prefix+"_pz").c_str(),    (prefix+"_pz").c_str(),           1000, 0,      500   );
  hists["mass_log"] = new TH1D((prefix+"_mass_log").c_str(),  (prefix+"_mass_log").c_str(), 1000,    logxBins(1000,0.1,150));
  hists["mass"]     = new TH1D((prefix+"_mass").c_str(),  (prefix+"_mass").c_str(),         10000, 0.1,   150   );
  hists["eta"]      = new TH1D((prefix+"_eta").c_str(),   (prefix+"_eta").c_str(),          1000, -5,     5     );
  hists["phi"]      = new TH1D((prefix+"_phi").c_str(),   (prefix+"_phi").c_str(),          1000, -5,     5     );
  // hists["y"]        = new TH1D((prefix+"_y").c_str(),     (prefix+"_y").c_str(),            1000, -5,     5     );
  // hists["theta"]    = new TH1D((prefix+"_theta").c_str(), (prefix+"_theta").c_str(),        1000, -5,     5     );
  hists["lxy"]      = new TH1D((prefix+"_lxy").c_str(),   (prefix+"_lxy").c_str(),          10000,0,      1000   );
  hists["lxy_logx"]      = new TH1D((prefix+"_lxy_logx").c_str(),   (prefix+"_lxy_logx").c_str(),100000,  logxBins(100000,0.0001,100));
  float binList[7] = {0, 2, 10, 24, 31, 70, 110}; // mm
  hists["lxy_rebinned"]= new TH1D((prefix+"_lxy_rebinned").c_str(),   (prefix+"_lxy_rebinned").c_str(),6, binList);
  float bin2List[3] = {0, 10, 110};
  hists["lxy_2bins"]= new TH1D((prefix+"_lxy_2bins").c_str(),   (prefix+"_lxy_rebinned").c_str(),2, bin2List);
  hists["lz"]       = new TH1D((prefix+"_lz").c_str(),    (prefix+"_lz").c_str(),           10000,0,      1000  );
  hists["lxyz"]     = new TH1D((prefix+"_lxyz").c_str(),  (prefix+"_lxyz").c_str(),         10000,0,      1000  );
  hists["ctau"]     = new TH1D((prefix+"_ctau").c_str(),  (prefix+"_ctau").c_str(),         1000, 0,      1000  );
  hists["proper_ctau"]     = new TH1D((prefix+"_proper_ctau").c_str(),  (prefix+"_proper_ctau").c_str(),         1000, 0,      1  );
  hists["boost"]    = new TH1D((prefix+"_boost").c_str(), (prefix+"_boost").c_str(),        1000, 0,      500   );
  hists["deltaR"]   = new TH1D((prefix+"_deltaR").c_str(),   (prefix+"_deltaR").c_str(),    1000, 0,      10    );
  // hists["deltaPhi"] = new TH1D((prefix+"_deltaPhi").c_str(), (prefix+"_deltaPhi").c_str(),  1000, -5,     5     );
  hists["deltalxy"] = new TH1D((prefix+"_deltalxy").c_str(), (prefix+"_deltalxy").c_str(),  10000, 0,      10   );
  hists["deltalxy_diff_abs"]= new TH1D((prefix+"_deltalxy_diff_abs").c_str(), (prefix+"_deltalxy_diff_abs").c_str(),          1000, 0,   10   );
  hists["deltalxy_ratio"] = new TH1D((prefix+"_deltalxy_ratio").c_str(), (prefix+"_deltalxy_ratio").c_str(),                  1000, 0,   10   );
  hists["deltalxy_ratio_abs"] = new TH1D((prefix+"_deltalxy_ratio_abs").c_str(), (prefix+"_deltalxy_ratio_abs").c_str(),      10000, 0,   10 );
  hists["deltalxy_ratio_error"] = new TH1D((prefix+"_deltalxy_ratio_error").c_str(), (prefix+"_deltalxy_ratio_error").c_str(),10000, 0,   10   );
  hists["deltalxy_ratio_abs_error"] = new TH1D((prefix+"_deltalxy_ratio_abs_error").c_str(), (prefix+"_deltalxy_ratio_abs_error").c_str(),10000, 0,   10   );
  hists["deltapt"]  = new TH1D((prefix+"_deltapt").c_str(), (prefix+"_deltapt").c_str(),    1000, 0,      500   );
}

void HistogramSet::fill(const Particle *particle, const Event *event)
{
  hists["pt"]->Fill(particle->four_vector.Pt());
  hists["pz"]->Fill(particle->four_vector.Pz());
  hists["mass"]->Fill(particle->four_vector.M());
  hists["mass_log"]->Fill(particle->four_vector.M());
  hists["eta"]->Fill(particle->four_vector.Eta());
  hists["phi"]->Fill(particle->four_vector.Phi());
  // hists["y"]->Fill(particle->four_vector.Rapidity());
  // hists["theta"]->Fill(particle->four_vector.Theta());
  hists["lxy"]->Fill(sqrt(pow(particle->x, 2) + pow(particle->y, 2)));
  hists["lxy_logx"]->Fill(sqrt(pow(particle->x, 2) + pow(particle->y, 2)));
  hists["lxy_rebinned"]->Fill(sqrt(pow(particle->x, 2) + pow(particle->y, 2)));
  hists["lxy_2bins"]->Fill(sqrt(pow(particle->x, 2) + pow(particle->y, 2)));
  hists["lz"]->Fill(particle->z);
  hists["lxyz"]->Fill(sqrt(pow(particle->x, 2) + pow(particle->y, 2) + pow(particle->z, 2)));
  hists["ctau"]->Fill(particle->ctau);
  if(event){
    auto mother = event->particles[particle->mothers[0]];
    hists["proper_ctau"]->Fill(particle->ctau/(mother->momentum()/mother->mass));
  }
  hists["boost"]->Fill(particle->momentum()/particle->mass);
}

void HistogramSet::fill(const Particle* particle_1, const Particle* particle_2)
{
  float epsilon = 1e-10;
  float x1 = particle_1->x;
  float y1 = particle_1->y;
  float x2 = particle_2->x + epsilon;
  float y2 = particle_2->y + epsilon;
  // hists["deltaPhi"]->Fill(particle_1->four_vector.DeltaPhi(particle_2->four_vector));
  hists["deltaR"]->Fill(particle_1->four_vector.DeltaR(particle_2->four_vector));
  // sqrt( (x1-x2)^2 + (y1-y2)^2 )
  hists["deltalxy"]->Fill(sqrt(pow(x1 - x2 , 2) + pow(y1 - y2, 2)));
 
  double lxy_1 = sqrt(pow(x1, 2) + pow(y1, 2));
  double lxy_2 = sqrt(pow(x2, 2) + pow(y2, 2));

  // | lxy_1 - lxy_2 |
  hists["deltalxy_diff_abs"]->Fill(abs(lxy_1 - lxy_2));
  // sqrt((x1-x2)^2 +(y1-y2)^2) / sqrt((x1+x2)^2 + (y1+y2)^2)
  hists["deltalxy_ratio"]->Fill(sqrt(pow(x1 - x2 , 2) + pow(y1 - y2, 2))/sqrt(pow(x1 + x2 , 2) + pow(y1 + y2, 2)));
  hists["deltalxy_ratio_abs"]->Fill(sqrt(pow(x1 - x2 , 2) + pow(y1 - y2, 2))/sqrt(pow(abs(x1) + abs(x2) , 2) + pow(abs(y1) + abs(y2), 2)));

  float delta_x = 0.3/sqrt(2);
  // (x1-x2)^2 + (y1-y2)^2
  float C_minus = pow(x1 - x2 , 2) + pow(y1 - y2, 2);
  // (x1+x2)^2 + (y1+y2)^2
  float C_plus = pow(x1 + x2 , 2) + pow(y1 + y2, 2);
  hists["deltalxy_ratio_error"]->Fill(sqrt(2*pow(delta_x,2)*(1+(C_minus/C_plus))/C_plus));
  float C_plus_abs = pow(abs(x1) + abs(x2) , 2) + pow(abs(y1) + abs(y2), 2);
  float dR2 = (2*pow(delta_x,2)/pow(C_plus_abs,2))*(C_minus + C_plus_abs + (abs(x1)+abs(x2)*(x1-x2)*((x1/abs(x1))-(x2/abs(x2)))) + (abs(y1)+abs(y2)*(y1-y2)*((y1/abs(y1))-(y2/abs(y2)))) );
  hists["deltalxy_ratio_abs_error"]->Fill(sqrt(dR2));
  
  hists["deltapt"]->Fill(abs(particle_1->four_vector.Pt()-particle_2->four_vector.Pt()));
  
  TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;
  hists["pt"]->Fill(diparticle.Pt());
  hists["pz"]->Fill(diparticle.Pz());
  hists["mass"]->Fill(diparticle.M());
  hists["mass_log"]->Fill(diparticle.M());
  hists["eta"]->Fill(diparticle.Eta());
  hists["phi"]->Fill(diparticle.Phi());
}

float* HistogramSet::logxBins(const int n_bins, const float min, const float max)
{
  float* binList = new float[n_bins+1];
  for (int i=0; i<n_bins+1; i++) {
    binList[i] = (pow(10,log10(min)+((log10(max)-log10(min))/n_bins)*i));
  }
  return binList;
}
