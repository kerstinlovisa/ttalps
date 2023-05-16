//
//  CutsManager.hpp
//  selections
//
//  Created by Jeremi Niedziela on 04/04/2023.
//

#ifndef CutsManager_hpp
#define CutsManager_hpp

#include <map>
#include <string>

#include <TLorentzVector.h>

class CutsManager {
public:
  CutsManager(bool displaced_mass_cuts=true);
  ~CutsManager(){}
  
  bool passes_mass_cuts(const TLorentzVector &diparticle);
  
private:
  std::map<std::string, float> masses = {}; // in GeV
  std::map<std::string, float> mass_cuts = {}; // in GeV
  
  std::map<std::string, float> mass_min; // in GeV
  std::map<std::string, float> mass_max; // in GeV
  
};

#endif /* CutsManager_hpp */
