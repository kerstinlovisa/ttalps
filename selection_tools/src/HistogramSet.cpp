//
//  HistogramSet.cpp
//  selections
//
//  Created by Jeremi Niedziela on 24/02/2023.
//

#include "HistogramSet.hpp"

using namespace std;

HistogramSet::HistogramSet(string prefix)
{
  hists["pt"]       = new TH1D((prefix+"_pt").c_str(),    (prefix+"_pt").c_str(),           1000, 0,      100   );
  hists["pz"]       = new TH1D((prefix+"_pz").c_str(),    (prefix+"_pz").c_str(),           1000, 0,      100   );
  // hists["mass"]     = new TH1D((prefix+"_mass").c_str(),  (prefix+"_mass").c_str(),         1000, 0,      100   );
  hists["mass"]     = new TH1D((prefix+"_mass").c_str(),  (prefix+"_mass").c_str(),         1000,         logxBins(1000,0.1,100));
  hists["eta"]      = new TH1D((prefix+"_eta").c_str(),   (prefix+"_eta").c_str(),          1000, -5,     5     );
  hists["phi"]      = new TH1D((prefix+"_phi").c_str(),   (prefix+"_phi").c_str(),          1000, -4,     4     );
  hists["y"]        = new TH1D((prefix+"_y").c_str(),     (prefix+"_y").c_str(),            1000, -10,    10    );
  hists["theta"]    = new TH1D((prefix+"_theta").c_str(), (prefix+"_theta").c_str(),        1000, -5,     5     );
  hists["lxy"]      = new TH1D((prefix+"_lxy").c_str(),   (prefix+"_lxy").c_str(),          1000, 0,      100   );
  hists["lz"]       = new TH1D((prefix+"_lz").c_str(),    (prefix+"_lz").c_str(),           1000, 0,      100   );
  hists["lxyz"]     = new TH1D((prefix+"_lxyz").c_str(),  (prefix+"_lxyz").c_str(),         1000, 0,      100   );
  hists["ctau"]     = new TH1D((prefix+"_ctau").c_str(),  (prefix+"_ctau").c_str(),         1000, 0,      100   );
  hists["boost"]    = new TH1D((prefix+"_boost").c_str(), (prefix+"_boost").c_str(),        1000, 0,      500   );
  hists["deltaR"]   = new TH1D((prefix+"_deltaR").c_str(),   (prefix+"_deltaR").c_str(),    1000, 0,      10    );
  hists["deltaPhi"] = new TH1D((prefix+"_deltaPhi").c_str(), (prefix+"_deltaPhi").c_str(),  1000, -5,     5     );
}

void HistogramSet::fill(const Particle *particle)
{
  hists["pt"]->Fill(particle->four_vector.Pt());
  hists["pz"]->Fill(particle->four_vector.Pz());
  hists["mass"]->Fill(particle->four_vector.M());
  hists["eta"]->Fill(particle->four_vector.Eta());
  hists["phi"]->Fill(particle->four_vector.Phi());
  hists["y"]->Fill(particle->four_vector.Rapidity());
  hists["theta"]->Fill(particle->four_vector.Theta());
  hists["lxy"]->Fill(sqrt(pow(particle->x, 2) + pow(particle->y, 2)));
  hists["lz"]->Fill(particle->z);
  hists["lxyz"]->Fill(sqrt(pow(particle->x, 2) + pow(particle->y, 2) + pow(particle->z, 2)));
  hists["ctau"]->Fill(particle->ctau);
  hists["boost"]->Fill(particle->momentum()/particle->mass);
}

void HistogramSet::fill(const Particle* particle_1, const Particle* particle_2)
{
 
  hists["deltaPhi"]->Fill(particle_1->four_vector.DeltaPhi(particle_2->four_vector));
  hists["deltaR"]->Fill(particle_1->four_vector.DeltaR(particle_2->four_vector));
  
  TLorentzVector diparticle = particle_1->four_vector + particle_2->four_vector;
  hists["pt"]->Fill(diparticle.Pt());
  hists["pz"]->Fill(diparticle.Pz());
  hists["mass"]->Fill(diparticle.M());
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