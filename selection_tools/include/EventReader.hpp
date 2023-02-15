//
//  EventReader.hpp
//  selections
//
//  Created by Jeremi Niedziela on 13/02/2023.
//

#ifndef EventReader_hpp
#define EventReader_hpp

#include <stdio.h>
#include <vector>

#include <TTree.h>

#include "Event.hpp"

class EventReader {
public:
  EventReader(int _max_events=-1, int _n_daughters=3): max_events(_max_events), n_daughters(_n_daughters){}
  
  std::vector<Event*> read_events(TTree *tree);
  
private:
  int max_events;
  int n_daughters;
  
};

#endif /* EventReader_hpp */
